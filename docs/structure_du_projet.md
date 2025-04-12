# 📂 Structuration du Projet PI-THON

Ce document décrit l'organisation des fichiers et dossiers de **PI-THON**

---

## 📌 Structure Générale

Le projet est organisé de la manière suivante :

```
pi-thon/
│── README.md                  # Documentation principale
│── licence.txt                # Licence du projet (GPL v3+)
│── presentation.pdf           # Présentation synthétique du projet (4 pages)
│── requirements.txt           # Liste des bibliothèques Python nécessaires
│
├── sources/                   # 📌 Code source du projet
│   ├── main.py                # Fichier principal du programme
│   ├── affichage.py           # Gestion de l'affichage avec Pygame
│   ├── utils.py               # Fonctions utilitaires
│   ├── methodes_estimation/   # 📌 Implémentation des différentes méthodes d'estimation de π
│   │   ├── monte_carlo.py
│   │   ├── collisions.py
│   │   ├── formule_de_machin.py
│   │   ├── pendule.py
│   │   ├── buffon.py
│   │   ├── archimede.py
│   │   ├── nilakantha.py
│   │   ├── approximation_integration.py
│   │   ├── ramanujan.py
│   │   ├── gauss.py
│   │   ├── leibniz.py
│   │   ├── chudnovsky.py
│   │   ├── borwein.py
│
├── docs/                      # 📌 Documentation technique
│   ├── structure_du_projet.md # Explication de la structuration du projet
│
├── data/                      # 📌 Ressources et fichiers générés
│   ├── pi_reference.txt       # Décimales de référence pour vérification
│   ├── logo.png               # Logo du projet
│   ├── Iosevka_fixed.ttf      # Police utilisée dans l'interface
│   ├── pi_estimations/        # 📌 Résultats générés par le programme (fichiers .txt)
```

---

## 📌 Explication des Dossiers

### **📁 `sources/` – Code source du projet**
Ce dossier contient **tout le code Python**, y compris **`main.py`**, qui est le point d’entrée du programme.  

📌 **Organisation interne :**
- `main.py` → Fichier principal du programme.
- `affichage.py` → Gestion de l'interface et du menu avec **Pygame**.
- `utils.py` → Fonctions utilitaires (gestion des événements, enregistrement des résultats, etc.).
- `methodes_estimation/` → Implémentation des différentes **méthodes d'estimation de π**.

---

### **📁 `docs/` – Documentation technique**
Ce dossier contient **les documents explicatifs** du projet :
- `structure_du_projet.md` → Présentation de l'organisation des fichiers et leur rôle.

---

### **📁 `data/` – Ressources et fichiers générés**
Ce dossier contient :
- `pi_reference.txt` → Décimales de référence pour vérifier l'exactitude des calculs.
- `logo.png` → Logo utilisé pour pygame qui est juste une image de pi, ce n'est pas le vrai logo du projet.
- `Iosevka_fixed.ttf` → Police utilisée pour l'affichage.
- `pi_estimations/` → Contient **les fichiers `.txt` générés par le programme**, stockant les valeurs de π calculées.
