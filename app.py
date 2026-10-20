from flask import Flask, render_template, request, redirect, session, send_from_directory
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'dev-kento-amatrix-2026'
UPLOAD_FOLDER = 'uploads'
ADMIN_PASS = 'kento123'
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    text = request.form.get('text','')
    if file and file.filename:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    elif text:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + "_note.txt"
        with open(os.path.join(UPLOAD_FOLDER, filename), "w", encoding="utf-8") as f:
            f.write(text)
    return "✅ FICHIER BIEN REÇU PAR DEV KENTO AMATRIX"
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['is_admin'] = True
            return redirect('/admin')
        else:
            return "Mauvais mot de passe Boss"
    if not session.get('is_admin'):
        return render_template('admin_login.html')
    files = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    return render_template('admin.html', files=files)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/delete/<filename>')
def delete(filename):
    if not session.get('is_admin'): return "Non autorisé"
    try: os.remove(os.path.join(UPLOAD_FOLDER, filename))
    except: pass
    return redirect('/admin')
@app.route('/uploads/<filename>')
def get_file(filename):
    if not session.get('is_admin'): return "Non autorisé"
    return send_from_directory(UPLOAD_FOLDER, filename)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
