
from PIL import Image
import matplotlib.pyplot as plt

chemin_image = 'lena_color.gif'
image = Image.open(chemin_image)

plt.subplot(1, 1, 1)
plt.imshow(image)
plt.title("Image Originale")
plt.axis("off")
plt.show()

image.save('image_originale.png')
print("Image sauvegardée sous 'image_originale.png'")


nouvelle_taille = (200, 200) 
image_redimensionnee = image.resize(nouvelle_taille)


plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("Image Originale")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_redimensionnee)
plt.title("Image Redimensionnée)")
plt.axis("off")

plt.show()

image_redimensionnee.save('image_redimensionnee.png')
print("Image redimensionnée sauvegardée sous 'image_redimensionnee.png'")