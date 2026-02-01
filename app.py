from flask import Flask, render_template, request, jsonify
from printer_service import PrinterService
import os
import secrets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Default to "ThermalPrinter" as configured in CUPS
# User can change this in the UI or Env Var
PRINTER_NAME = os.environ.get("PRINTER_NAME", "ThermalPrinter")
printer = PrinterService(printer_name=PRINTER_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle File Uploads for Printing
    """
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    if file:
        filename = secrets.token_hex(8) + "_" + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            printer.print_file(filepath)
            # Clean up immediately
            os.remove(filepath) 
            return jsonify({"status": "success", "message": "File sent to printer"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Listen on port 8080 (Mapped to ngrok http 8080)
    app.run(host='0.0.0.0', port=8080, debug=True)
