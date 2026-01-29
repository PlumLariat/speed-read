
def main():
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

    load_dotenv()
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    images = convert_from_path('assets/Atmosphere_Weather_and_Climate_----_(6_Atmospheric_motion_principles).pdf')

    page_out_list = []
    
    for image in images:
        page_out_list.append(pytesseract.image_to_string(image))

    tess_res = " ".join(page_out_list)

    
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Filter out any nonsensical artifacts. Remove figure descriptions in the output. Remove Bibliographies and attributions. Try to improve structure and flow. Do not summarize, want a one-to-one transcription. No bullet points or emojis or indentation. Raw Text as output only.\n{tess_res}"
    )



    with open(f"output_{datetime.now().isoformat()[:10]}.txt", 'x', encoding='utf-8') as file:
        assert response.text is not None
        file.write(response.text)
    
if __name__ == "__main__":
    main()