from utils.pdf_extraction import extract_pdf_content

pdf_path = "C:/Users/umair/Desktop/Misc/Final Year Project Proposal/FYP Proposal (AI Surveillance System).pdf"

print("[INFO] Starting extraction...")
data = extract_pdf_content(pdf_path)
print("[INFO] Extraction complete!\n")

# Check what came out
print(f"Pages with text: {len(data['text'])}")
print(f"Tables extracted: {len(data['tables'])}")
print(f"Objects found: {len(data['objects'])}\n")

# Preview a sample text and table
if data['text']:
    print("----- Sample Text (Page 1) -----")
    print(data['text'][0][:500])  # first 500 chars
    print()

if data['tables']:
    print("----- Sample Table (First Page Found) -----")
    table_info = data['tables'][0]
    print(f"Page: {table_info['page']}")
    print(table_info['table'].head())  # first few rows
