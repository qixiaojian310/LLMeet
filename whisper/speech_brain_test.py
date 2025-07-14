import json
import re
import subprocess
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

import whisper
import torch
from scipy.io import wavfile
from speechbrain.inference.speaker import EncoderClassifier
from sklearn.cluster import AgglomerativeClustering
from loguru import logger
# ---------------------------------------------
# 1. 合并音频（与原 mix_audio_by_timestamp 保持一致）
# ---------------------------------------------
def mix_audio_by_timestamp(
    mp4_dir: str,
    output_wav: str = "merged.wav"
):
    p = Path(mp4_dir)
    pattern = re.compile(r"^final_.+?_(\d{8}_\d{6})\.mp4$")
    entries = []
    for f in p.glob("*.mp4"):
        m = pattern.match(f.name)
        if not m: continue
        ts = datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
        entries.append((ts, f))
    if not entries:
        raise RuntimeError("没找到任何匹配的 MP4 文件")
    entries.sort(key=lambda x: x[0])
    t0 = entries[0][0]

    inputs = []
    delays = []
    for idx, (ts, mp4) in enumerate(entries):
        inputs += ["-i", str(mp4)]
        delta_ms = int((ts - t0).total_seconds() * 1000)
        delays.append(f"[{idx}:a]adelay={delta_ms}|{delta_ms}[a{idx}]")

    delayed = "".join(f"[a{idx}]" for idx in range(len(entries)))
    amix = f"{delayed}amix=inputs={len(entries)}:duration=longest:dropout_transition=0[mixout]"
    filter_complex = ";".join(delays + [amix])

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[mixout]",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        output_wav
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"✅ 合并完成：{output_wav}")

# ---------------------------------------------------
# 2. 使用 SpeechBrain 提取说话人嵌入 + 聚类 (Diarization)
# ---------------------------------------------------
def diarize_with_speechbrain(
    merged_wav: str,
    model_cache: str,
    num_speakers: int = None,
    window_size: float = 2.0
):
    # 读取合并后的 WAV
    sr, audio = wavfile.read(merged_wav)
    audio = audio.astype('float32') / 32768.0  # PCM16 -> float32

    # 切分为固定窗口
    total_sec = len(audio) / sr
    segments = []
    t = 0.0
    while t < total_sec:
        start = t
        end = min(t + window_size, total_sec)
        segments.append((start, end))
        t += window_size

    # 加载 ECAPA-TDNN 说话人嵌入模型
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=f"{model_cache}/speechbrain/spkrec-ecapa-voxceleb"
    )

    embeddings = []
    for start, end in segments:
        s_frame = int(start * sr)
        e_frame = int(end * sr)
        sig = torch.from_numpy(audio[s_frame:e_frame]).unsqueeze(0)
        emb = classifier.encode_batch(sig)
        embeddings.append(emb.squeeze().cpu().numpy())

    # 聚类
    k = num_speakers or 2
    clustering = AgglomerativeClustering(n_clusters=k).fit(embeddings)

    diarization = []
    for (start, end), label in zip(segments, clustering.labels_):
        diarization.append({
            "start": start,
            "end": end,
            "speaker": f"SPK{label:02d}"
        })
    return diarization

# ---------------------------------------------------
# 3. 合并 & 分离 & 转写 主流程
# ---------------------------------------------------
    
def extract_and_diarize_transcribe(
        mp4_dir: str,
        whisper_model: str = "large",
        whisper_cache: str = "/root/autodl-tmp/whisper_model",
        num_speakers: int = None
    ):
        merged = "merged.wav"
        logger.info("Start FFMPEG MERGE")
        mix_audio_by_timestamp(mp4_dir, merged)
        logger.info("END FFMPEG MERGE")
        # SpeechBrain Diarization
        logger.info("START DIARIZE WORK")
        diarization = diarize_with_speechbrain(merged, whisper_cache , num_speakers)
        logger.info("END DIARIZE WORK")
        # Whisper 转写
        model = whisper.load_model(whisper_model, download_root=whisper_cache)
        result = model.transcribe(merged, language=None, task="transcribe")
        print(result)
        enriched = []
        for seg in result['segments']:
            mid = (seg['start'] + seg['end']) / 2
            # 找匹配的 speaker
            spk = next((d['speaker'] for d in diarization if d['start'] <= mid < d['end']), 'unknown')
            enriched.append({
                'speaker': spk,
                'start': seg['start'],
                'end': seg['end'],
                'text': seg['text'].strip()
            })
        return {'language': result['language'], 'segments': enriched}

if __name__ == "__main__":
    out = extract_and_diarize_transcribe(
        mp4_dir='.',
        whisper_model='medium',
        whisper_cache='/root/autodl-tmp/whisper_model',
        num_speakers=3
    )
    logger.info("Detected language:", out['language'])
    json_str = json.dumps(out, ensure_ascii=False)  
    # ensure_ascii=False 保证中文不会被转成 \uXXXX，输出更可读
    for seg in out['segments']:
        print(f"[{seg['speaker']}] {seg['start']:.1f}s→{seg['end']:.1f}s: {seg['text']}")
