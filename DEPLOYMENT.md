# Biométrie Studio - Traitement d'Images

Application web de traitement d'images avec Flask et PIL.

## Déploiement

Cette application peut être déployée sur Render, PythonAnywhere, ou Railway.

### Pour Render.com

1. Push le code sur GitHub
2. Connectez-vous à Render
3. Créez un nouveau "Web Service"
4. Sélectionnez votre repo
5. Render détecte automatiquement Python

### Pour PythonAnywhere

1. Créez un compte sur pythonanywhere.com
2. Uploadez les fichiers
3. Configurez une application Flask
4. Spécifiez `web_app.py` comme fichier principal

## Variables d'Environnement

Aucune variable d'environnement requise pour la version de base.

## Structure

```
├── web_app.py          # Application Flask principale
├── requirements.txt    # Dépendances Python
├── templates/          # Templates HTML
├── static/            # CSS, JS, images
├── uploads/           # Images uploadées (créé automatiquement)
└── results/           # Résultats (créé automatiquement)
```

## Commande de Démarrage

```bash
python web_app.py
```
