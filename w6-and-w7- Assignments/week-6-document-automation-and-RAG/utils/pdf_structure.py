import os
from utils.pdf_extraction import extract_pdf_content

def get_filename_from_path(path):
    """Extract just the file name from a full path."""
    return os.path.basename(path)

def split_text(text):
    """Split text into smaller blocks for later embedding."""
    if not text:
        return []
    return [block.strip() for block in text.split("\n\n") if block.strip()]

def convert_tables(tables, page_index):
    """Get tables for a given page index (1-based page numbers)."""
    page_tables = []
    if isinstance(tables, list):
        for t in tables:
            if t["page"] == page_index + 1:  # match 1-based page numbering
                df = t["table"]
                if hasattr(df, "columns"):
                    headers = list(df.columns)
                    rows = df.values.tolist()
                    page_tables.append({"headers": headers, "rows": rows})
    return page_tables


def structure_extracted_data(pdf_path):
    raw_data = extract_pdf_content(pdf_path)

    structured = {
        "document_name": get_filename_from_path(pdf_path),
        "pages": []
    }

    total_pages = len(raw_data["text"])  # number of text entries = total pages

    for page_index in range(total_pages):
        page_entry = {
            "page_number": page_index + 1,
            "text_blocks": split_text(raw_data["text"][page_index]),
            "tables": convert_tables(raw_data["tables"], page_index)
        }
        structured["pages"].append(page_entry)
    return structured
