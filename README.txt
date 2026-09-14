SIH PACKCHECK - DESKTOP DEMO APP

What it does:
- Select 1 to 4 photos of the same packaged product.
- Runs OCR with Tesseract.
- Extracts Product Name, MRP, Net Quantity, Date and Manufacturer.
- Gives a preliminary compliance result.
- Shows missing/unclear information and OCR text.

Requirements:
1. Windows
2. Python 3.12
3. Tesseract OCR installed at:
   C:\Program Files\Tesseract-OCR\tesseract.exe
4. Python packages:
   pip install -r requirements.txt

Run:
   python app.py

Or double-click:
   RUN_PACKCHECK.bat

Important:
The result is an AI-assisted preliminary screening, not a legal certification.
For the SIH demo, show:
1. A correctly labelled package -> PRELIMINARY COMPLIANT
2. A package with missing/unclear fields -> NEEDS MANUAL REVIEW
3. Multiple photos (front/back/side) of the same package.
