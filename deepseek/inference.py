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
        max_seq_length=8192,
        device_map="auto",
    )
    tokenizer = get_chat_template(
        tokenizer,
        chat_template="qwen3",  # 对应 Qwen2 模型
        mapping={"role": "role", "content": "content", "user": "user", "assistant": "assistant"}
    )
    model.eval()
    yield

app = FastAPI(lifespan=lifespan)

# 🔧 将同步迭代器转换为异步生成器
async def _aiter_from_sync(sync_iter):
    for item in sync_iter:
        yield item
        await asyncio.sleep(0)

def build_summarization_messages(segments: List[TranscriptSegment]) -> List[dict]:
    system = {
        "role": "system",
        "content": "你是一个会议摘要助手，会将下面的会议转录生成简洁摘要。"
    }
    text = "\n".join(f"{s.speaker}: {s.text}" for s in segments)
    user = {
        "role": "user",
        "content": text
    }
    return [system, user]

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
            "max_new_tokens": 2048,
            "do_sample": False,
            "temperature": 0.7,
            "top_p": 0.95,
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
                "content": f"以下是会议背景材料，请参考后回答用户提问：\n\n{segment_text}"
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
    
    messages = build_summarization_messages(segments)
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
