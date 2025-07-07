import os
import cv2
import pytesseract
from pdf2image import convert_from_path

# ✅ 1. Path to your RHMD PDF
pdf_path = "January-March-2022.pdf"  # Ensure this file is in the same folder as this script

# ✅ 2. Set Tesseract path (where tesseract.exe is installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ 3. Set Poppler path (where pdfinfo.exe & pdftoppm.exe are located)
poppler_path = r"C:\poppler-24.08.0\Library\bin"

# ✅ 4. Output file name
output_text_path = "ocr_output_rhmd.txt"

# ✅ 5. Convert PDF pages to images
print("📄 Converting PDF pages to images...")
pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

# ✅ 6. Process and OCR each page
print("🔍 Running OCR on each page...")
extracted_text = []

# Skip first 4 pages (title, index) and start from page 5
for i, page in enumerate(pages[4:]):
    image_name = f"rhmd_page_{i+5}.png"
    page.save(image_name, "PNG")

    # 🧠 Preprocess image for better OCR accuracy
    img = cv2.imread(image_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 🧠 OCR extract using Tesseract
    text = pytesseract.image_to_string(blur)
    extracted_text.append(text)

    print(f"✅ Page {i+5} processed.")

# ✅ 7. Save OCR result to text file
with open(output_text_path, "w", encoding="utf-8") as f:
    f.write("\n\n".join(extracted_text))

print(f"🎯 OCR complete. Output saved to: {output_text_path}")
