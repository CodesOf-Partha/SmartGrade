import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sympy import Eq, symbols, solve
from typing import List
from PIL import Image
import io
import openai
from dotenv import load_dotenv
import pytesseract

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock OCR function (replace with real OCR later)
def mock_ocr(image_bytes: bytes) -> str:
    # For demo, return a fixed string similar to the worksheet
    return "Q1: Perimeter = 5+6+7 = 18 cm\nQ2: Perimeter = 4x4 = 16 cm²\nQ3: Perimeter = 5x3x4 = 60 cm²\nQ4: Object A = 5+5+4 = 14 cm, Object B = 3+3+3 = 9 cm"

def real_ocr(image_bytes: bytes) -> str:
    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    # Use Tesseract to do OCR
    text = pytesseract.image_to_string(image, lang='eng')
    return text

# Reference answers and questions
ground_truth = [
    {
        "question": "Find the perimeter of the following figure (Triangle)",
        "correct": "Perimeter = 5 + 6 + 7 = 18 cm",
    },
    {
        "question": "Find the perimeter of the following figure (Square)",
        "correct": "Perimeter = 4 × side = 4 × 4 = 16 cm",
    },
    {
        "question": "Find the perimeter of the following figure (Cuboid)",
        "correct": "Total edge length = 4 × (5 + 3 + 4) = 4 × 12 = 48 cm",
    },
    {
        "question": "Which object has a larger perimeter?",
        "correct": "Object A: 5 + 5 + 4 = 14 cm, Object B: 3 + 3 + 3 = 9 cm. Object A > Object B",
    },
]

# Use OpenAI to grade each answer
def openai_grade(question, student_answer, correct_answer):
    import openai
    import os
    openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure API key is set for each call
    prompt = f"""
You are a friendly math teacher. Here is a student's answer to a worksheet question.\n
Question: {question}\nStudent's Solution: {student_answer}\nCorrect Solution: {correct_answer}\n
Please:\n- Say if the answer is correct or not.\n- Give a score out of 5.\n- If there are mistakes, explain them simply.\n- Give a child-friendly feedback message.\n- Output in JSON: {{\"score\": x, \"correct\": true/false, \"mistake\": \"...\", \"feedback\": \"...\"}}
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )
    import json
    import re
    # Extract JSON from response
    text = response.choices[0].message.content
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return {"score": 0, "correct": False, "mistake": "Could not parse feedback.", "feedback": "Sorry, something went wrong."}
    else:
        return {"score": 0, "correct": False, "mistake": "No feedback found.", "feedback": "Sorry, something went wrong."}

@app.post("/upload-worksheet/")
async def upload_worksheet(file: UploadFile = File(...)):
    image_bytes = await file.read()
    # For now, use mock OCR
    extracted_text = real_ocr(image_bytes)
    # Split student answers by line
    student_answers = extracted_text.split("\n")
    grading = []
    for i, ans in enumerate(student_answers):
        if i < len(ground_truth):
            g = openai_grade(
                ground_truth[i]["question"],
                ans,
                ground_truth[i]["correct"]
            )
            grading.append({
                "question": i+1,
                "score": g["score"],
                "correct": g["correct"],
                "mistake": g["mistake"],
                "feedback": g["feedback"]
            })
    return JSONResponse({
        "extracted_text": extracted_text,
        "grading": grading
    }) 