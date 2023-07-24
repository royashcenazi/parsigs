import pytesseract
from PIL import Image

def image_to_text(image_path, lang='eng'):
    """
    Extracts text from an image using pytesseract.

    Parameters:
        image_path (str): Path to the image file.
        lang (str): Language code (ISO 639-3) for the desired language. Default is 'eng' (English).

    Returns:
        str: The extracted text from the image.
    """
    try:
        # Open the image using PIL (Python Imaging Library)
        image = Image.open(image_path)

        # Use pytesseract to extract text from the image with the specified language
        extracted_text = pytesseract.image_to_string(image, lang=lang)

        return extracted_text
    except Exception as e:
        print(f"Error: {e}")
        return None
