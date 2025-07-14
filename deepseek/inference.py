from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from unsloth import FastLanguageModel
from peft import PeftModel
from transformers import TextStreamer
import torch

app = FastAPI()

# 🧠 初始化模型和 tokenizer
cache_dir = "/root/autodl-tmp/llm-model"
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-32B-bnb-4bit",
    cache_dir=cache_dir,
    load_in_4bit=True,
    max_seq_length=4096,
)
model = PeftModel.from_pretrained(model, f"{cache_dir}/qwen3-32b-summarization-lora-finetuned")
model = model.merge_and_unload()
model = PeftModel.from_pretrained(model, f"{cache_dir}/qwen3-32b-summarization-lora-finetuned-meetingbank")
model.eval()

# 📄 输入数据结构
class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str
    speaker: str

@app.post("/summarize")
async def summarize_audio_segments(segments: List[TranscriptSegment]):
    # 拼接所有文字内容
    transcript_text = "\n".join([f"{seg.speaker}: {seg.text}" for seg in segments])

    # 构造模型输入
    input_text = f"<|user|>\nSummarize this meeting transcript:\n\n{transcript_text}\n<|end|>"
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    # 推理
    output = model.generate(
        **inputs,
        do_sample=False,
        temperature=0.7,
        top_p=0.95,
    )
    summary = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"summary": summary.strip()}
