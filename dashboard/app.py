import threading
import shutil
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploads")
REPORTS_FOLDER = os.path.join(PROJECT_ROOT, "reports")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

@app.route("/")
def index():
    reports = []
    for file in os.listdir(REPORTS_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(REPORTS_FOLDER, file)) as f:
                reports.append(json.load(f))
    return render_template("index.html", reports=reports)
    
    
analysis_status = {}
import sys
sys.path.insert(0, os.path.dirname(__file__))
from analyze import run as run_analysis_func

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["apk"]
    
    if not file.filename.endswith(".apk"):
        return {"error": "Only .apk files allowed"}, 400
    
    filename = secure_filename(file.filename)
    apk_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(apk_path)
    
    analysis_status[filename] = "running"
    
    def run_analysis():
        try:
            run_analysis_func(apk_path)
            analysis_status[filename] = "done"
        except Exception as e:
            print(f"Analysis error: {e}")
            analysis_status[filename] = "error"
    
    thread = threading.Thread(target=run_analysis)
    thread.start()
    
    return {"status": "started", "filename": filename}
    
@app.route("/status/<filename>")
def status(filename):
    return {"status": analysis_status.get(filename, "unknown")}
    

if __name__ == "__main__":
    app.run(debug=True)
