from fastapi import FastAPI, HTTPException, UploadFile, Form
from pydantic import BaseModel
from typing import Optional
import os
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline import LivePortraitPipeline
import subprocess
import torch

app = FastAPI()


class InferenceRequest(BaseModel):
    source: str
    driving: str
    output_dir: str


def partial_fields(target_class, kwargs):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})


def fast_check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False


def fast_check_args(args: ArgumentConfig):
    if not os.path.exists(args.source):
        raise FileNotFoundError(f"source info not found: {args.source}")
    if not os.path.exists(args.driving):
        raise FileNotFoundError(f"driving info not found: {args.driving}")


def run_inference(source, driving, output_dir):
    try:
        args = ArgumentConfig(source=source, driving=driving, output_dir=output_dir)

        ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
        if os.path.exists(ffmpeg_dir):
            os.environ["PATH"] += (os.pathsep + ffmpeg_dir)

        if not fast_check_ffmpeg():
            raise ImportError("FFmpeg is not installed.")

        fast_check_args(args)

        inference_cfg = partial_fields(InferenceConfig, args.__dict__)
        crop_cfg = partial_fields(CropConfig, args.__dict__)

        live_portrait_pipeline = LivePortraitPipeline(
            inference_cfg=inference_cfg,
            crop_cfg=crop_cfg
        )

        wfp, wfp_concat = live_portrait_pipeline.execute(args)
    except RuntimeError as e:
        print(f"RuntimeError during inference: {e}")
        torch.cuda.empty_cache()
        raise
    return wfp, wfp_concat


@app.post("/generate_video")
async def generate_video(request: InferenceRequest):
    try:
        source = request.source
        driving = request.driving
        output_dir = request.output_dir

        # Run inference
        output_video_path, concatenated_video_path = run_inference(source, driving, output_dir)

        return {
            "message": "Video generation completed",
            "output_video_path": output_video_path,
            "concatenated_video_path": concatenated_video_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
