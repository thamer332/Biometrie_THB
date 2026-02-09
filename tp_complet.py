"""
TP : Traitement des images avec la bibliothèque PIL (Pillow)
Toutes les parties (1-9) avec affichage et sauvegarde
"""

from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import matplotlib.pyplot as plt
import os

# Créer le dossier results s'il n'existe pas
os.makedirs('results', exist_ok=True)

# Charger l'image originale
chemin_image = 'lena_color.gif'
image = Image.open(chemin_image)

# Convertir en RGB si nécessaire (pour éviter "image has wrong mode")
if image.mode != 'RGB':
    image = image.convert('RGB')

print("=" * 60)
print("TP Traitement d'Images - Toutes les Parties")
print("=" * 60)

# ===== PARTIE 1 : Lecture et affichage de l'image originale =====
print("\n[Partie 1] Lecture et affichage de l'image originale")
plt.figure(figsize=(6, 6))
plt.subplot(1, 1, 1)
plt.imshow(image)
plt.title("Image Originale")
plt.axis("off")
plt.tight_layout()
plt.savefig('results/partie1_image_originale.png', dpi=100, bbox_inches='tight')
plt.show()
image.save('results/image_originale.png')
print("✓ Image sauvegardée : results/image_originale.png")

# ===== PARTIE 2 : Redimensionnement de l'image =====
print("\n[Partie 2] Redimensionnement de l'image")
nouvelle_taille = (200, 200)
image_redimensionnee = image.resize(nouvelle_taille)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title(f"Image Originale ({image.size[0]}x{image.size[1]})")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_redimensionnee)
plt.title(f"Image Redimensionnée ({nouvelle_taille[0]}x{nouvelle_taille[1]})")
plt.axis("off")

plt.tight_layout()
plt.savefig('results/partie2_comparaison.png', dpi=100, bbox_inches='tight')
plt.show()
image_redimensionnee.save('results/image_redimensionnee.png')
print("✓ Image sauvegardée : results/image_redimensionnee.png")
print(f"  Transformation : {image.size} → {nouvelle_taille}")

# ===== PARTIE 3 : Ajustement de la luminosité =====
print("\n[Partie 3] Ajustement de la luminosité")
facteur_luminosite = 1.5

# S'assurer que l'image est en mode RGB pour ImageEnhance
if image.mode != 'RGB':
    image_rgb = image.convert('RGB')
else:
    image_rgb = image

enhancer = ImageEnhance.Brightness(image_rgb)
image_lumineuse = enhancer.enhance(facteur_luminosite)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title("Image Originale")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_lumineuse)
plt.title(f"Luminosité Augmentée (facteur {facteur_luminosite})")
plt.axis("off")

plt.tight_layout()
plt.savefig('results/partie3_comparaison.png', dpi=100, bbox_inches='tight')
plt.show()
image_lumineuse.save('results/image_luminosite_augmente.png')
print("✓ Image sauvegardée : results/image_luminosite_augmente.png")
print(f"  Facteur de luminosité : {facteur_luminosite}")

# ===== PARTIE 4 : Conversion en niveaux de gris =====
print("\n[Partie 4] Conversion en niveaux de gris")
image_gris = image.convert('L')

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("Image Originale (Couleur)")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_gris, cmap='gray')
plt.title("Image en Niveaux de Gris")
plt.axis("off")

plt.tight_layout()
plt.savefig('results/partie4_comparaison.png', dpi=100, bbox_inches='tight')
plt.show()
image_gris.save('results/image_gris.png')
print("✓ Image sauvegardée : results/image_gris.png")
print("  Mode de conversion : 'L' (Luminance)")

# ===== PARTIE 5 : Binarisation de l'image =====
print("\n[Partie 5] Binarisation de l'image")
seuil = 128
image_binarisee = image_gris.point(lambda x: 255 if x > seuil else 0)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image_gris, cmap='gray')
plt.title("Image en Niveaux de Gris")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_binarisee, cmap='gray')
plt.title(f"Image Binarisée (seuil = {seuil})")
plt.axis("off")

plt.tight_layout()
plt.savefig('results/partie5_comparaison.png', dpi=100, bbox_inches='tight')
plt.show()
image_binarisee.save('results/image_binarisee.png')
print("✓ Image sauvegardée : results/image_binarisee.png")
print(f"  Seuil utilisé : {seuil}")

# ===== PARTIE 6 : Détection des contours =====
print("\n[Partie 6] Détection des contours")
image_contours = image_gris.filter(ImageFilter.FIND_EDGES)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image_gris, cmap='gray')
plt.title("Image en Niveaux de Gris")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_contours, cmap='gray')
plt.title("Détection des Contours")
plt.axis("off")

plt.tight_layout()
plt.savefig('results/partie6_comparaison.png', dpi=100, bbox_inches='tight')
plt.show()
image_contours.save('results/image_contours.png')
print("✓ Image sauvegardée : results/image_contours.png")
print("  Filtre utilisé : ImageFilter.FIND_EDGES")

# ===== PARTIE 7 : Filtrage et débruitage (Flou gaussien) =====
print("\n[Partie 7] Filtrage - Flou gaussien")
rayons = [1, 2, 3]

# S'assurer que l'image est en mode RGB pour le filtre
if image.mode != 'RGB':
    image_rgb = image.convert('RGB')
else:
    image_rgb = image

images_floues = [image_rgb.filter(ImageFilter.GaussianBlur(r)) for r in rayons]

plt.figure(figsize=(15, 5))
plt.subplot(1, 4, 1)
plt.imshow(image_rgb)
plt.title("Image Originale")
plt.axis("off")

for i, (img_floue, rayon) in enumerate(zip(images_floues, rayons), start=2):
    plt.subplot(1, 4, i)
    plt.imshow(img_floue)
    plt.title(f"Flou Gaussien (r={rayon})")
    plt.axis("off")

plt.tight_layout()
plt.savefig('results/partie7_comparaison.png', dpi=100, bbox_inches='tight')
plt.show()

# Sauvegarder le flou avec rayon = 2
images_floues[1].save('results/image_flou_gaussien.png')
print("✓ Image sauvegardée : results/image_flou_gaussien.png")
print(f"  Rayons testés : {rayons}")

# ===== PARTIE 8 : Histogramme de l'image =====
print("\n[Partie 8] Histogramme de l'image")
histogramme = image_gris.histogram()

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image_gris, cmap='gray')
plt.title("Image en Niveaux de Gris")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.plot(histogramme, color='black')
plt.title("Histogramme de l'Image")
plt.xlabel("Niveau de gris (0-255)")
plt.ylabel("Nombre de pixels")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/partie8_histogramme.png', dpi=100, bbox_inches='tight')
plt.show()
print("✓ Histogramme sauvegardé : results/partie8_histogramme.png")

# ===== PARTIE 9 : Égalisation de l'histogramme =====
print("\n[Partie 9] Égalisation de l'histogramme")
image_egalisee = ImageOps.equalize(image_gris)
histogramme_egalise = image_egalisee.histogram()

# Comparaison des images
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(image_gris, cmap='gray')
plt.title("Image Originale (Niveaux de Gris)")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_egalisee, cmap='gray')
plt.title("Image Égalisée")
plt.axis("off")

plt.tight_layout()
plt.savefig('results/partie9_comparaison_images.png', dpi=100, bbox_inches='tight')
plt.show()

# Comparaison des histogrammes
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(histogramme, color='blue')
plt.title("Histogramme Original")
plt.xlabel("Niveau de gris (0-255)")
plt.ylabel("Nombre de pixels")
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(histogramme_egalise, color='red')
plt.title("Histogramme Égalisé")
plt.xlabel("Niveau de gris (0-255)")
plt.ylabel("Nombre de pixels")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/partie9_comparaison_histogrammes.png', dpi=100, bbox_inches='tight')
plt.show()

image_egalisee.save('results/image_egalisee.png')
print("✓ Image sauvegardée : results/image_egalisee.png")
print("✓ Comparaisons sauvegardées dans results/")

print("\n" + "=" * 60)
print("TP TERMINÉ !")
print("=" * 60)
print("\nTous les résultats sont dans le dossier 'results/'")
print("\nRésumé des transformations :")
print("  • Partie 1 : Lecture et affichage")
print("  • Partie 2 : Redimensionnement (200x200)")
print("  • Partie 3 : Augmentation luminosité (facteur 1.5)")
print("  • Partie 4 : Conversion niveaux de gris")
print("  • Partie 5 : Binarisation (seuil 128)")
print("  • Partie 6 : Détection des contours")
print("  • Partie 7 : Flou gaussien (rayons 1, 2, 3)")
print("  • Partie 8 : Histogramme")
print("  • Partie 9 : Égalisation d'histogramme")
print("\n✓ Toutes les images sont sauvegardées !")
