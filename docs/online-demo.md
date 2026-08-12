# Online Demo

The online demo uses Gradio and reuses the same local conversion code as the desktop and CLI tools.

## Local Run

```powershell
python -m pip install -r requirements-demo.txt
python demo_app.py
```

Open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

## Features

- Upload one audio file
- Choose a preset
- Adjust semitones
- Preview and download the output

## Privacy Notice

The online demo processes uploaded audio on the server. Do not upload private, sensitive, or unauthorized audio.

## Hugging Face Spaces

For Hugging Face Spaces, create a Gradio Space and include:

- `demo_app.py`
- `requirements-demo.txt`
- `src/`
- `pyproject.toml`

For a Space repository, Hugging Face commonly expects:

- `app.py`
- `requirements.txt`

So copy `demo_app.py` to `app.py`, and copy `requirements-demo.txt` to `requirements.txt` inside the Space repository.
