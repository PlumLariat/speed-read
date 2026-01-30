from google import genai
from dotenv import load_dotenv
import os
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import pytesseract
from datetime import datetime

# Use tesseract to grab as much text data as possible from pdf
def extract(pdf_filepath: str) -> str:
    images = convert_from_path(pdf_filepath)

    page_out_list = []

    for image in images:
        page_out_list.append(pytesseract.image_to_string(image))

    return " ".join(page_out_list)


def gemini_reconstruction(tesseract_str: str) -> None:
    '''
    This function is the second step in extracting text data from a pdf of a textbook. This step hopes to
    scrub away some of the OCR artifacts that are left behind when tessaract does its first pass.
    Function sends that data with a prompt that trys to reconstruct and clean up output.

    Output is in the form of an text file that is created in the root dir distinguised by its timestamp.
    
    :param tesseract_str: String generated via tesseract in the previous step.
    :type tesseract_str: str
    '''
    load_dotenv()
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Filter out any nonsensical artifacts. Remove figure descriptions in the output. Remove Bibliographies and attributions. Try to improve structure and flow. Do not summarize, want a one-to-one transcription. No bullet points or emojis or indentation. Raw Text as output only.\n{tesseract_str}"
    )

    with open(f"output_{datetime.now().isoformat()[:10]}.txt", 'x', encoding='utf-8') as file:
        assert response.text is not None
        file.write(response.text)