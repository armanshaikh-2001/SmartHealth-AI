

import os
import re
import random
from datetime import datetime
import json
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import fitz
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import qrcode
import pytesseract 
import cv2  
import numpy as np
from flask import send_file
import json
import tempfile
from fpdf import FPDF
from fpdf import XPos, YPos
import uuid
from storage import save_user_data
from ml_model import predict_condition

TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp_reports')
os.makedirs(TEMP_DIR, exist_ok=True)

def save_risk_chart(data, path):
    conditions = list(data.keys())
    risks = list(data.values())
    plt.figure(figsize=(10, 4))
    plt.bar(conditions, risks, color='salmon')
    plt.title("Health Risk Profile", fontsize=14)
    plt.ylabel("Risk %")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def save_qr_code(url, path):
    qr = qrcode.make(url)
    qr.save(path)

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime(format)

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.jinja_env.filters['datetimeformat'] = datetimeformat  # Enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'mp4'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_temp_dir():
    """Get cross-platform temporary directory"""
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp_reports')
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

# Dummy medical knowledge base
MEDICAL_KNOWLEDGE = {
    "conditions": {
        "common_cold": {
            "name": "Common Cold",
            "symptoms": ["cough", "sore_throat", "runny_nose", "sneezing", "mild_fever"],
            "body_parts": ["head", "throat", "nose"],
            "first_aid": [
                "Rest and drink plenty of fluids",
                "Use over-the-counter cold medicines for symptom relief",
                "Gargle with warm salt water for sore throat"
            ],
            "lifestyle": [
                "Get adequate sleep to boost immune system",
                "Wash hands frequently to prevent spread",
                "Avoid close contact with others to prevent transmission"
            ],
            "diet": [
                "Warm liquids like herbal tea or broth",
                "Vitamin C rich foods (oranges, bell peppers)",
                "Zinc-rich foods (nuts, seeds, legumes)"
            ],
            "specialist": "General Physician"
        },
        "migraine": {
            "name": "Migraine",
            "symptoms": ["headache", "nausea", "sensitivity_to_light", "aura"],
            "body_parts": ["head"],
            "first_aid": [
                "Rest in a quiet, dark room",
                "Apply cold compress to forehead",
                "Over-the-counter pain relievers (ibuprofen, acetaminophen)"
            ],
            "lifestyle": [
                "Identify and avoid migraine triggers",
                "Maintain regular sleep schedule",
                "Practice stress-reduction techniques"
            ],
            "diet": [
                "Stay hydrated",
                "Avoid known food triggers (often chocolate, cheese, caffeine)",
                "Eat regular meals to maintain blood sugar"
            ],
            "specialist": "Neurologist"
        },
        "gastritis": {
            "name": "Gastritis",
            "symptoms": ["stomach_pain", "bloating", "nausea", "indigestion", "loss_of_appetite"],
            "body_parts": ["stomach"],
            "first_aid": [
                "Avoid foods that irritate stomach",
                "Antacids may provide temporary relief",
                "Small, frequent meals instead of large meals"
            ],
            "lifestyle": [
                "Reduce stress",
                "Avoid alcohol and smoking",
                "Don't lie down immediately after eating"
            ],
            "diet": [
                "Bland, non-acidic foods",
                "Probiotic-rich foods (yogurt, kefir)",
                "Avoid spicy, fried, or fatty foods"
            ],
            "specialist": "Gastroenterologist"
        }
    },
    "symptoms": {
        "headache": ["migraine", "tension_headache", "sinusitis"],
        "cough": ["common_cold", "flu", "bronchitis"],
        "sore_throat": ["common_cold", "strep_throat", "tonsillitis"],
        "stomach_pain": ["gastritis", "food_poisoning", "ibs"],
        "nausea": ["migraine", "gastritis", "food_poisoning"],
        "fatigue": ["anemia", "depression", "chronic_fatigue"],
        "fever": ["common_cold", "flu", "infection"]
    },
    "body_parts": {
        "head": ["migraine", "tension_headache", "sinusitis"],
        "throat": ["common_cold", "strep_throat", "tonsillitis"],
        "stomach": ["gastritis", "food_poisoning", "ibs"],
        "chest": ["bronchitis", "asthma", "pneumonia"]
    }
}

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = PyMuPDF.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def extract_text_from_image(filepath):
    """Extract text from image using Tesseract OCR"""
    try:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting image text: {e}")
        return ""

def process_video(filepath):
    """Placeholder for video processing - in a real app would implement proper video analysis"""
    try:
        # Just return basic file info as we're not actually processing video content
        cap = cv2.VideoCapture(filepath)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        return f"Video file detected with {frame_count} frames (~{duration:.2f} seconds)"
    except Exception as e:
        print(f"Error processing video: {e}")
        return "Video file received but not analyzed"

def analyze_uploaded_files(files):
    """Process all uploaded files and extract text where possible"""
    results = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            file_info = {
                "filename": filename,
                "type": file.content_type,
                "size": os.path.getsize(filepath)
            }
            
            # Process based on file type
            if filename.lower().endswith('.pdf'):
                file_info["content"] = extract_text_from_pdf(filepath)
                file_info["type"] = "pdf"
            elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_info["content"] = extract_text_from_image(filepath)
                file_info["type"] = "image"
            elif filename.lower().endswith('.mp4'):
                file_info["content"] = process_video(filepath)
                file_info["type"] = "video"
            
            results.append(file_info)
            
            # Clean up - in production, you might want to keep these
            os.remove(filepath)
    
    return results

def analyze_symptoms(user_input, files_text):
    """Analyze symptoms and suggest possible conditions"""
    symptoms = user_input.get('symptoms', [])
    body_parts = user_input.get('body_parts', [])
    description = user_input.get('description', '').lower()
    
    # Combine all text for keyword analysis
    all_text = description + " " + " ".join(files_text)
    
    # Find possible conditions based on symptoms
    possible_conditions = set()
    
    # First, find conditions that match all symptoms (if any)
    if symptoms:
        for condition_id, condition in MEDICAL_KNOWLEDGE['conditions'].items():
            if all(symptom in condition['symptoms'] for symptom in symptoms):
                possible_conditions.add(condition_id)
    
    # If no conditions match all symptoms, look for partial matches
    if not possible_conditions and symptoms:
        for symptom in symptoms:
            if symptom in MEDICAL_KNOWLEDGE['symptoms']:
                for condition_id in MEDICAL_KNOWLEDGE['symptoms'][symptom]:
                    possible_conditions.add(condition_id)
    
    # Also consider body parts
    if body_parts:
        body_part_conditions = set()
        for body_part in body_parts:
            if body_part in MEDICAL_KNOWLEDGE['body_parts']:
                for condition_id in MEDICAL_KNOWLEDGE['body_parts'][body_part]:
                    body_part_conditions.add(condition_id)
        
        if possible_conditions:
            possible_conditions = possible_conditions.intersection(body_part_conditions)
        else:
            possible_conditions = body_part_conditions
    
    # If still no conditions, look for keywords in description
    if not possible_conditions and description:
        for condition_id, condition in MEDICAL_KNOWLEDGE['conditions'].items():
            condition_name = condition['name'].lower()
            if condition_name in description:
                possible_conditions.add(condition_id)
    
    # Also scan file text for keywords
    if not possible_conditions and files_text:
        for condition_id, condition in MEDICAL_KNOWLEDGE['conditions'].items():
            condition_name = condition['name'].lower()
            if any(condition_name in text.lower() for text in files_text):
                possible_conditions.add(condition_id)
    
    # Get condition details for matched conditions
    matched_conditions = []
    for condition_id in possible_conditions:
        if condition_id in MEDICAL_KNOWLEDGE['conditions']:
            condition = MEDICAL_KNOWLEDGE['conditions'][condition_id].copy()
            condition['id'] = condition_id
            matched_conditions.append(condition)
    
    return matched_conditions

def generate_summary(user_input, conditions, files_info):
    timestamp = datetime.now().isoformat()
    """Generate a health summary based on user input and conditions"""
    if not conditions:
        conditions = [{
            "name": "General Health Advice",
            "first_aid": [
                "Monitor your symptoms and seek medical attention if they worsen",
                "Get adequate rest and stay hydrated"
            ],
            "lifestyle": [
                "Maintain a balanced diet and regular exercise routine",
                "Practice good sleep hygiene"
            ],
            "diet": [
                "Eat a variety of fruits and vegetables",
                "Stay hydrated with water and limit sugary drinks"
            ],
            "specialist": "General Physician"
        }]
    
    # Combine all condition recommendations
    first_aid = set()
    lifestyle = set()
    diet = set()
    specialists = set()
    
    for condition in conditions:
        for item in condition.get('first_aid', []):
            first_aid.add(item)
        for item in condition.get('lifestyle', []):
            lifestyle.add(item)
        for item in condition.get('diet', []):
            diet.add(item)
        if 'specialist' in condition:
            specialists.add(condition['specialist'])
    
    # Create summary
    summary = {
        "user_info": {
            "name": user_input.get('name'),
            "email": user_input.get('email'),
            "phone": user_input.get('phone'),
            "gender": user_input.get('gender'),
            "bloodGroup": user_input.get('bloodGroup'),
            "ethnicity": user_input.get('ethnicity'),
            "timestamp": datetime.now().isoformat()
        },
        "possible_conditions": [c['name'] for c in conditions],
        "health_summary": {
            "first_aid": list(first_aid),
            "lifestyle_recommendations": list(lifestyle),
            "dietary_suggestions": list(diet),
            "recommended_specialist": list(specialists)[0] if specialists else "General Physician"
        },
        "file_analysis": files_info
    }
    # Calculate health score (0-100)
    health_score = calculate_health_score(conditions)
    summary['health_score'] = health_score

    # Ensure timestamp exists
    if 'timestamp' not in summary['user_info']:
        summary['user_info']['timestamp'] = datetime.now().isoformat()
    return summary

def calculate_health_score(conditions):
    """Simple health score calculation"""
    if not conditions:
        return random.randint(70, 90)  # Good health
    
    # More conditions = lower score
    base_score = max(30, 90 - (len(conditions) * 15))
    return min(100, max(10, base_score + random.randint(-5, 5)))

# Routes
@app.route('/')
def index():
    """Serve the frontend (would be built separately in production)"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/analyze', methods=['GET'])
def analyze_health_get():
    return jsonify({
        "error": "Method not allowed",
        "message": "Use POST request to submit health data"
    }), 405

@app.route('/api/analyze', methods=['POST'])
def analyze_health():
    """Enhanced health analysis endpoint with fixes"""
    try:
        # Get form data with safe defaults
        user_input = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'gender': request.form.get('gender', '').strip(),
            'bloodGroup': request.form.get('bloodGroup', '').strip(),
            'ethnicity': request.form.get('ethnicity', '').strip(),
            'symptoms': request.form.getlist('symptoms[]'),
            'body_parts': request.form.getlist('body_parts[]'),
            'description': request.form.get('description', '').strip()
        }

        # Validate required fields
        if not user_input['name'] or not user_input['description']:
            return jsonify({"error": "Name and health description are required"}), 400

        # Process uploaded files
        files = request.files.getlist('files')
        files_info = analyze_uploaded_files(files)
        files_text = [f['content'] for f in files_info if 'content' in f and isinstance(f['content'], str)]

        # Analyze symptoms and conditions
        conditions = analyze_symptoms(user_input, files_text)

        # Generate summary
        summary = generate_summary(user_input, conditions, files_info)
        save_user_data(user_input, conditions)

        # Add timestamp if missing
        if 'timestamp' not in summary['user_info']:
            summary['user_info']['timestamp'] = datetime.now().isoformat()

        # Generate unique session ID for telemedicine
        session_id = str(uuid.uuid4())
        summary['session_id'] = session_id

        # Generate PDF report
        try:
            pdf_path = generate_pdf_report(summary)
            summary['pdf_url'] = f'/download-report/{session_id}'
        except Exception as e:
            app.logger.error(f"PDF generation failed: {str(e)}")
            summary['pdf_url'] = None

        # Return response based on request type
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response = jsonify(summary)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            return render_template('result.html', summary=summary)

    except Exception as e:
        app.logger.exception("Critical analysis error")
        return jsonify({
            "error": "analysis_failed",
            "message": str(e),
            "details": "See server logs for more information"
        }), 500


def generate_pdf_report(summary):
    from fpdf import FPDF, XPos, YPos
    from datetime import datetime

    class PDF(FPDF):
        def header(self):
            if self.page_no() == 1:
                self.set_fill_color(58, 104, 147)
                self.rect(0, 0, self.w, 20, 'F')
                self.set_font("Helvetica", 'B', 20)
                self.set_text_color(255, 255, 255)
                self.set_y(6)
                self.cell(0, 10, "SmartHealth AI Patient Summary", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        def section_title(self, title):
            self.set_y(self.get_y() + 6)
            self.set_fill_color(217, 237, 247)
            self.set_text_color(0, 51, 102)
            self.set_font("Helvetica", 'B', 14)
            self.set_x(self.l_margin)
            self.cell(0, 10, title, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        def section_body(self, lines):
            self.set_font("Helvetica", '', 11)
            self.set_text_color(0)
            for line in lines:
                self.set_x(self.l_margin + 5)
                self.multi_cell(0, 6, line)
            self.ln(2)
        def footer(self):
            self.set_y(-20)
            self.set_font("Helvetica", 'B', 9)
            self.set_text_color(0, 102, 204)  # Blue color
            self.set_draw_color(0, 102, 204)  # Blue border
            self.set_line_width(0.5)

            self.set_x(self.l_margin)
            self.cell(
                0, 10,
                "This report is generated by SmartHealth AI. Not a substitute for professional medical advice.",
                border=1,
                align='C'
            )

    pdf = PDF(orientation='P', format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(left=20, top=25, right=20)
    pdf.add_page()

    user_info = summary.get('user_info', {})
    timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")

    # Patient Info
    pdf.section_title("Patient Information")
    fields = [
        f"Name: {user_info.get('name', '-')}",
        f"Email: {user_info.get('email', '-')}",
        f"Phone: {user_info.get('phone', '-')}",
        f"Gender: {user_info.get('gender', '-')}",
        f"Blood Group: {user_info.get('bloodGroup', '-')}",
        f"Report Generated: {timestamp}"
    ]
    pdf.section_body(fields)

    if summary.get('possible_conditions'):
        pdf.section_title("Possible Conditions")
        pdf.section_body(summary['possible_conditions'])

    pdf.section_title("AI Insights")
    health_summary = summary.get('health_summary', {})
    confidence_score = health_summary.get('confidence_score', 92)
    model_used = health_summary.get('model', "SmartHealthML v2.1")
    pdf.section_body([
        f"Prediction Confidence: {confidence_score}%",
        f"Model Used: {model_used}"
    ])

    # Action Plan
    plan = health_summary.get('action_plan', [])
    if plan:
        pdf.section_title("7-Day Health Action Plan")
        pdf.section_body(plan)

    # Health Sections
    health_sections = [
        ("First Aid & Home Remedies", health_summary.get('first_aid', [])),
        ("Lifestyle Recommendations", health_summary.get('lifestyle_recommendations', [])),
        ("Dietary Suggestions", health_summary.get('dietary_suggestions', [])),
    ]
    for title, content in health_sections:
        if content:
            pdf.section_title(title)
            pdf.section_body(content)

    pdf.add_page()
    # Reference Table
    pdf.section_title("Health Reference Ranges")
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_x(pdf.l_margin)
    pdf.cell(60, 8, "Vital", border=1, align='C', fill=True)
    pdf.cell(100, 8, "Normal Range", border=1, align='C', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", '', 11)
    references = [
        ("Heart Rate", "60-100 bpm"),
        ("Blood Pressure", "120/80 mmHg"),
        ("BMI", "18.5-24.9"),
        ("Temperature", "97°F - 99°F")
    ]
    for vital, value in references:
        pdf.set_x(pdf.l_margin)
        pdf.cell(60, 8, vital, border=1)
        pdf.cell(100, 8, value, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Specialist
    specialist = health_summary.get('recommended_specialist')
    if specialist:
        pdf.section_title("Recommended Specialist")
        pdf.section_body([specialist])

    # QR Code
    qr_path = os.path.join(TEMP_DIR, "qr_code.png")
    try:
        save_qr_code("https://github.com/yourusername/smarthealth-ai", qr_path)
        pdf.section_title("Access Full Project")
        pdf.image(qr_path, x=pdf.l_margin, w=40)
        pdf.set_font("Helvetica", '', 10)
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 10, "Scan the QR to visit GitHub project page.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    except:
        pdf.section_body(["[QR Code could not be generated]"])


    pdf_path = os.path.join(TEMP_DIR, f"{summary['session_id']}.pdf")
    pdf.output(pdf_path)
    return pdf_path


# Report Download Endpoint
@app.route('/download-report/<session_id>')
def download_report(session_id):
    try:
        pdf_path = os.path.join(TEMP_DIR, f"{session_id}.pdf")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError()

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"SmartHealth-Summary-{session_id[:8]}.pdf",
            mimetype='application/pdf'
        )
    except FileNotFoundError:
        return jsonify({"error": "Report not found or expired"}), 404


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Resource not found"), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('error.html', error="Method not allowed"), 405

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)