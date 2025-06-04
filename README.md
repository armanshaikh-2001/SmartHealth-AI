<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>SmartHealth AI – README</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.7;
      margin: 0;
      padding: 2rem;
      background: #f8f9fa;
      color: #333;
    }
    h1, h2, h3 {
      color: #0d6efd;
    }
    h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }
    h2 {
      margin-top: 2rem;
      border-bottom: 2px solid #dee2e6;
      padding-bottom: 0.5rem;
    }
    p {
      margin: 0.5rem 0;
    }
    pre {
      background: #f1f1f1;
      padding: 1rem;
      overflow-x: auto;
      border-left: 4px solid #0d6efd;
    }
    code {
      background: #e9ecef;
      padding: 2px 5px;
      border-radius: 4px;
      font-family: Consolas, monospace;
    }
    ul {
      padding-left: 1.5rem;
    }
    li {
      margin: 0.5rem 0;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin-top: 1rem;
    }
    table, th, td {
      border: 1px solid #dee2e6;
    }
    th, td {
      padding: 0.75rem;
      text-align: left;
    }
    blockquote {
      border-left: 5px solid #0d6efd;
      margin: 1rem 0;
      padding-left: 1rem;
      color: #555;
      background: #f1f3f5;
    }
    .screenshot img {
      max-width: 100%;
      border: 1px solid #dee2e6;
      margin: 1rem 0;
    }
    .license, .acknowledgments, .author {
      margin-top: 2rem;
      font-size: 0.95rem;
      color: #666;
    }
    .author a {
      color: #0d6efd;
      text-decoration: none;
    }
  </style>
</head>
<body>

  <h1>🧠 SmartHealth AI – Interactive Medical Summary Generator</h1>
  <p>An intelligent web-based health assistant that analyzes user symptoms and uploaded medical reports to generate a personalized medical summary, including condition suggestions, lifestyle advice, and a downloadable PDF report.</p>
  <p><strong>Built for aspiring healthcare technology and AI solutions.</strong></p>

  <h2>🚀 Features</h2>
  <ul>
    <li>🩺 Symptom & body part selection via interactive UI</li>
    <li>📁 Upload support for medical PDFs, images, and videos</li>
    <li>🧠 AI logic to predict possible conditions</li>
    <li>📊 Health score and recommendations generator</li>
    <li>🧾 Exportable PDF medical summary</li>
    <li>💾 SQLite database to store user input</li>
    <li>🤖 Optional ML model trained on synthetic symptom data</li>
    <li>🧪 Unit tests for backend validation</li>
  </ul>

  <h2>📸 Screenshots</h2>
  <div class="screenshot">
    <img src=static/project-snaps/img_1.png" alt="SmartHealth AI Screenshot"/>
  </div>
<div class="screenshot">
    <img src=static/project-snaps/img_2.png" alt="SmartHealth AI Screenshot"/>
<div class="screenshot">
    <img src=static/project-snaps/pdf_report.png" alt="SmartHealth AI Screenshot"/>
  </div>

  </div>

  <blockquote>
    <em>Mock UI: Includes file uploads, symptom selectors, PDF download, and AI-powered insights.</em>
  </blockquote>

  <h2>🛠 Tech Stack</h2>
  <table>
    <thead>
      <tr><th>Frontend</th><th>Backend</th><th>AI & OCR</th><th>PDF</th><th>Storage</th></tr>
    </thead>
    <tbody>
      <tr><td>HTML, CSS, JS</td><td>Flask, Python</td><td>scikit-learn, Tesseract OCR</td><td>FPDF</td><td>SQLite</td></tr>
    </tbody>
  </table>

  <h2>📦 Installation</h2>
  <h3>1. Clone the repository</h3>
  <pre><code>git clone https://github.com/your-username/smarthealth-ai.git
cd smarthealth-ai</code></pre>

  <h3>2. Create a virtual environment</h3>
  <pre><code>python -m venv venv
venv\Scripts\activate  # On Windows</code></pre>

  <h3>3. Install dependencies</h3>
  <pre><code>pip install -r requirements.txt</code></pre>

  <blockquote>
    🔍 Ensure <a href="https://github.com/tesseract-ocr/tesseract" target="_blank">Tesseract OCR</a> is installed on your system.<br/>
    On Windows, set the path in <code>app.py</code>:
    <pre><code>pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'</code></pre>
  </blockquote>

  <h2>⚙️ Run the App</h2>
  <pre><code>python app.py</code></pre>
  <p>Visit: <a href="http://localhost:5050">http://localhost:5050</a></p>

  <h2>🧪 Running Tests</h2>
  <pre><code>python test_app.py</code></pre>

  <h2>🧠 Using the ML Model</h2>
  <pre><code>python ml_model.py</code></pre>
  <p>Modify test symptoms inside <code>ml_model.py</code>:</p>
  <pre><code>test_input = ['cough', 'sore_throat']</code></pre>

  <h2>💽 Data Storage</h2>
  <ul>
    <li>User inputs saved in <code>health.db</code> (SQLite).</li>
    <li>View with:
      <pre><code>sqlite3 health.db
sqlite&gt; SELECT * FROM health_data;</code></pre>
    </li>
  </ul>

  <h2>✨ Portfolio Value</h2>
  <ul>
    <li>Full-stack capability (frontend + backend + DB)</li>
    <li>AI-driven decision logic</li>
    <li>Clean data modeling with JSON</li>
    <li>PDF report automation</li>
    <li>Practical healthcare application</li>
  </ul>

  <h2>📁 Project Structure</h2>
  <pre><code>smarthealth-ai/
├── app.py                # Main Flask backend
├── storage.py            # SQLite data storage logic
├── ml_model.py           # ML prediction script
├── test_app.py           # Unit tests
├── condition_mapping.json# Knowledge base
├── templates/
│   └── index.html        # Main UI
├── static/
│   ├── js/script.js      # Frontend logic
│   └── css/style.css     # Styling (if applicable)
├── health.db             # SQLite DB (auto-created)
└── README.md             # This file
</code></pre>

  <div class="license">
    <h2>📄 License</h2>
    <p>This project is for educational and demonstration purposes only. Not a substitute for professional medical advice.</p>
  </div>

  <div class="acknowledgments">
    <h2>🙌 Acknowledgments</h2>
    <ul>
      <li><a href="https://github.com/tesseract-ocr/tesseract">Tesseract OCR</a></li>
      <li><a href="https://scikit-learn.org/">scikit-learn</a></li>
      <li><a href="https://pyfpdf.readthedocs.io/">FPDF for Python</a></li>
      <li>Font Awesome icons & UI inspiration</li>
    </ul>
  </div>

  <div class="author">
    <h2>💼 Author</h2>
    <p><strong>[Your Name]</strong> – <em>AI & Full-Stack Developer</em></p>
    <p>
      <a href="https://linkedin.com/in/your-profile">LinkedIn</a> |
      <a href="https://github.com/your-username">GitHub</a> |
      <a href="https://yourportfolio.com">Portfolio</a>
    </p>
  </div>

</body>
</html>
