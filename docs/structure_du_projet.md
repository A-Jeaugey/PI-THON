# 📦 Structure du projet PI-THON (🇫🇷)

Ce document décrit l’organisation du projet PI-THON, structuré avec deux branches séparées pour chaque langue.

---

## 🗂️ Organisation générale

- **Branche `main`** → Version française (projet original)
- **Branche `EN`** → Version anglaise (projet traduit)

Chaque branche contient son propre code source, sa documentation et ses ressources.

---

## 📌 Structure typique d'une branche

```
pi-thon/
├── README.md               # README principal (FR ou EN selon la branche)
├── sources/                # Code source
│   ├── main.py
│   ├── affichage.py (ou display.py)
│   ├── utils.py
│   └── methodes_estimation/
│       ├── monte_carlo.py
│       ├── collisions.py
│       ├── formule_de_machin.py (ou machin_formula.py)
│       ├── pendule.py
│       ├── buffon.py
│       ├── archimede.py
│       ├── nilakantha.py
│       ├── approximation_integration.py
│       ├── ramanujan.py
│       ├── gauss.py
│       ├── leibniz.py
│       ├── chudnovsky.py
│       ├── borwein.py
├── docs/                   # Documentation technique
│   └── structure_du_projet.md (ou project_structure.md)
├── data/                   # Ressources et fichiers générés
│   ├── pi_reference.txt
│   ├── logo.png
│   ├── Iosevka_fixed.ttf
│   └── pi_estimations/
├── licence.txt             # Licence GPL v3+
├── requirements.txt        # Bibliothèques Python nécessaires
├── presentation.pdf        # Présentation synthétique du projet
```

---

## 📌 Détails

- La **branche EN** est une traduction complète du projet en anglais :
  - Interface utilisateur,
  - Commentaires dans le code,
  - Documentation.

- Les deux branches partagent la même logique et structure de code,
  mais sont maintenues séparément pour plus de clarté et de simplicité.

---

## 🚀 Objectif

Cette structure par branches permet de :

✅ Garder les versions linguistiques indépendantes,  
✅ Éviter de tout dupliquer dans une seule branche,  
✅ Faciliter l’utilisation et les contributions internationales.
