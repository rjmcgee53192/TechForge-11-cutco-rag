import pypdf
import os

pdf_path = r"c:\Users\rjmcg\OneDrive\Desktop\Portfolio-Blitz-2026\projects\11-techforge-rag\data\wellness_industrial equipments.pdf"
output_path = r"c:\Users\rjmcg\OneDrive\Desktop\Portfolio-Blitz-2026\projects\11-techforge-rag\data\raw_dump.txt"

try:
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extraction complete. Saved to {output_path}")
except Exception as e:
    print(f"Error during extraction: {e}")
