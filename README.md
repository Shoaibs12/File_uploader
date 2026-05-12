# LTX-Video YouTube Shorts Automation Pipeline

This repository contains scripts to automate the generation of videos using Lightricks' **LTX-Video** model and upload them directly to YouTube as Shorts.

Since LTX-Video requires a GPU with at least 16GB VRAM, this guide focuses on running this pipeline for **free** using cloud platforms like Kaggle Notebooks.

## Included Scripts

- `generate_video.py`: Uses the Hugging Face `diffusers` library to load the LTX-Video model. It supports both **text-to-video** and **image-to-video** generation, creating an MP4 video optimized for a 16GB VRAM GPU.
- `youtube_uploader.py`: Uses the Google YouTube Data API v3 to upload the generated MP4 video directly to your YouTube channel.
- `kaggle_notebook.ipynb`: A ready-to-run Jupyter notebook configured for Kaggle.

## How to Get Free GPUs

1. **Kaggle Notebooks (Highly Recommended):**
   - Offers up to 30 hours per week of dual Nvidia T4 GPUs (16GB VRAM each) completely free.
   - Ideal for running `generate_video.py` stably. We provide `kaggle_notebook.ipynb` specifically for this!
2. **GitHub Student Developer Pack:**
   - If you are a student, you can claim the [GitHub Student Developer Pack](https://education.github.com/pack).
   - Provides $200 in DigitalOcean credits and $100 in Azure credits.

## Setup Instructions (For Kaggle Notebooks)

Because Kaggle is a headless cloud environment, you cannot complete the YouTube browser authentication pop-up there. You must generate an authentication token locally first.

### Step 1: Generate `token.json` Locally
1. Install dependencies on your local computer: `pip install google-api-python-client google-auth-oauthlib google-auth-httplib2`
2. Go to the [Google Cloud Console](https://console.cloud.google.com/).
3. Create a new Project and enable the **YouTube Data API v3**.
4. Go to Credentials, create an **OAuth 2.0 Client ID** (Desktop Application).
5. Download the JSON file and rename it to `client_secrets.json`. Place it in the same directory as the script.
6. Run the uploader script locally once to trigger the login:
   ```bash
   python youtube_uploader.py --file "dummy.mp4" --title "Test"
   ```
7. A browser window will open. Log into your YouTube account and grant permissions.
8. This will create a `token.json` file in your directory.

### Step 2: Run in Kaggle
1. Create a new Kaggle Notebook and import this GitHub repository.
2. Under "Session Options" in Kaggle, set the Accelerator to **GPU T4 x2**.
3. Upload your `token.json` file into the Kaggle working directory.
4. If you are doing Image-to-Video, upload your character reference image.
5. Open `kaggle_notebook.ipynb` and run the cells! It will automatically install dependencies, generate the video, and upload it to YouTube using your token.

## Manual Setup (Local Machine)

If you are running this entirely on your own PC with a 16GB+ GPU:

```bash
pip install -r requirements.txt
```

**Generate Video:**
```bash
python generate_video.py \
    --prompt "A character walking down a neon-lit cyberpunk street, cinematic lighting" \
    --output "my_short.mp4"
```

**Upload to YouTube:**
```bash
python youtube_uploader.py \
    --file "my_short.mp4" \
    --title "Neon Cyberpunk Walk #Shorts" \
    --description "Generated using LTX-Video AI. #Shorts #AI" \
    --privacy "private"
```
