import os
import pytest
import json
from io import BytesIO
from werkzeug.datastructures import FileStorage
from app import app, allowed_file, extract_text_from_pdf, extract_text_from_image, analyze_symptoms, generate_summary

# Test Client Setup
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.test_client() as client:
        yield client
    # Cleanup
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
    os.rmdir(app.config['UPLOAD_FOLDER'])

# Helper Functions
def create_test_file(filename, content=None, filetype='text/plain'):
    if not content:
        content = f"Test content for {filename}"
    return FileStorage(
        stream=BytesIO(content.encode()),
        filename=filename,
        content_type=filetype
    )

# --- Core Function Tests ---
def test_allowed_file():
    assert allowed_file("report.pdf") == True
    assert allowed_file("image.png") == True
    assert allowed_file("video.mp4") == True
    assert allowed_file("script.exe") == False

def test_extract_text_from_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    with open(pdf_path, 'wb') as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<</Title(Test PDF)>>\nendobj\nxref\ntrailer\n<</Root 1 0 R>>\nstartxref\n%%EOF")
    text = extract_text_from_pdf(str(pdf_path))
    assert "Test PDF" in text

def test_analyze_symptoms():
    user_input = {
        'symptoms': ['headache', 'nausea'],
        'body_parts': ['head'],
        'description': "I have a severe headache"
    }
    conditions = analyze_symptoms(user_input, [])
    assert any(c['name'] == 'Migraine' for c in conditions)

# --- Route Tests ---
def test_index_route(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"SmartHealth AI" in res.data

def test_health_check(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert b"healthy" in res.data

def test_analyze_route_json(client):
    data = {
        'name': 'Test User',
        'description': 'Headache and nausea',
        'symptoms[]': ['headache', 'nausea'],
        'body_parts[]': ['head']
    }
    res = client.post('/api/analyze', data=data, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert res.status_code == 200
    response = json.loads(res.data)
    assert 'possible_conditions' in response

def test_analyze_route_with_files(client):
    data = {
        'name': 'Test User',
        'description': 'Test with files'
    }
    files = {
        'files': create_test_file("report.pdf", "Test PDF Content", "application/pdf")
    }
    res = client.post('/api/analyze', data=data, files=files)
    assert res.status_code == 200

# --- Full Integration Test ---
def test_full_workflow(client):
    # Step 1: Load index page
    res = client.get('/')
    assert b"Medical Summary Generator" in res.data

    # Step 2: Submit form with all data types
    data = {
        'name': 'Integration Test',
        'email': 'test@example.com',
        'phone': '1234567890',
        'gender': 'male',
        'ethnicity': 'asian',
        'description': 'Severe headache with light sensitivity',
        'symptoms[]': ['headache', 'nausea'],
        'body_parts[]': ['head']
    }
    files = {
        'files': create_test_file("blood_report.pdf", "Patient: Integration Test\nSymptoms: Headache", "application/pdf")
    }
    res = client.post('/api/analyze', data=data, files=files)
    
    # Verify response
    assert res.status_code == 200
    if res.headers['Content-Type'] == 'application/json':
        response = json.loads(res.data)
        assert 'Migraine' in str(response['possible_conditions'])
    else:
        assert b"First Aid" in res.data  # HTML response

# --- Error Handling Tests ---
def test_invalid_file_upload(client):
    res = client.post('/api/analyze', data={
        'name': 'Test',
        'description': 'Test'
    }, files={
        'files': create_test_file("virus.exe", "malicious", "application/exe")
    })
    assert res.status_code == 400

def test_missing_required_fields(client):
    res = client.post('/api/analyze', data={
        'description': 'No name provided'
    })
    assert res.status_code == 400

# --- Test Coverage ---
"""
To run with coverage:
1. pip install pytest-cov
2. pytest --cov=app --cov-report=html test_smarthealth.py
"""