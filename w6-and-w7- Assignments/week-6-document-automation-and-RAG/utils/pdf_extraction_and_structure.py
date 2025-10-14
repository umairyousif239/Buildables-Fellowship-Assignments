import pdfplumber
import pandas as pd

pdf_path = "C:/Users/umair/Downloads/BATTLE-AX B850M-PLUS WIFI V14 主板使用手册.pdf"

def extract_pdf_content(pdf_path):
    all_text = []
    all_tables = []
    all_objects = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Text Extraction
            text = page.extract_text()
            if text:
                all_text.append(text)
                
            # Tables Extraction
            tables = page.extract_tables()
            if tables:
                for table_data in tables:
                    # converting tables into Dataframe
                    if len(table_data) > 1:
                        df = pd.DataFrame(table_data[1:], columns=table_data[0])
                        all_tables.append({
                            "page": page_number,
                            "table": df
                        })
            # Objects Extraction
            all_objects.append({
                "page": page_number,
                "object": page.objects
            })
            
    return{
        "text": all_text,
        "tables": all_tables,
        "objects": all_objects
    }