import os, json
from docling.document_converter import DocumentConverter

def extract_with_docling(pdf_path):
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    doc = result.document
    texts = [getattr(t, "text", str(t)) for t in getattr(doc, "texts", [])]
    tables = []
    try:
        for table in getattr(doc, "tables", []):
            df = table.export_to_dataframe()
            tables.append(df.astype(str).to_dict(orient="records"))
    except Exception:
        pass
    pictures = []
    return {"source_pdf": os.path.basename(pdf_path), "texts": texts, "tables": tables, "pictures": pictures}

def save_extraction(pdf_path, out_json):
    data = extract_with_docling(pdf_path)
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_json