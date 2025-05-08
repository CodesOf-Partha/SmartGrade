# SmartGrade Backend

This is the FastAPI backend for SmartGrade, an AI-powered grading and feedback system for handwritten math worksheets.

## Features
- Accepts worksheet image uploads
- (Mock) OCR extraction of math content
- Grades perimeter questions and provides child-friendly feedback

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn python-multipart sympy openai pillow
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API
- `POST /upload-worksheet/` — Upload an image file, returns extracted text and grading results.

---

Replace the mock OCR with a real OCR pipeline for production use. 

## **Step 1: Install Tesseract and pytesseract**

**On macOS:**
```bash
brew install tesseract
pip install pytesseract
```

**On Ubuntu:**
```bash
sudo apt-get install tesseract-ocr
pip install pytesseract
```

## **Step 2: Update Your Backend Code**

Replace the `mock_ocr` function in `backend/main.py` with a real OCR function using `pytesseract`.

**Here's the code to add/replace:**

```python
import pytesseract

def real_ocr(image_bytes: bytes) -> str:
    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    # Use Tesseract to do OCR
    text = pytesseract.image_to_string(image, lang='eng')
    return text
```

Then, in your `/upload-worksheet/` endpoint, replace:
```python
extracted_text = mock_ocr(image_bytes)
```
with:
```python
extracted_text = real_ocr(image_bytes)
```

## **Step 3: (Optional) Preprocess the Image for Better OCR**

Handwriting OCR works best with clear, high-contrast images. You can preprocess the image using Pillow or OpenCV (e.g., convert to grayscale, increase contrast, binarize).

## **Step 4: Test the Flow**

1. Restart your backend server.
2. Upload a real worksheet image via the frontend.
3. The backend will now extract the actual text from the image and send it to OpenAI for grading.

## **Summary of Code Changes**

- Install Tesseract and `pytesseract`.
- Replace the mock OCR function with a real one.
- Use the real OCR function in your upload endpoint.

---

Would you like me to make the code changes for you? If so, please confirm your OS (macOS, Ubuntu, Windows) so I can give you the exact install command for Tesseract! 