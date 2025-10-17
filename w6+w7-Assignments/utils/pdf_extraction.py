from docling.document_converter import DocumentConverter
import pandas as pd
import os

# === CONFIG ===
pdf_path = "C:/Users/umair/Desktop/Misc/Final Year Project Proposal/FYP Proposal (AI Surveillance System).pdf"
output_folder = "extracted_output"
os.makedirs(output_folder, exist_ok=True)

# === CONVERT PDF ===
converter = DocumentConverter()
result = converter.convert(pdf_path)
doc = result.document

# === 1. Save extracted text ===
text_path = os.path.join(output_folder, "extracted_text.txt")
with open(text_path, "w", encoding="utf-8") as f:
    f.write("\n".join(getattr(t, "text", str(t)) for t in doc.texts))
print(f"✅ Text content saved to {text_path}")

# === 2. Extract tables and export to CSV ===
for i, table in enumerate(doc.tables, start=1):
    df = table.export_to_dataframe()
    caption = getattr(table, "caption_text", "")
    
    csv_path = os.path.join(output_folder, f"table_{i}.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ Table {i} exported to {csv_path}")
    
    if caption:
        print(f"   Caption: {caption}")

# === 3. Extract pictures/images ===
for i, picture in enumerate(doc.pictures, start=1):
    image_obj = getattr(picture, "image", None)
    if image_obj and hasattr(image_obj, "png_bytes") and image_obj.png_bytes:
        img_path = os.path.join(output_folder, f"picture_{i}.png")
        with open(img_path, "wb") as f:
            f.write(image_obj.png_bytes)
        print(f"✅ Picture {i} saved as {img_path}")
    else:
        print(f"⚠️ Picture {i} skipped — no image data found.")
    
    caption = getattr(picture, "caption_text", None)
    if caption:
        print(f"   Caption: {caption}")
    else:
        print("   Caption: (none)")
