import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name="dhavixtln",
    api_key="965531754343319",
    api_secret="YBVYU-VQXrkCzaXkFoGHONyNNuo"
)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key

# Temporary list to store images (later use DB)
images = []

@app.route('/')
def index():
    return render_template('index.html', images=images)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'rahul' and password == 'rahul7975':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if 'file' not in request.files:
        return redirect(url_for('index'))
    files = request.files.getlist('file')
    for file in files:
        if file.filename != '':
            result = cloudinary.uploader.upload(file)
            image_url = result['secure_url']
            public_id = result['public_id']
            images.append({
                "url": image_url,
                "id": public_id
            })
    return redirect(url_for('index'))

@app.route('/delete/<public_id>', methods=['POST'])
def delete(public_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    cloudinary.uploader.destroy(public_id)
    global images
    images = [img for img in images if img['id'] != public_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)