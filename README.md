# 🇹🇳 TN Job Hunter — Agent IA

> Agent intelligent qui cherche automatiquement les meilleures offres 
> de stage en Tunisie et analyse la compatibilité avec ton CV.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-red)
![LangChain](https://img.shields.io/badge/LangChain-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-orange)

---

## C'est quoi ?

**TN Job Hunter** est une application IA qui automatise la recherche de stages 
en Tunisie. Elle cherche sur 5 plateformes d'emploi simultanément, filtre les 
offres récentes et analyse la compatibilité avec le CV du candidat.

---

## Démo

1. Uploade ton CV (PDF)
2. Choisis ta filière, spécialité et ville
3. Clique sur **Rechercher**
4. Reçois les offres + analyse de ton CV pour chaque poste

---

## Architecture
┌─────────────────────────────────────┐
│              UTILISATEUR             │
│         localhost:8501               │
└────────────────┬────────────────────┘
│
┌────────────────▼────────────────────┐
│         INTERFACE STREAMLIT          │
│   - Sélection filière / ville        │
│   - Upload CV (PDF)                  │
│   - Affichage des résultats          │
└────────────────┬────────────────────┘
│
┌────────────────▼────────────────────┐
│           AGENT IA                   │
│                                      │
│  ÉTAPE 1 — RECHERCHE                 │
│  Tavily Search → 5 sites x 2 queries │
│  LinkedIn, Tanitjobs, Keejob...      │
│                                      │
│  ÉTAPE 2 — DÉDUPLICATION             │
│  Suppression des doublons par URL    │
│                                      │
│  ÉTAPE 3 — ANALYSE IA                │
│  Groq LLaMA 3.3 analyse les offres   │
│  + compatibilité avec le CV          │
└──────────┬──────────────┬───────────┘
│              │
┌──────────▼──────┐  ┌────▼──────────┐
│  Tavily Search  │  │   Groq API    │
│  (recherche web)│  │ LLaMA 3.3 70B │
│  1000 req/mois  │  │ gratuit       │
└─────────────────┘  └───────────────┘

---

## Fonctionnalités

- 🔍 Recherche automatique sur 5 plateformes d'emploi
- 🎓 Filtrage par filière, spécialité, ville et type de stage
- 📄 Analyse CV et compatibilité avec chaque offre
- ✅ Points forts identifiés par rapport à chaque poste
- ⚠️ Points à améliorer pour maximiser les chances
- 🔗 Liens directs vers les offres

---

## Stack Technique

| Couche | Technologie | Pourquoi |
|--------|------------|---------|
| Interface | Streamlit | Simple, rapide, Python natif |
| Agent IA | LangChain | Orchestration des outils IA |
| LLM | Groq LLaMA 3.3 70B | Gratuit, rapide, performant |
| Recherche | Tavily Search API | Recherche web optimisée pour IA |
| PDF | PyPDF2 | Extraction de texte depuis CV |

---

## Structure du projet
tn-job-hunter/
├── app.py          # Application principale Streamlit
├── README.md       # Documentation
└── .gitignore      # Fichiers exclus de GitHub

---

## Installation

```bash
pip install streamlit langchain-groq langchain-community tavily-python pypdf2
```

---

## Configuration

Remplace les clés API dans `app.py`:
```python
os.environ["TAVILY_API_KEY"] = "your_tavily_key"
GROQ_API_KEY = "your_groq_key"
```

Obtenir les clés gratuitement:
- Groq API: [console.groq.com](https://console.groq.com)
- Tavily API: [app.tavily.com](https://app.tavily.com)

---

## Lancement

```bash
streamlit run app.py
```

---

## Coût

| Composant | Coût |
|-----------|------|
| Groq LLaMA 3.3 | 0$ — gratuit |
| Tavily Search | 0$ — 1000 req/mois |
| Streamlit | 0$ — open source |
| **Total** | **0$** |

---

## Auteure

**Samia Chaabani**  
Étudiante en Génie Informatique — ENICarthage, Tunisie  
Samia.chaabani@enicar.ucar.tn  
[linkedin.com/in/samia-chaabani](https://linkedin.com/in/samia-chaabani)  
[github.com/samia-chaabani](https://github.com/samia-chaabani)
