# File Uploader

A simple Streamlit-based file upload dashboard that:

- Accepts file uploads with a visible upload progress bar
- Stores uploaded files in a local `uploads/` folder
- Preserves metadata for retrieval anytime
- Allows browsing and downloading previously uploaded files

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Open the URL shown in the terminal to use the uploader.

## Notes

- Uploaded files are saved into `uploads/`.
- Metadata is stored in `uploads/metadata.json`.
- `uploads/` is ignored by Git so your stored files remain local.
