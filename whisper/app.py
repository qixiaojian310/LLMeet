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

from speech_brain_test import extract_and_diarize_transcribe_and_visualize

app = FastAPI(title="Audio Diarization & Transcription API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscribeResponse(BaseModel):
    language: str
    segments: List[dict]
    video_summarization: str

@app.post(
    "/transcribe",
    response_model=TranscribeResponse,
    summary="上传多段 MP4，返回带说话人标签的转写结果"
)
async def transcribe_endpoint(
    files: List[UploadFile] = File(..., description="多段 MP4 文件"),
    num_speakers: Optional[int] = Form(None, description="可选的说话人数（用于指导分离）"),
):
    tmpdir = tempfile.mkdtemp(prefix="transcribe_")
    try:
        saved = []
        for f in files:
            if not f.filename.lower().endswith(".mp4"):
                raise HTTPException(400, f"不支持的文件格式：{f.filename}")
            dst = os.path.join(tmpdir, f.filename)
            contents = await f.read()
            with open(dst, "wb") as wf:
                wf.write(contents)
            saved.append(dst)

        logger.info(f"Saved {len(saved)} files to {tmpdir}")

        result = extract_and_diarize_transcribe_and_visualize(
            mp4_dir=tmpdir,
            whisper_model="medium",
            whisper_cache="/root/autodl-tmp/whisper_model",
            num_speakers=num_speakers
        )
        logger.info(result)

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"转写失败: {e}", exc_info=True)
        raise HTTPException(500, detail="内部服务器错误，请查看日志") from e
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=6006,
        reload=True, 
    )
