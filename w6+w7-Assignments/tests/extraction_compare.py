import os, re, json
from utils.pdf_extraction import extract_with_docling

def extract_with_pypdf2(pdf_path):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    return "\n".join([(p.extract_text() or "") for p in reader.pages])

def extract_with_pdfplumber(pdf_path):
    import pdfplumber
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return "\n".join(texts)

def _norm(s): return re.sub(r"\s+", " ", (s or "")).strip().lower()
def _stats(t): 
    n=_norm(t); 
    return {"words": len(n.split()), "chars": len(n), "lines": (t or "").count("\n")+1}
def _overlap(a,b):
    A=set(_norm(a).split()); B=set(_norm(b).split())
    inter=A & B; uni=A | B
    return {"overlap_words": len(inter), "jaccard": (len(inter)/len(uni)) if uni else 0.0}

def run_compare(pdf_path):
    txt_pypdf2 = extract_with_pypdf2(pdf_path)
    txt_pdfplumber = extract_with_pdfplumber(pdf_path)
    docling = extract_with_docling(pdf_path)
    txt_docling = "\n".join(docling.get("texts", []))
    engines = {
        "PyPDF2": {"stats": _stats(txt_pypdf2), "sample": txt_pypdf2[:1200]},
        "pdfplumber": {"stats": _stats(txt_pdfplumber), "sample": txt_pdfplumber[:1200]},
        "Docling": {"stats": _stats(txt_docling), "sample": txt_docling[:1200]},
    }
    overlaps = {
        "PyPDF2_vs_pdfplumber": _overlap(txt_pypdf2, txt_pdfplumber),
        "PyPDF2_vs_Docling": _overlap(txt_pypdf2, txt_docling),
        "pdfplumber_vs_Docling": _overlap(txt_pdfplumber, txt_docling),
    }
    return {"pdf": os.path.basename(pdf_path), "engines": engines, "overlaps": overlaps}

def save_reports(data, md_path, json_path):
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(data, jf, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write(f"# Extraction Comparison: {data['pdf']}\n\n")
        mf.write("| Engine | Words | Chars | Lines |\n|---|---:|---:|---:|\n")
        for k in ["PyPDF2", "pdfplumber", "Docling"]:
            s = data["engines"][k]["stats"]
            mf.write(f"| {k} | {s['words']} | {s['chars']} | {s['lines']} |\n")
        mf.write("\n## Pairwise Overlaps\n\n| Pair | Overlap Words | Jaccard |\n|---|---:|---:|\n")
        for k, v in data["overlaps"].items():
            mf.write(f"| {k} | {v['overlap_words']} | {v['jaccard']:.3f} |\n")