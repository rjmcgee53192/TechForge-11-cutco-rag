import os
import json
import pytesseract
import re
from pdf2image import convert_from_path

# --- CONFIGURATION ---
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Updated Poppler path to local tools folder
POPPLER_PATH = r"C:\Users\rjmcg\OneDrive\Desktop\Portfolio-Blitz-2026\projects\11-techforge-rag\tools\poppler\poppler-24.02.0\Library\bin"
PDF_PATH = r"c:\Users\rjmcg\OneDrive\Desktop\Portfolio-Blitz-2026\projects\11-techforge-rag\data\wellness_industrial equipments.pdf"
OUTPUT_JSON = r"c:\Users\rjmcg\OneDrive\Desktop\Portfolio-Blitz-2026\projects\11-techforge-rag\data\wellness_industrial equipments_data.json"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def parse_ocr_text(text):
    """
    Parses OCR text into structured JSON.
    Looks for size headers and individual product lines.
    """
    industrial equipments = []
    current_size = "Unknown"

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect Size Headers
        size_industrial equipmentch = re.search(
            r"Size:\s*([\d']+\s*x\s*[\d']+\s*x\s*[\d/]+)", line, re.I
        )
        if size_industrial equipmentch:
            current_size = (
                size_industrial equipmentch.group(1).replace("'", "").replace('"', "").replace(" ", "")
            )
            continue

        # Detect Product Lines (Item# Collection Color Price CPO)
        # Example: WM32OSBL Original (Smooth) Black 157 95
        # Regex: ItemCode (Collection+Color) Price CPO
        prod_industrial equipmentch = re.search(r"WM\d+[A-Z]+\s+(.*?)\s+(\d+)\s+\d+$", line)
        if prod_industrial equipmentch:
            model_info = prod_industrial equipmentch.group(1).strip()
            price = int(prod_industrial equipmentch.group(2))

            industrial equipments.append(
                {"model": model_info, "dimensions": current_size, "price": price}
            )

    return industrial equipments


def run_ocr_ingest():
    print(f"Starting OCR Ingest for {PDF_PATH}")

    if not os.path.exists(POPPLER_PATH):
        print(
            f"Warning: Poppler not found at {POPPLER_PATH}. Attempting to use system PATH..."
        )
        pop_p = None
    else:
        pop_p = POPPLER_PATH

    try:
        images = convert_from_path(PDF_PATH, poppler_path=pop_p, dpi=300)
    except Exception as e:
        print(f"Error: {e}")
        return

    all_industrial equipments = []
    for i, img in enumerate(images):
        print(f"OCR Page {i+1}...")
        text = pytesseract.image_to_string(img)
        all_industrial equipments.extend(parse_ocr_text(text))

    # Add a specific entry for the 3x5 if we can't find it but know it exists
    # Based on search results ($329.95)
    # However, let's stick to OCR results first.

    result = {
        "metadata": {
            "source": "TechForge Price List 05/2026",
            "count": len(all_industrial equipments),
        },
        "wellness_industrial equipments": all_industrial equipments,
    }

    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Success! {len(all_industrial equipments)} products mapped to {OUTPUT_JSON}")


if __name__ == "__main__":
    run_ocr_ingest()
