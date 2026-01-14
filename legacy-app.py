import os
import logging
from flask import Flask, request, render_template_string

# VIOLATION 2: Implicit Dependencies
# The app ASSUMES these folders exist on the Operating System.
# It does not check for them. It does not create them.
# If the SysAdmin forgot to run 'mkdir', the app crashes.
DATA_DIR = "data"
LOG_FILE = "logs/app.log"
UPLOAD_DIR = "uploads"

APP_COLOR = "lightgrey" 
SECRET_KEY = "my_hardcoded_secret_key_123"

app = Flask(__name__)
app.secret_key = SECRET_KEY

# VIOLATION 11: Logging to file
# This will CRASH with FileNotFoundError if the 'logs' folder doesn't exist.
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

HTML_TEMPLATE = """
<body style="background-color: {{ color }}; font-family: sans-serif; padding: 2rem;">
    <h1>Legacy Monolith App</h1>
    <div style="border: 2px solid black; padding: 20px; background: white;">
        <h2>Visitor Count: {{ count }}</h2>
    </div>
    <br>
    <div style="border: 2px solid red; padding: 20px; background: white;">
        <h3>Upload a File</h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </div>
</body>
"""

@app.route('/')
def index():
    count_file = os.path.join(DATA_DIR, "counter.txt")
    
    count = 0
    # Logic tries to read file, but if folder is missing, writing back will fail later
    if os.path.exists(count_file):
        with open(count_file, 'r') as f:
            try:
                count = int(f.read())
            except ValueError:
                count = 0
    
    count += 1
    
    # VIOLATION: This will CRASH if 'data' folder is missing
    with open(count_file, 'w') as f:
        f.write(str(count))
        
    logging.info(f"Page visited. New count: {count}")
    return render_template_string(HTML_TEMPLATE, count=count, color=APP_COLOR)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # VIOLATION: This will CRASH if 'uploads' folder is missing
    file.save(save_path)
    
    logging.info(f"File saved locally at {save_path}")
    return f"File '{file.filename}' saved successfully!"

if __name__ == "__main__":
    print(f"Starting Legacy App...")
    # This will crash immediately if 'logs' folder is missing due to logging setup above
    app.run(host="0.0.0.0", port=5000)