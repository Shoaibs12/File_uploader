# FileVault & LTX-Video YouTube Shorts Automation Pipeline

This repository contains two main projects:
1. **File Uploader (FileVault):** A simple Streamlit-based file upload dashboard.
2. **LTX-Video Automation:** Scripts to automate the generation of videos using Lightricks' **LTX-Video** model and upload them directly to YouTube as Shorts.

---

## 1. File Uploader (FileVault)

A simple Streamlit-based file upload dashboard that accepts file uploads, stores them in a local `uploads/` folder, preserves metadata, and allows browsing/downloading.

### Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 2. LTX-Video YouTube Shorts Automation Pipeline

Since LTX-Video requires a GPU with at least 16GB VRAM, this guide includes instructions on how to run this pipeline for **free** using cloud platforms.

### Included Scripts

- `generate_video.py`: Uses the Hugging Face `diffusers` library to load the LTX-Video model. It supports both **text-to-video** and **image-to-video** generation, creating an MP4 video optimized for a 16GB VRAM GPU.
- `youtube_uploader.py`: Uses the Google YouTube Data API v3 to upload the generated MP4 video directly to your YouTube channel.

### How to Get Free GPUs

If you do not have a local GPU with 16GB+ VRAM, you can use these free cloud platforms:

1. **Kaggle Notebooks (Highly Recommended):**
   - Offers up to 30 hours per week of dual Nvidia T4 GPUs (16GB VRAM each) completely free.
   - Ideal for running `generate_video.py` stably.
2. **Google Colab (Free Tier):**
   - Provides free access to a single Nvidia T4 GPU. Sessions can time out if left inactive.
3. **GitHub Student Developer Pack:**
   - If you are a student, you can claim the [GitHub Student Developer Pack](https://education.github.com/pack).
   - Provides $200 in DigitalOcean credits and $100 in Azure credits.
   - *Note:* While the credits are free, activating GPU virtual machines on these platforms usually requires adding a valid credit card and occasionally submitting a manual support ticket for a GPU quota increase.

### Setup Instructions

#### 1. Install Dependencies
In your Python environment (or Kaggle/Colab notebook), install the dependencies:
```bash
pip install -r requirements.txt
```

#### 2. Video Generation
To generate a video, run the script.

**For Text-to-Video:**
```bash
python generate_video.py \
    --prompt "A character walking down a neon-lit cyberpunk street, cinematic lighting" \
    --output "my_short.mp4"
```

**For Image-to-Video (with Character Reference):**
```bash
python generate_video.py \
    --image "path/to/character.jpg" \
    --prompt "A character walking down a neon-lit cyberpunk street, cinematic lighting" \
    --output "my_short.mp4"
```

*(Note: Audio generation for LTX-2.3 is natively supported by the base model, but full audio integration within the standard Diffusers pipeline is actively being added by the community. Once updated, Diffusers will allow passing audio conditioning.)*

#### 3. YouTube Upload Automation
To upload the video automatically, you need to set up the YouTube API:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new Project and enable the **YouTube Data API v3**.
3. Go to Credentials, create an **OAuth 2.0 Client ID** (Desktop Application).
4. Download the JSON file and rename it to `client_secrets.json`. Place it in the same directory as the script.
5. Run the upload script:
```bash
python youtube_uploader.py \
    --file "my_short.mp4" \
    --title "Neon Cyberpunk Walk #Shorts" \
    --description "Generated using LTX-Video AI. #Shorts #AI" \
    --privacy "private"
```
*(The first time you run this, a browser window will open asking you to authenticate with your YouTube account).*
