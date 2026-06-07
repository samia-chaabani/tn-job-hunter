import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
import os
import PyPDF2

# API Keys
os.environ["TAVILY_API_KEY"] = "your_tavily_key"
GROQ_API_KEY = "your_groq_key"

# Setup
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
search_tool = TavilySearchResults(max_results=10)

# Domaines complets
DOMAINES = {
    "🖥️ Informatique": [
        "Développement Web", "Développement Mobile Android",
        "Spring Boot / Java Backend", "Data Science / Machine Learning",
        "Intelligence Artificielle", "Cybersécurité",
        "DevOps / Cloud", "Systèmes & Réseaux",
        "Base de données / SQL", "Full Stack Development"
    ],
    "⚙️ Génie Mécanique": [
        "Conception mécanique / CAO", "Maintenance industrielle",
        "Génie des procédés", "Automatisme / Robotique",
        "Bureau d'études mécanique"
    ],
    "⚡ Génie Électrique": [
        "Électronique", "Électrotechnique",
        "Automatisme industriel", "Énergies renouvelables",
        "Instrumentation et mesure"
    ],
    "🏗️ Génie Civil": [
        "Travaux publics", "Structure et béton armé",
        "Topographie", "Urbanisme et aménagement"
    ],
    "🧪 Génie Chimique": [
        "Chimie industrielle", "Génie des procédés chimiques",
        "Contrôle qualité", "Environnement et sécurité"
    ],
    "📡 Télécommunications": [
        "Réseaux télécoms", "Fibre optique",
        "5G et technologies mobiles", "Systèmes embarqués"
    ],
    "💼 Génie Industriel": [
        "Lean Manufacturing", "Supply Chain / Logistique",
        "Qualité / ISO", "Management de production"
    ],
}

# Sites de recherche
SITES = [
    "site:linkedin.com",
    "site:tanitjobs.com",
    "site:keejob.com",
    "site:indeed.com",
    "site:welcometothejungle.com",
]

# Interface
st.set_page_config(page_title="TN Job Hunter", page_icon="🇹🇳", layout="wide")
st.title("🇹🇳 TN Job Hunter")
st.write("Agent IA qui cherche les meilleures offres de stage en Tunisie pour toi!")

# CV Upload
st.subheader("📄 Upload ton CV (optionnel)")
cv_file = st.file_uploader("Uploade ton CV (PDF)", type=["pdf"])
cv_text = ""
if cv_file:
    reader = PyPDF2.PdfReader(cv_file)
    for page in reader.pages:
        cv_text += page.extract_text()
    st.success("✅ CV chargé!")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    filiere = st.selectbox("🎓 Filière:", list(DOMAINES.keys()))

with col2:
    domaine = st.selectbox("🔧 Spécialité:", DOMAINES[filiere])

with col3:
    ville = st.selectbox("📍 Ville:", [
        "Tunis", "Ariana", "Ben Arous", "Sfax",
        "Sousse", "Monastir", "Bizerte", "Nabeul",
        "Toute la Tunisie"
    ])

type_stage = st.radio(
    "Type de stage:",
    ["Stage d'été", "Stage PFA", "Stage PFE", "Tous les types"],
    horizontal=True
)

if st.button("🔍 Chercher les stages", use_container_width=True):
    with st.spinner("L'agent cherche sur plusieurs sites..."):

        all_results = []
        progress = st.progress(0)

        for i, site in enumerate(SITES):
            try:
                queries = [
                    f"stage été 2026 {domaine} {ville} Tunisie disponible postuler {site}",
                    f"offre stage 2026 {domaine} Tunisie juin juillet août {site}",
                ]
                for q in queries:
                    try:
                        res = search_tool.invoke(q)
                        all_results.extend(res)
                    except:
                        pass
            except:
                pass
            progress.progress((i + 1) / len(SITES))

        # Remove duplicates
        seen = set()
        results = []
        for r in all_results:
            if r['url'] not in seen:
                seen.add(r['url'])
                results.append(r)

        # Analyze with AI
        context = "\n".join([f"- {r['url']}: {r['content']}" for r in results[:15]])
        cv_section = f"\n\nCV du candidat:\n{cv_text[:2000]}" if cv_text else ""

        prompt = f"""Tu es un assistant qui aide les étudiants tunisiens à trouver des stages.

Voici les résultats pour un stage en {domaine} à {ville} ({type_stage}):
{context}
{cv_section}

IMPORTANT: Nous sommes en 2026. Ignore les offres de 2024 et 2025.

Pour chaque offre trouve:
- 🏢 Entreprise
- 📝 Description
- 🛠️ Compétences requises
- 🔗 Lien
{"- ✅ Points forts de ton CV pour ce poste" if cv_text else ""}
{"- ⚠️ Ce qui manque dans ton CV" if cv_text else ""}

Si aucune offre 2026 trouvée, dis-le et suggère comment chercher autrement.
Réponds en français."""

        response = llm.invoke([HumanMessage(content=prompt)])

        st.success(f"✅ Résultats pour: {domaine} — {ville}")
        st.write(response.content)

        with st.expander("🔗 Toutes les sources trouvées"):
            for r in results:
                st.write(f"- [{r['url']}]({r['url']})")