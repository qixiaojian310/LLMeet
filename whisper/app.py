# app.py
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger

# 直接引入你之前写好的函数
from speech_brain_test import extract_and_diarize_transcribe

app = FastAPI(title="Audio Diarization & Transcription API")

# 如果前端跨域调用需要打开 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # 或者指定你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscribeResponse(BaseModel):
    language: str
    segments: List[dict]

@app.post(
    "/transcribe",
    response_model=TranscribeResponse,
    summary="上传多段 MP4，返回带说话人标签的转写结果"
)
async def transcribe_endpoint(
    files: List[UploadFile] = File(..., description="多段 MP4 文件"),
    num_speakers: Optional[int] = Form(None, description="可选的说话人数（用于指导分离）"),
):
    # 创建临时目录，保存上传的文件
    tmpdir = tempfile.mkdtemp(prefix="transcribe_")
    try:
        saved = []
        for f in files:
            # 只接收 .mp4
            if not f.filename.lower().endswith(".mp4"):
                raise HTTPException(400, f"不支持的文件格式：{f.filename}")
            dst = os.path.join(tmpdir, f.filename)
            contents = await f.read()
            with open(dst, "wb") as wf:
                wf.write(contents)
            saved.append(dst)

        logger.info(f"Saved {len(saved)} files to {tmpdir}")

        # 调用你现有的主流程
        result = extract_and_diarize_transcribe(
            mp4_dir=tmpdir,
            whisper_model="medium",
            whisper_cache="/root/autodl-tmp/whisper_model",
            num_speakers=num_speakers
        )

        return result

    except HTTPException:
        # 直接抛出的 4xx
        raise
    except Exception as e:
        logger.error(f"转写失败: {e}", exc_info=True)
        raise HTTPException(500, detail="内部服务器错误，请查看日志") from e
    finally:
        # 清理临时目录
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=6006,
        reload=True, 
        # 请确保已安装 websockets/wsproto via `pip install "uvicorn[standard]"`
    )
