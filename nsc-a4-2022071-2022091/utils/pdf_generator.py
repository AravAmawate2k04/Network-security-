import os
import io
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from base64 import b64encode
from crypto_utils import generate_keys, sign_data
from ntp_time import get_gmt_datetime
import PyPDF2

COURSES = ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science"]
GRADES = ["A", "B", "C", "D", "E", "F"]
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def _create_signature_page(sig_b64: str) -> io.BytesIO:
    """
    Returns a BytesIO buffer containing a single-page PDF with the signature.
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    w, h = LETTER
    c.setFont("Helvetica-Bold", 10)
    margin_x = 50
    margin_y = 100
    text = c.beginText(margin_x, h - margin_y)
    for i in range(0, len(sig_b64), 80):
        text.textLine(sig_b64[i:i + 80])
    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf


def generate_degree_certificate(user: dict, output_dir: str = "output") -> str:
    output_dir = os.path.join(BASE_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)
    dt_issue = get_gmt_datetime().strftime("%Y-%m-%d %H:%M:%S GMT")
    watermark = f"Login Time: {user['login_time'].strftime('%Y-%m-%d %H:%M:%S GMT')}"

    buf_cert = io.BytesIO()
    c = canvas.Canvas(buf_cert, pagesize=LETTER)
    w, h = LETTER

    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, h - 80, "UNIVERSITY OF INDIA")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w / 2, h - 120, "Official Degree Certificate")

    c.setFont("Helvetica", 14)
    text = c.beginText(100, h - 180)
    text.setLeading(20)
    text.textLine(f"This is to certify that {user['name']},")
    text.textLine(f"Roll Number: {user['roll_number']}, has successfully fulfilled the")
    text.textLine(f"academic requirements set by the {user['college']}.")
    text.textLine(f"Year of Graduation: {user['grad_year']}")
    text.textLine(f"Date of Issue: {dt_issue}")
    c.drawText(text)

    # Smaller watermark
    c.saveState()
    c.setFont("Helvetica", 36)
    c.setFillGray(0.95)
    c.translate(w / 2, h / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, watermark)
    c.restoreState()

    c.showPage()
    c.save()
    buf_cert.seek(0)

    cert_bytes = buf_cert.getvalue()
    generate_keys()
    signature = sign_data(cert_bytes)
    sig_b64 = b64encode(signature).decode()

    buf_sig = _create_signature_page(sig_b64)

    reader_cert = PyPDF2.PdfReader(buf_cert)
    reader_sig = PyPDF2.PdfReader(buf_sig)
    writer = PyPDF2.PdfWriter()
    for p in reader_cert.pages:
        writer.add_page(p)
    for p in reader_sig.pages:
        writer.add_page(p)

    path = os.path.join(output_dir, f"{user['roll_number']}_degree_certificate.pdf")
    with open(path, "wb") as f:
        writer.write(f)
    return path


def generate_grade_report(user: dict, output_dir: str = "output") -> str:
    output_dir = os.path.join(BASE_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)
    dt_issue = get_gmt_datetime().strftime("%Y-%m-%d %H:%M:%S GMT")
    watermark = f"Login Time: {user['login_time'].strftime('%Y-%m-%d %H:%M:%S GMT')}"

    grades = {course: random.choice(GRADES) for course in COURSES}

    buf_report = io.BytesIO()
    c = canvas.Canvas(buf_report, pagesize=LETTER)
    w, h = LETTER

    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, h - 80, "UNIVERSITY OF EXCELLENCE")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w / 2, h - 120, "Official Grade Report")

    c.setFont("Helvetica", 14)
    text = c.beginText(100, h - 180)
    text.setLeading(20)
    text.textLine(f"Name: {user['name']}")
    text.textLine(f"Roll Number: {user['roll_number']}")
    text.textLine(f"Year of Graduation: {user['grad_year']}")
    text.textLine(f"Date of Issue: {dt_issue}")
    text.textLine("")
    text.textLine("Courses and Grades:")
    for course, grade in grades.items():
        text.textLine(f"  {course}: {grade}")
    c.drawText(text)

    c.saveState()
    c.setFont("Helvetica", 36)
    c.setFillGray(0.95)
    c.translate(w / 2, h / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, watermark)
    c.restoreState()

    c.showPage()
    c.save()
    buf_report.seek(0)

    report_bytes = buf_report.getvalue()
    generate_keys()
    signature = sign_data(report_bytes)
    sig_b64 = b64encode(signature).decode()

    buf_sig = _create_signature_page(sig_b64)

    reader_report = PyPDF2.PdfReader(buf_report)
    reader_sig = PyPDF2.PdfReader(buf_sig)
    writer = PyPDF2.PdfWriter()
    for p in reader_report.pages:
        writer.add_page(p)
    for p in reader_sig.pages:
        writer.add_page(p)

    path = os.path.join(output_dir, f"{user['roll_number']}_grade_report.pdf")
    with open(path, "wb") as f:
        writer.write(f)
    return path


# if __name__ == "__main__":
#     import datetime

#     test_user = {
#         "name": "Alice Johnson",
#         "roll_number": "2022CS101",
#         "college": "School of Computer Science",
#         "grad_year": 2025,
#         "login_time": datetime.datetime.utcnow()
#     }

#     print("Generating degree certificate...")
#     degree_path = generate_degree_certificate(test_user)
#     print(f"Degree certificate saved at: {degree_path}")

#     print("Generating grade report...")
#     report_path = generate_grade_report(test_user)
#     print(f"Grade report saved at: {report_path}")
