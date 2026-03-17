from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
SECRET_KEY = 'vanille2026'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_auth(req):
    auth_header = req.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return token == SECRET_KEY
    return False

def read_json(filename, default=None):
    if default is None:
        default = []
    if not os.path.exists(filename):
        return default
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default

def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data or data.get('key') != SECRET_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'status': 'success', 'token': SECRET_KEY})

@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    return jsonify(read_json('blogs.json'))

@app.route('/api/blogs', methods=['POST'])
def save_blogs():
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    write_json('blogs.json', data)
    return jsonify({'status': 'success'})

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    default_gallery = [
        {"name": "Dark Truffle Extravagance", "imageUrl": "https://lh3.googleusercontent.com/aida-public/AB6AXuBTyXF_qZYWsAJad2iF7XBhZlxTNQa0UuOkPYmdXHSSJCT4mTplHj9cg5R4zU_pSqV7QszqjoPCrDmJxll_fPSdkFHqmLao_N1V6fmNmLC4Z2l4ceKbB44mD0p_8wsk_bEsW6Uofy-EpxOcX19Rzj3XV0Kef9gqfocEJ2SRo1HTbMsd81pjyG8YXQGB-NbYx5PWd0j-QtPucM4sUnbyS2E3whriAVplIVxfNp7ziKEAbeh1o0sThZ68E9MJwLNvAT6tSZ4S42zeQVaI"},
        {"name": "Vanilla Bean Dream", "imageUrl": "https://lh3.googleusercontent.com/aida-public/AB6AXuBOmYUO8zyj8XBQqcF04HXqXoPP9HhPgmy2xXCXme2nTxMyAWCDX6aqiaSBopyipin_VgUYK-feVP_6A18AR0zc0ti5WNzn4PAjcUcbad8W1UbUeMkTihFLPnCSgR2vhbWzba4Adip4EKqwe3D-tDGRA-hjBPI3JTw6fIkMnhCvnCEm8ciFLZIdgKLsxEGNssEWrUIA7U4hkEu2jvdWVoZHsdS8N6Zperqt8LRfgWx04uzTaev4i_rEo4S-dw7z1sJwrN_0twQULNnn"},
        {"name": "Red Velvet Passion", "imageUrl": "https://lh3.googleusercontent.com/aida-public/AB6AXuAfA1-YQ018mjrZsnHDuT9ss4cK0RPDJyQjsRlcioM6-t4ds8TCczPmduN7B1DhKUPYPjr6-3SilB_O7Isl6w1o13BhoK-zGj0kQdYu2FCxYldpUffyq1FxaD1FbltdX_mf6Dy_Bew4S2Ow5cHCp8-K7l117sM9wjvGi0r8AhQFCllAlTB1eixiJik_b21MOpfVdko6gKNFYTyovA14YXxTZrlfjb7BAcvADljX7SJsOQjSvt7Nai74eRrxSHyh_FGKl9xA85-JpLby"}
    ]
    if not os.path.exists('gallery.json'):
         write_json('gallery.json', default_gallery)
    return jsonify(read_json('gallery.json', default_gallery))

@app.route('/api/gallery', methods=['POST'])
def save_gallery():
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    write_json('gallery.json', data)
    return jsonify({'status': 'success'})

@app.route('/upload', methods=['POST'])
def upload_image():
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    url = f'/uploads/{filename}'
    return jsonify({'url': url})

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
