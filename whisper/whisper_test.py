
import re
import subprocess
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

import whisper
from pyannote.audio import Pipeline  # pip install pyannote.audio
from loguru import logger

def mix_audio_by_timestamp(
    mp4_dir: str,
    output_wav: str = "merged.wav"
):
    """
    扫描 mp4_dir 下所有 final_<任意>_<YYYYMMDD_HHMMSS>.mp4，
    提取音频、根据时间戳延迟、然后混合到一个输出文件 mixed.wav。
    """
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
    # 按时间戳升序
    entries.sort(key=lambda x: x[0])
    # 找到最早的时间，作为基准
    t0 = entries[0][0]

    inputs = []
    delays = []
    for idx, (ts, mp4) in enumerate(entries):
        # 提取音频到 pipe: 这里我们直接让 ffmpeg 处理 mp4 输入并解码
        inputs += ["-i", str(mp4)]
        # 计算相对延迟（毫秒）
        delta_ms = int((ts - t0).total_seconds() * 1000)
        # 生成每路的 adelay 参数
        # 单声道 WAV 用 "delay|delay"
        delays.append(f"[{idx}:a]adelay={delta_ms}|{delta_ms}[a{idx}]")

    # 把所有延迟后的流名称拼起来
    delayed_streams = "".join(f"[a{idx}]" for idx in range(len(entries)))
    # amix 参数：inputs=N, duration=longest
    amix = f"{delayed_streams}amix=inputs={len(entries)}:duration=longest:dropout_transition=0[mixout]"

    # 拼 filter_complex
    filter_complex = ";".join(delays + [amix])

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[mixout]",
        "-c:a", "pcm_s16le",     # PCM 16-bit
        output_wav
    ]

    # 打印一下看命令是否正确
    logger.info("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    logger.info(f"✅ 混合完成：{output_wav}")

def extract_merge_and_diarize_transcribe(
    merged_wav: str = "merged.wav",
    whisper_model: str = "large",
    whisper_cache: str = "/root/autodl-tmp/whisper_model",
    hf_token: str = None,  # HuggingFace API token
):
    logger.info("分离对话")
    # ── 2. 说话人分离 ───────────────────────────────
    # 你需要提前在环境变量 HF_API_TOKEN 中设置你的 HuggingFace Token
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token or "",
        cache_dir=whisper_cache
    )
    import torch
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    pipeline = pipeline.to(torch.device('cuda:0'))

    diarization = pipeline(merged_wav)
    # diarization 是一个 pyannote.core.Annotation，下面映射到 (segment, speaker)
    turns = []
    for segment, track, speaker in diarization.itertracks(yield_label=True):
        turns.append({
            "start": segment.start,
            "end":   segment.end,
            "speaker": speaker
        })
    logger.info("whisper开始")

    # ── 3. Whisper 转写 ─────────────────────────────
    model = whisper.load_model(whisper_model, download_root=whisper_cache)
    result = model.transcribe(merged_wav, language="en", task="transcribe")

    # ── 4. 给每段转写打上 speaker 标签 ─────────────
    enriched_segments = []
    for seg in result["segments"]:
        mid = (seg["start"] + seg["end"]) / 2
        # 找到包含 mid 的说话人区间
        spk = None
        for turn in turns:
            if turn["start"] <= mid < turn["end"]:
                spk = turn["speaker"]
                break
        enriched_segments.append({
            "speaker": spk or "unknown",
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        })

    return {
        "language": result["language"],
        "segments": enriched_segments
    }


if __name__ == "__main__":
    out = mix_audio_by_timestamp(".")
    text_out = extract_merge_and_diarize_transcribe(
        merged_wav="merged.wav",
        whisper_model="medium",
        whisper_cache="/root/autodl-tmp/whisper_model",
    )

    logger.info("Detected language:", text_out["language"])
    for seg in text_out["segments"]:
        print(f"[{seg['speaker']}] {seg['start']:.1f}s→{seg['end']:.1f}s: {seg['text']}")
