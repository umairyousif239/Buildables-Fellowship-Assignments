from utils.pdf_extraction_and_structure import extract_pdf_content

pdf_path = "C:/Users/umair/Desktop/Misc/Final Year Project Proposal/FYP Proposal (AI Surveillance System).pdf"
data = extract_pdf_content(pdf_path)

print("Total pages with text:", len(data["text"]))
print("Total tables extracted:", len(data["tables"]))
print("Objects metadata for first page:", data["objects"][0])

# Example: View a table
if data["tables"]:
    first_table = data["tables"][0]["table"]
    print(first_table.head())
