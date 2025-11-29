# OCR Document Verification Setup

## Prerequisites

### 1. Install Tesseract OCR

#### Windows:
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (e.g., `tesseract-ocr-w64-setup-v5.3.0.20221214.exe`)
3. During installation, note the installation path (default: `C:\Program Files\Tesseract-OCR`)
4. Add Tesseract to system PATH or update `document_verifier.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

#### macOS:
```bash
brew install tesseract
```

### 2. Install Poppler (for PDF support)

#### Windows:
1. Download Poppler for Windows: http://blog.alivate.com.au/poppler-windows/
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to system PATH

#### Linux (Ubuntu/Debian):
```bash
sudo apt install poppler-utils
```

#### macOS:
```bash
brew install poppler
```

## Python Dependencies Installation

```bash
cd C:\Users\ruchi\Documents\task\task_Backend
.\env\Scripts\Activate.ps1
pip install pytesseract Pillow pdf2image
```

## Verification

Test if Tesseract is working:

```python
import pytesseract
from PIL import Image

# Test Tesseract
print(pytesseract.get_tesseract_version())

# Test OCR
img = Image.new('RGB', (200, 100), color='white')
text = pytesseract.image_to_string(img)
print("OCR working!")
```

## How It Works

1. **Document Upload**: User uploads PAN/Aadhaar card (PDF, PNG, JPEG, etc.)
2. **OCR Extraction**: System extracts text from the document using Tesseract
3. **Name Extraction**: AI extracts the name from the OCR text
4. **Name Matching**: System compares extracted name with candidate's registered name
5. **Verification**:
   - **Pass**: Name similarity >= 60% (configurable)
   - **Verification Failed**: Name similarity < 60%

## Database Schema

```sql
CREATE TABLE submitted_documents (
    id INTEGER PRIMARY KEY,
    candidate_id INTEGER,
    document_type TEXT,  -- 'PAN Card' or 'Aadhaar Card'
    file_path TEXT,
    submission_date TIMESTAMP,
    verification_status TEXT,  -- 'Pass' or 'Verification Failed'
    extracted_name TEXT,  -- Name extracted from document
    similarity_score REAL,  -- 0.0 to 1.0
    verification_reason TEXT  -- Explanation
);
```

## API Response Example

```json
{
  "message": "Documents uploaded and verified successfully",
  "documents": [
    {
      "type": "PAN Card",
      "filename": "pan_card_1_file.jpg",
      "size": 245678,
      "verification_status": "Pass",
      "extracted_name": "JOHN DOE",
      "similarity_score": 0.95
    },
    {
      "type": "Aadhaar Card",
      "filename": "aadhaar_card_1_file.jpg",
      "size": 189456,
      "verification_status": "Verification Failed",
      "extracted_name": "Jane Smith",
      "similarity_score": 0.35
    }
  ],
  "overall_status": "Verification Failed"
}
```

## Adjusting Verification Threshold

In `app.py`, modify the threshold parameter:

```python
verification_result = doc_verifier.verify_document(
    filepath, 
    'PAN Card', 
    candidate_name,
    threshold=0.6  # Change this (0.0 to 1.0)
)
```

## Troubleshooting

### Error: "TesseractNotFoundError"
- Solution: Install Tesseract and set the path in `document_verifier.py`

### Error: "Unable to get page count"
- Solution: Install Poppler and add to system PATH

### Low Accuracy
- Ensure document images are clear and high resolution
- Try preprocessing images (contrast enhancement, noise reduction)
- Adjust similarity threshold

### Name Not Extracted
- Document format may be non-standard
- Try with different document images
- Check logs for extracted text to debug patterns
