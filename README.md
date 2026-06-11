# Speed Read

A desktop speed-reading app that displays text one word at a time at a configurable pace. Accepts plain-text files directly, or PDFs — which are processed through OCR and cleaned up with Gemini AI before reading.

## Requirements

- Python 3.13+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](https://poppler.freedesktop.org/)
- A Gemini API key (PDF imports only)

## Installation

```bash
git clone https://github.com/plumlariat/speed-read
cd speed-read
uv sync
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
```

## Running

```bash
uv run main.py
```

## Docs

Full documentation at [plumlariat.github.io/speed-read](https://plumlariat.github.io/speed-read)
