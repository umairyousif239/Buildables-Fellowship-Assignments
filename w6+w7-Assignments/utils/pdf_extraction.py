from docling.document_converter import DocumentConverter
import os
import base64
import json

# === CONFIG ===
pdf_path = "C:/Users/umair/Desktop/Misc/Final Year Project Proposal/FYP Proposal (AI Surveillance System).pdf"
output_folder = "extracted_output"
os.makedirs(output_folder, exist_ok=True)

# === CONVERT PDF ===
converter = DocumentConverter()
result = converter.convert(pdf_path)
doc = result.document

# === 1. Extract text ===
texts = [getattr(t, "text", str(t)) for t in doc.texts]

# === 2. Extract tables ===
tables = []
for i, table in enumerate(doc.tables, start=1):
    df = table.export_to_dataframe()

    # --- Safely extract caption ---
    caption = ""
    try:
        if hasattr(table, "caption_text") and callable(table.caption_text):
            caption = table.caption_text() or ""
        elif hasattr(table, "captions") and table.captions:
            caption = " ".join(c.text for c in table.captions if hasattr(c, "text"))
    except Exception:
        caption = "(no caption)"

    tables.append({
        "table_number": i,
        "caption": caption.strip(),
        "columns": list(map(str, df.columns.tolist())),
        "data": df.astype(str).to_dict(orient="records")
    })

# === 3. Extract pictures ===
pictures = []
for i, picture in enumerate(doc.pictures, start=1):
    # --- Safely extract caption ---
    caption = ""
    try:
        if hasattr(picture, "caption_text") and callable(picture.caption_text):
            caption = picture.caption_text() or ""
        elif hasattr(picture, "captions") and picture.captions:
            caption = " ".join(c.text for c in picture.captions if hasattr(c, "text"))
    except Exception:
        caption = "(no caption)"

    # --- Encode image if available ---
    img_b64 = None
    if getattr(picture, "image", None) and getattr(picture.image, "png_bytes", None):
        img_b64 = base64.b64encode(picture.image.png_bytes).decode("utf-8")

    pictures.append({
        "picture_number": i,
        "caption": caption.strip(),
        "image_base64": img_b64 or "(no image data)"
    })

# === 4. Combine everything into one JSON ===
combined_data = {
    "source_pdf": os.path.basename(pdf_path),
    "texts": texts,
    "tables": tables,
    "pictures": pictures
}

# === 5. Save to JSON ===
json_path = os.path.join(output_folder, "extracted_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)

print(f"✅ Combined JSON saved to {json_path}")
print(f"   - Text sections: {len(texts)}")
print(f"   - Tables: {len(tables)}")
print(f"   - Pictures: {len(pictures)}")
