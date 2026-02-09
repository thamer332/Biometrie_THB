let currentFilename = null;

// Gestion de l'upload
const fileInput = document.getElementById('fileInput');
const uploadBox = document.getElementById('uploadBox');
const browseBtn = document.getElementById('browseBtn');

fileInput.addEventListener('change', handleFileSelect);

// Bouton Parcourir
browseBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Empêcher la propagation au parent
    fileInput.click();
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = 'var(--accent)';
    uploadBox.style.transform = 'scale(1.02)';
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.style.borderColor = 'var(--primary)';
    uploadBox.style.transform = 'scale(1)';
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = 'var(--primary)';
    uploadBox.style.transform = 'scale(1)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// Clic sur la zone (mais pas sur le bouton)
uploadBox.addEventListener('click', (e) => {
    // Ne rien faire si le clic est sur le bouton
    if (e.target.id !== 'browseBtn' && !e.target.closest('#browseBtn')) {
        fileInput.click();
    }
});

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

async function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Veuillez sélectionner une image valide');
        return;
    }

    showLoader();
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            currentFilename = data.filename;
            document.getElementById('originalImage').src = data.image;
            document.getElementById('originalInfo').textContent = 
                `Dimensions: ${data.size[0]} x ${data.size[1]} px`;
            
            document.getElementById('controlPanel').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            // Animation d'apparition
            setTimeout(() => {
                document.getElementById('controlPanel').style.animation = 'fadeIn 0.5s ease-out';
            }, 100);
        } else {
            alert('Erreur: ' + data.error);
        }
    } catch (error) {
        alert('Erreur lors du téléchargement: ' + error.message);
    } finally {
        hideLoader();
    }
}

async function processImage(action) {
    if (!currentFilename) {
        alert('Veuillez d\'abord charger une image');
        return;
    }

    showLoader();

    const requestData = {
        action: action,
        filename: currentFilename
    };

    // Ajouter les paramètres spécifiques selon l'action
    switch(action) {
        case 'resize':
            requestData.width = document.getElementById('resizeWidth').value;
            requestData.height = document.getElementById('resizeHeight').value;
            break;
        case 'rotate':
            requestData.angle = document.getElementById('rotateAngle')?.value || 90;
            break;
        case 'blur':
            requestData.radius = 5;
            break;
        case 'brightness':
            requestData.factor = document.getElementById('brightness').value;
            break;
        case 'contrast':
            requestData.factor = document.getElementById('contrast')?.value || 1.5;
            break;
        case 'binarize':
            requestData.threshold = document.getElementById('binarizeThreshold').value;
            break;
        case 'gaussian_blur':
            requestData.radius = document.getElementById('gaussianRadius').value;
            break;
    }

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('originalImage').src = data.original;
            document.getElementById('resultImage').src = data.result;
            document.getElementById('resultInfo').textContent = 
                `Dimensions: ${data.size[0]} x ${data.size[1]} px`;
            
            document.getElementById('results').style.display = 'block';
            document.getElementById('downloadBtn').style.display = 'block';
            document.getElementById('downloadBtn').onclick = () => {
                window.location.href = `/download/${data.filename}`;
            };

            // Scroll vers les résultats
            document.getElementById('results').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        } else {
            alert('Erreur: ' + data.error);
        }
    } catch (error) {
        alert('Erreur lors du traitement: ' + error.message);
    } finally {
        hideLoader();
    }
}

function showLoader() {
    document.getElementById('loader').style.display = 'block';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

// Mise à jour des valeurs des sliders
document.getElementById('brightness').addEventListener('input', (e) => {
    document.getElementById('brightnessValue').textContent = e.target.value;
});

if (document.getElementById('contrast')) {
    document.getElementById('contrast').addEventListener('input', (e) => {
        document.getElementById('contrastValue').textContent = e.target.value;
    });
}

document.getElementById('binarizeThreshold').addEventListener('input', (e) => {
    document.getElementById('binarizeValue').textContent = e.target.value;
});

document.getElementById('gaussianRadius').addEventListener('input', (e) => {
    document.getElementById('gaussianValue').textContent = e.target.value;
});

// Fonction pour afficher l'histogramme
async function showHistogram() {
    if (!currentFilename) {
        alert('Veuillez d\'abord charger une image');
        return;
    }

    showLoader();

    try {
        const response = await fetch('/histogram', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: currentFilename })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('originalImage').src = data.original;
            document.getElementById('resultImage').src = data.histogram;
            document.getElementById('resultInfo').textContent = 'Histogramme des niveaux de gris';
            
            document.getElementById('results').style.display = 'block';
            document.getElementById('downloadBtn').style.display = 'none';

            // Scroll vers les résultats
            document.getElementById('results').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        } else {
            alert('Erreur: ' + data.error);
        }
    } catch (error) {
        alert('Erreur lors du calcul de l\'histogramme: ' + error.message);
    } finally {
        hideLoader();
    }
}

// Animation de chargement de la page
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});
