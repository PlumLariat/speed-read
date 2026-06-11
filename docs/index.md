---
icon: lucide/rocket
---

# Speed Read

A desktop speed-reading app that displays text one word at a time at a configurable pace. Accepts plain-text files directly, or PDF files — which are processed through OCR and cleaned up with Gemini AI before reading.

## Requirements

- Python 3.13+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system
- [Poppler](https://poppler.freedesktop.org/) installed on your system (required for PDF conversion)
- A Gemini API key (only needed for PDF imports)

## Installation

```bash
git clone https://github.com/plumlariat/speed-read
cd speed-read
uv sync
```

Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

## Running the app

```bash
uv run main.py
```

## Usage

**Opening a file**

Use **File → Open** or press ++ctrl+o++ to open a `.txt` or `.pdf` file.

- `.txt` files are loaded directly.
- `.pdf` files are run through Tesseract OCR and then cleaned up by Gemini AI. The cleaned text is saved as a timestamped `.txt` file in the project root, then loaded for reading.

**Playback controls**

| Action | How |
|---|---|
| Play | Click **Play** or press ++space++ |
| Pause | Click **Pause** or press ++space++ |
| Adjust speed | Use the **Words/Minute** spinner |

The progress bar at the bottom tracks position through the document. When the end is reached, pressing Play again restarts from the beginning.
