# 📦 PI-THON Project Structure (EN)

This document describes the organization of the PI-THON project, structured with two separate branches for each language.

---

## 🗂️ General Organization

- **`main` branch** → French version (original project)
- **`EN` branch** → English version (translated project)

Each branch contains its own source code, documentation, and resources.

---

## 📌 Typical Branch Structure

```
pi-thon/
├── README.md               # Main README (FR or EN depending on branch)
├── sources/                # Source code
│   ├── main.py
│   ├── display.py
│   ├── utils.py
│   └── estimation_methods/
│       ├── monte_carlo.py
│       ├── collisions.py
│       ├── machin_formula.py
│       ├── pendulum.py
│       ├── buffon.py
│       ├── archimedes.py
│       ├── nilakantha.py
│       ├── integration_approximation.py
│       ├── ramanujan.py
│       ├── gauss.py
│       ├── leibniz.py
│       ├── chudnovsky.py
│       ├── borwein.py
├── docs/                   # Technical documentation
│   └── project_structure.md
├── data/                   # Resources and generated files
│   ├── pi_reference.txt
│   ├── logo.png
│   ├── Iosevka_fixed.ttf
│   └── pi_estimations/
├── licence.txt             # GPL v3+ License
├── requirements.txt        # Python library requirements
├── presentation.pdf        # Project summary presentation
```

---

## 📌 Details

- The **EN branch** is a full English translation of the project:
  - User interface,
  - Code comments,
  - Documentation.

- Both branches share the same code logic and folder structure,
  but are maintained separately for clarity and ease of use.

---

## 🚀 Purpose

This branch-based structure allows to:

✅ Keep language versions independent,  
✅ Avoid duplicating everything inside one branch,  
✅ Facilitate international use and contributions.
