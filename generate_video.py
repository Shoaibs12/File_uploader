import argparse
import torch
from diffusers import LTXPipeline, LTXImageToVideoPipeline
from diffusers.utils import export_to_video, load_image
import os

def generate_video(prompt, image_path, output_path, num_frames=121, num_inference_steps=40):
    """
    Generates a video from a text prompt (and optionally an image) using LTX-Video.
    Optimized for 16GB VRAM GPUs (e.g., Google Colab / Kaggle T4).
    """

    # Enable memory optimizations for 16GB VRAM
    width, height = 704, 1216

    if image_path and os.path.exists(image_path):
        print(f"Loading LTXImageToVideoPipeline for Image-to-Video generation...")
        # Note: LTX-2.3 diffusers support is emerging. We use the Lightricks/LTX-Video repo.
        pipe = LTXImageToVideoPipeline.from_pretrained(
            "Lightricks/LTX-Video", torch_dtype=torch.bfloat16
        )
        pipe.enable_model_cpu_offload()

        print(f"Loading reference image from {image_path}...")
        image = load_image(image_path)

        print(f"Generating video with prompt: '{prompt}'...")
        video = pipe(
            image=image,
            prompt=prompt,
            negative_prompt="worst quality, inconsistent, blurry, deformed",
            width=width,
            height=height,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps,
        ).frames[0]
    else:
        print(f"Loading LTXPipeline for Text-to-Video generation...")
        pipe = LTXPipeline.from_pretrained(
            "Lightricks/LTX-Video", torch_dtype=torch.bfloat16
        )
        pipe.enable_model_cpu_offload()

        print(f"Generating video with prompt: '{prompt}'...")
        video = pipe(
            prompt=prompt,
            negative_prompt="worst quality, inconsistent, blurry, deformed",
            width=width,
            height=height,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps,
        ).frames[0]

    print(f"Exporting video to {output_path}...")
    # Export to mp4
    export_to_video(video, output_path, fps=24)
    print(f"Video saved to {output_path}")

    # Note on Audio: LTX-2.3 produces synchronized audio natively, but its full open-source Diffusers integration
    # for the joint audio-video pipeline might require using the raw `Lightricks/LTX-2.3` checkpoint
    # and their official github codebase rather than the current standard diffusers pipeline.
    # The LTX-Video pipeline currently focuses on video.


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate video using LTX-Video")
    parser.add_argument("--prompt", type=str, required=True, help="Text prompt for the video action")
    parser.add_argument("--image", type=str, default=None, help="Path to the character reference image (optional)")
    parser.add_argument("--output", type=str, default="output.mp4", help="Output path for the generated mp4")
    parser.add_argument("--frames", type=int, default=121, help="Number of frames to generate")
    parser.add_argument("--steps", type=int, default=40, help="Number of inference steps")

    args = parser.parse_args()

    generate_video(args.prompt, args.image, args.output, args.frames, args.steps)
