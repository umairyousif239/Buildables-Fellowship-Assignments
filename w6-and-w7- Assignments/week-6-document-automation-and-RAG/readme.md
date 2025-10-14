### 🧩 Dependencies

This project uses:
- `pdfplumber` for text and object extraction.
- `Camelot` for structured table extraction.

### ⚙️ Requirements

To use Camelot:
1. Install Ghostscript on your system.
   - **Windows:** Download from https://ghostscript.com/releases/gsdnld.html
   - **Linux/macOS:** Use your package manager, e.g.  
     `sudo apt install ghostscript` or `brew install ghostscript`

2. Install the Python dependencies:
   ```bash
   pip install camelot-py pdfplumber pandas
