import pdfplumber
import pandas as pd
import camelot

def extract_pdf_content(pdf_path):
    all_text = []
    all_tables = []
    all_objects = []

    print("[INFO] Starting extraction with pdfplumber + Camelot...")

    # 1️⃣ Extract text and objects using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        print(f"[DEBUG] Total pages detected: {len(pdf.pages)}")

        for page_number, page in enumerate(pdf.pages, start=1):
            print(f"[DEBUG] Processing page {page_number}...")

            # --- Text extraction ---
            text = page.extract_text()
            if text:
                all_text.append(text)
                print(f"[DEBUG] Text extracted from page {page_number} ({len(text)} chars)")

            # --- Objects extraction ---
            all_objects.append({
                "page": page_number,
                "object": page.objects
            })

    # 2️⃣ Extract tables using Camelot
    print("[DEBUG] Starting table extraction with Camelot...")
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")  # try lattice first
        print(f"[DEBUG] Camelot found {tables.n} table(s).")

        for t in tables:
            df = t.df
            if not df.empty:
                all_tables.append({
                    "page": t.page,
                    "table": df
                })
    except Exception as e:
        print(f"[WARNING] Camelot extraction failed: {e}")

    print("[INFO] Extraction complete.")
    print(f"Pages with text: {len(all_text)}")
    print(f"Tables extracted: {len(all_tables)}")
    print(f"Objects extracted: {len(all_objects)}")

    return {
        "text": all_text,
        "tables": all_tables,
        "objects": all_objects
    }
