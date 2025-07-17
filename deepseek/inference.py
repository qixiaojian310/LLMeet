import torch
from unsloth.chat_templates import get_chat_template
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Literal, Optional
from unsloth import FastLanguageModel
from peft import PeftModel
from transformers import TextIteratorStreamer
from fastapi.responses import StreamingResponse
import threading
import asyncio
import json

# 🧠 全局模型变量
model = None
tokenizer = None

# 📄 数据结构
class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str
    speaker: str

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    segments: Optional[List[TranscriptSegment]]
    video_summarization: str
    stream: bool = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    # —— 在这里放启动逻辑 ——  
    cache_dir = "/root/autodl-tmp/llm-model"
    global model, tokenizer
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Qwen3-14B-bnb-4bit",
        cache_dir=cache_dir,
        load_in_4bit=True,
        max_seq_length=16384,
        device_map="auto",
    )
    tokenizer = get_chat_template(
        tokenizer,
        chat_template="qwen3",
        mapping={"role": "role", "content": "content", "user": "user", "assistant": "assistant"}
    )
    model = PeftModel.from_pretrained(model, f"{cache_dir}/qwen3-14b-summarization-lora-finetuned")
    model = model.merge_and_unload()
    model = PeftModel.from_pretrained(model, f"{cache_dir}/qwen3-14b-summarization-lora-finetuned-meetingbank")
    model.eval()
    yield

app = FastAPI(lifespan=lifespan)

# 🔧 将同步迭代器转换为异步生成器
async def _aiter_from_sync(sync_iter):
    for item in sync_iter:
        yield item
        await asyncio.sleep(0)

def build_summarization_messages(segments: List[TranscriptSegment], video_summarization: str) -> List[dict]:
    system = {
        "role": "system",
        "content": (
            "You are a multilingual meeting summarization assistant. "
            "Please read the transcript below and generate a concise summary in the same language as the conversation. "
            "For example, summarize in English if the transcript is in English, and summarize in Chinese if the transcript is in Chinese.\n\n"
            "你是一个多语言会议摘要助手，请根据会议内容所使用的语言输出对应语言的简洁摘要。"
            "Next, I will send you two parts of data. One is the text transcription of the video's audio, and the other is the summary of the video's images. The video images are the screen shots from the video conference camera. You can refer to both of them simultaneously."
            "I can now assure you that visual summary refers to the camera footage of multiple participants in a video conference."
            "During the process of generating the summary, do not simply merge the visual summary and the transcript, but instead describe it in natural language."
        )
    }

    transcript_text = "\n".join(f"{s.speaker}: {s.text}" for s in segments)
    fewshot_user = {
        "role": "user",
        "content": (
            "Transcript:\n"
            "SPK01: Welcome everyone to today's product meeting.\n"
            "SPK02: Let's start by reviewing the timeline for our next app release.\n"
            "SPK01: We are aiming for an internal beta by mid-August.\n"
            "SPK03: The new UI has been completed, pending QA review.\n\n"
            "Visual Summary (video without audio):\n"
            "Three people are sitting around a meeting table, each with a laptop. "
            "One participant is presenting slides on a shared screen.\n\n"
            "Please generate a meeting summary based on the above."
        )
    }
    # ❷ One-shot 输出
    fewshot_assistant = {
        "role": "assistant",
        "content": (
            "The team reviewed the timeline for the next app release, targeting an internal beta by mid-August. "
            "The new UI is complete and awaits QA. Participants were engaged while one member presented the slides."
        )
    }
    user = {
        "role": "user",
        "content": (
            f"Transcript:\n{transcript_text}\n\n"
            f"Visual Summary (video without audio):\n{video_summarization}\n\n"
            f"Please generate a meeting summary based on the above. "
        )
    }
    return [system, fewshot_user, fewshot_assistant, user]

async def _stream_response(chat_messages: List[dict]):
    if not hasattr(tokenizer, "apply_chat_template"):
        raise RuntimeError("tokenizer 不支持 apply_chat_template 方法")
    
    prompt = tokenizer.apply_chat_template(chat_messages, tokenize=False)
    inputs = tokenizer(prompt, return_tensors="pt", return_token_type_ids=False).to(model.device)

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_special_tokens=True,
        skip_prompt=True,
    )
    thread = threading.Thread(
        target=model.generate,
        kwargs={
            **inputs,
            "max_new_tokens": 4096,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "streamer": streamer,
        },
    )
    thread.daemon = True
    thread.start()

    collecting = False
    buffer = ""

    async for token in _aiter_from_sync(streamer):
        buffer += token
        if not collecting:
            if "</think>" in buffer:
                collecting = True
                buffer = buffer.split("</think>", 1)[1]  # 只保留 think 后内容
                continue
            else:
                continue

        # 进入正式输出阶段
        chunk = {"choices": [{"delta": {"content": token}, "index": 0, "finish_reason": None}]}
        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
    torch.cuda.empty_cache()
    yield "data: [DONE]\n\n"

# 🚀 /v1/chat/completions
@app.post("/v1/chat/completions")
async def chat(req: ChatRequest):
    messages = [m.model_dump() for m in req.messages]
    if req.segments:
        try:
            segment_text = "\n".join(f"{s.speaker}: {s.text}" for s in req.segments)
            summary_hint = {
                "role": "system",
                "content": (
                    "Below is the meeting transcript background. Please refer to it when answering the user's question. "
                    "You should respond in the same language as the user's question. For example, reply in English if the user asks in English, "
                    "and reply in Chinese if the user asks in Chinese.\n\n"
                    "以下是会议的文字记录和无声视频的图像总结。请结合**两者**回答用户问题。"
                    "若视频中包含文字记录未体现的重要信息，请务必在回答中体现。"
                    f"The Transcript of this meeting is {segment_text}, and the pure image video (without audio) summarization is {req.video_summarization}"
                )
            }
            messages.insert(0, summary_hint)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Segment parse error: {e}")
    if req.stream:
        return StreamingResponse(_stream_response(messages), media_type="text/event-stream")
    else:
        prompt = tokenizer.apply_chat_template(messages, tokenize=False)
        inputs = tokenizer(prompt, return_tensors="pt", return_token_type_ids=False).to(model.device)
        output = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            temperature=0.7,
            top_p=0.95,
        )
        text = tokenizer.decode(output[0], skip_special_tokens=False).strip()
        return {
            "id": "chatcmpl-chatmode",
            "object": "chat.completion",
            "choices": [
                {"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}
            ]
        }

# 🚀 /v1/chat/summarization
@app.post("/v1/chat/summarization")
async def summarization(req: ChatRequest):
    if not req.messages or not req.messages[0].content:
        raise HTTPException(status_code=400, detail="Invalid input")
    try:
        segments = json.loads(req.messages[0].content)
        segments = [TranscriptSegment(**seg) for seg in segments]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"JSON parse error: {e}")
    
    messages = build_summarization_messages(segments,req.video_summarization)
    if req.stream:
        return StreamingResponse(_stream_response(messages), media_type="text/event-stream")
    
    prompt = tokenizer.apply_chat_template(messages, tokenize=False)
    inputs = tokenizer(prompt, return_tensors="pt", return_token_type_ids=False).to(model.device)
    output = model.generate(
        **inputs,
        max_new_tokens=1024,
        do_sample=False,
        temperature=0.7,
        top_p=0.95,
    )
    summary = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    return {
        "id": "chatcmpl-summary",
        "object": "chat.completion",
        "choices": [
            {"index": 0, "message": {"role": "assistant", "content": summary}, "finish_reason": "stop"}
        ],
        "model": "qwen3-14b"
    }

# 📦 本地运行入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("inference:app", host="0.0.0.0", port=7000, reload=False)
