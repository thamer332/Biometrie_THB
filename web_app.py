from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io
import base64
from werkzeug.utils import secure_filename
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Créer les dossiers s'ils n'existent pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image):
    """Convertir une image PIL en base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Charger et convertir l'image
        image = Image.open(filepath)
        image_base64 = image_to_base64(image)
        
        return jsonify({
            'success': True,
            'image': image_base64,
            'filename': filename,
            'size': image.size
        })
    
    return jsonify({'error': 'Type de fichier non autorisé'}), 400

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    action = data.get('action')
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'Aucune image chargée'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Image non trouvée'}), 404
    
    image = Image.open(filepath)
    result_image = None
    
    try:
        # Convertir en RGB si nécessaire (éviter "image has wrong mode")
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        
        if action == 'resize':
            width = int(data.get('width', 200))
            height = int(data.get('height', 200))
            result_image = image.resize((width, height))
            
        elif action == 'rotate':
            angle = float(data.get('angle', 90))
            result_image = image.rotate(angle, expand=True)
            
        elif action == 'flip_horizontal':
            result_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            
        elif action == 'flip_vertical':
            result_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            
        elif action == 'grayscale':
            result_image = image.convert('L')
            
        elif action == 'blur':
            # S'assurer que l'image est en RGB pour le flou
            if image.mode != 'RGB':
                image = image.convert('RGB')
            radius = float(data.get('radius', 5))
            result_image = image.filter(ImageFilter.GaussianBlur(radius))
            
        elif action == 'sharpen':
            # S'assurer que l'image est en RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            result_image = image.filter(ImageFilter.SHARPEN)
            
        elif action == 'brightness':
            # S'assurer que l'image est en RGB pour ImageEnhance
            if image.mode != 'RGB':
                image = image.convert('RGB')
            factor = float(data.get('factor', 1.5))
            enhancer = ImageEnhance.Brightness(image)
            result_image = enhancer.enhance(factor)
            
        elif action == 'contrast':
            # S'assurer que l'image est en RGB pour ImageEnhance
            if image.mode != 'RGB':
                image = image.convert('RGB')
            factor = float(data.get('factor', 1.5))
            enhancer = ImageEnhance.Contrast(image)
            result_image = enhancer.enhance(factor)
            
        elif action == 'edge_detect':
            # Convertir en niveaux de gris pour la détection de contours
            gray_image = image.convert('L')
            result_image = gray_image.filter(ImageFilter.FIND_EDGES)
            
        elif action == 'binarize':
            threshold = int(data.get('threshold', 128))
            gray_image = image.convert('L')
            result_image = gray_image.point(lambda x: 255 if x > threshold else 0)
            
        elif action == 'equalize':
            gray_image = image.convert('L')
            result_image = ImageOps.equalize(gray_image)
            
        elif action == 'gaussian_blur':
            # S'assurer que l'image est en RGB pour le flou gaussien
            if image.mode != 'RGB':
                image = image.convert('RGB')
            radius = int(data.get('radius', 2))
            result_image = image.filter(ImageFilter.GaussianBlur(radius))
            
        else:
            return jsonify({'error': 'Action non reconnue'}), 400
        
        # Sauvegarder l'image traitée dans le dossier results
        result_filename = f"processed_{action}_{filename}"
        result_filepath = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
        result_image.save(result_filepath)
        
        result_base64 = image_to_base64(result_image)
        
        return jsonify({
            'success': True,
            'original': image_to_base64(image),
            'result': result_base64,
            'filename': result_filename,
            'size': result_image.size
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
    if not os.path.exists(filepath):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

@app.route('/histogram', methods=['POST'])
def histogram():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'Aucune image chargée'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Image non trouvée'}), 404
    
    try:
        image = Image.open(filepath)
        gray_image = image.convert('L')
        
        # Calculer l'histogramme
        hist = gray_image.histogram()
        
        # Créer le graphique
        plt.figure(figsize=(10, 5))
        plt.plot(hist, color='black')
        plt.title('Histogramme de l\'image en niveaux de gris')
        plt.xlabel('Niveau de gris (0-255)')
        plt.ylabel('Nombre de pixels')
        plt.grid(True, alpha=0.3)
        
        # Sauvegarder le graphique en base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        hist_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'histogram': f"data:image/png;base64,{hist_base64}",
            'original': image_to_base64(gray_image)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    # Pour la production (Render, Railway, etc.)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
