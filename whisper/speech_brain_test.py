import gc
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
from transformers import LlavaNextVideoForConditionalGeneration, LlavaNextVideoProcessor
from PIL import Image
import cv2
import torch

def concat_videos_by_timestamp(
    mp4_dir: str,
    output_video: str = "merged_video.mp4"
):
    p = Path(mp4_dir)
    pattern = re.compile(r"^final_.+?_(\d{8}_\d{6})\.mp4$")
    entries = []
    for f in p.glob("*.mp4"):
        m = pattern.match(f.name)
        if not m:
            continue
        ts = datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
        entries.append((ts, f))
    if not entries:
        raise RuntimeError("❌ 没找到任何匹配的 MP4 文件")
    entries.sort(key=lambda x: x[0])

    list_file = Path(mp4_dir) / "concat_list.txt"
    with open(list_file, "w") as f:
        for _, mp4 in entries:
            abs_path = mp4.resolve().as_posix()
            f.write(f"file '{abs_path}'\n")

    print("🔧 正在合并视频：")
    for _, mp4 in entries:
        print("   ▶", mp4.name)

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        output_video
    ]
    print("Running:", " ".join(cmd))
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print("=== FFmpeg STDERR ===")
        print(result.stderr)
        raise RuntimeError(f"❌ FFmpeg 视频合并失败，返回码：{result.returncode}")
    print(f"✅ 视频合并完成：{output_video}")
    return output_video

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
from pathlib import Path

def extract_video_insights_with_llava(
    mp4_dir: str,
    llava_cache: str,
    llava_model_name: str = "llava-hf/LLaVA-NeXT-Video-7B-hf",
    num_frames: int = 30,
    raw_prompt: str = "Make a summarization for the video part of this video (not include audio)"
) -> str:

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("🖥️ 使用设备：", device)

    model = LlavaNextVideoForConditionalGeneration.from_pretrained(
        llava_model_name,
        torch_dtype=torch.float16,
        cache_dir=llava_cache,
        low_cpu_mem_usage=True,
    ).to(device)

    processor = LlavaNextVideoProcessor.from_pretrained(llava_model_name, cache_dir=llava_cache)

    cap = cv2.VideoCapture(mp4_dir)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = total_frames // num_frames
    logger.info(interval)
    # 创建帧图像输出目录
    frame_dir = Path(mp4_dir).parent / "llava_frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            continue
        if i % interval == 0:
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frames.append(pil_img)
    cap.release()
    conversation = [
        {

            "role": "user",
            "content": [
                {"type": "text", "text": raw_prompt},
                {"type": "video"},
                ],
        },
    ]
    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(text=prompt, videos=frames, padding=True, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    raw_text = processor.decode(output[0], skip_special_tokens=True)
    # 提取 ASSISTANT 后的部分
    if "ASSISTANT:" in raw_text:
        response = raw_text.split("ASSISTANT:", 1)[1].strip()
    else:
        response = raw_text.strip()  # fallback
    return response

def extract_and_diarize_transcribe_and_visualize(
        mp4_dir: str,
        whisper_model: str = "large",
        whisper_cache: str = "/root/autodl-tmp/whisper_model",
        llava_cache: str = "/root/autodl-tmp/llava_model",
        llava_model: str = "llava-hf/LLaVA-NeXT-Video-7B-hf",
        num_speakers: int = None
    ):
    merged = "merged.wav"
    logger.info("Start FFMPEG MERGE")
    mix_audio_by_timestamp(mp4_dir, merged)
    logger.info("END FFMPEG MERGE")

    logger.info("START DIARIZE WORK")
    diarization = diarize_with_speechbrain(merged, whisper_cache, num_speakers)
    logger.info("END DIARIZE WORK")

    # Whisper
    model = whisper.load_model(whisper_model, download_root=whisper_cache)
    result = model.transcribe(merged, language=None, task="transcribe")

    enriched = []
    for seg in result['segments']:
        mid = (seg['start'] + seg['end']) / 2
        spk = next((d['speaker'] for d in diarization if d['start'] <= mid < d['end']), 'unknown')
        enriched.append({
            'speaker': spk,
            'start': seg['start'],
            'end': seg['end'],
            'text': seg['text'].strip()
        })

    del model  # 或 del whisper_model
    gc.collect()
    torch.cuda.empty_cache()
    # 选择一个视频文件（取时间最早那段）
    merged_video = concat_videos_by_timestamp(mp4_dir)
    video_summarization = extract_video_insights_with_llava(mp4_dir=merged_video, llava_cache=llava_cache, llava_model_name=llava_model)

    return {
        'language': result['language'],
        'segments': enriched,
        'video_summarization': video_summarization
    }


# if __name__ == "__main__":
#     out = extract_and_diarize_transcribe_and_visualize(
#         mp4_dir='.',
#         whisper_model='medium',
#         whisper_cache='/root/autodl-tmp/whisper_model',
#         num_speakers=3
#     )
#     logger.info("Detected language:", out['language'])
#     json_str = json.dumps(out, ensure_ascii=False)  
#     # ensure_ascii=False 保证中文不会被转成 \uXXXX，输出更可读
#     print(json_str)
