from __future__ import annotations

import re
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).parent
INFO_DIR = ROOT / "Info"
DATA_DIR = ROOT / "data"
PHOTO_PATH = INFO_DIR / "Foto JOPEDSAN.jpg"
PROJECTS_PATH = INFO_DIR / "proyectos_IBV_experiencia_investigadora.md"
CV_TEXT_PATH = INFO_DIR / "Jose_Pedrero_CV_Data_Scientist.txt"
CV_PDF_PATH = INFO_DIR / "CV_Jose_Pedrero_Docencia.pdf"
DEVELOP_CV_PDF_PATH = INFO_DIR / "CV_Jose_Pedrero_Develop.pdf"
SCHOLAR_PUBLICATIONS_PATH = DATA_DIR / "scholar_publications.csv"
MANUAL_PUBLICATIONS_PATH = DATA_DIR / "manual_publications.csv"
SCHOLAR_METRICS_PATH = DATA_DIR / "scholar_metrics.json"
VENUE_QUALITY_PATH = DATA_DIR / "venue_quality.csv"


PROFILE = {
    "name": "Jose Francisco Pedrero Sánchez",
    "role": "Data Scientist · ML Engineer · Research Technologist",
    "location": "Valencia, Spain",
    "email": "jpedrerosanchez@gmail.com",
    "phone": "+34 664 235 553",
    "linkedin": "https://www.linkedin.com/in/jos%C3%A9-francisco-pedrero-s%C3%A1nchez-454a40a0/",
    "researchgate": "https://www.researchgate.net/profile/Jose-Francisco-Pedrero-Sanchez",
    "scholar": "https://scholar.google.es/citations?user=IsAjXHwAAAAJ",
    "summary": (
        "PhD in Health and Wellbeing Technologies from Universitat Politècnica de València, "
        "with applied experience in advanced analytics, signal processing, statistical validation "
        "and transferable technology for clinical and industrial environments."
    ),
    "metrics": {
        "Citations": 213,
        "h-index": 8,
        "i10-index": 8,
        "Years at IBV": 10,
    },
}


EDUCATION = [
    {
        "degree": "PhD in Health and Wellbeing Technologies",
        "institution": "Universitat Politècnica de València",
        "year": "2023",
        "note": "Cum Laude",
    },
    {
        "degree": "MSc in Electronic Systems Engineering",
        "institution": "Universitat Politècnica de València",
        "year": "2015",
        "note": "",
    },
    {
        "degree": "BSc in Industrial Engineering - Industrial Electronics",
        "institution": "Universitat Politècnica de València",
        "year": "2012",
        "note": "",
    },
    {
        "degree": "Vocational Training - Electronics",
        "institution": "Col Juan Comenius",
        "year": "2005-2009",
        "note": "Advanced and intermediate training",
    },
]


EXPERIENCE = [
    {
        "company": "Instituto de Biomecánica de Valencia (IBV)",
        "role": "Research Technologist",
        "period": "2016 - 2026",
        "highlights": [
            "Functional assessment procedures using portable technologies.",
            "Digital health and active ageing: mobility, frailty and fall risk assessment.",
            "Ergonomics and occupational health: biomechanical labs, assistive devices and exoskeleton validation.",
            "Technology transfer, patents, ethics committees, teaching and supervision.",
        ],
    },
    {
        "company": "ai2 - Institute of Automation and Industrial Computing",
        "role": "Research Assistant",
        "period": "2009",
        "highlights": ["Mobile robotics programming at Universitat Politècnica de València."],
    },
    {
        "company": "Navtival S.L.U.",
        "role": "SAT Services - FERMAX",
        "period": "2008",
        "highlights": ["Technical support services in Valencia."],
    },
    {
        "company": "Electrónica R. Martí S.L.",
        "role": "Electronic Equipment Installation and Servicing Technician",
        "period": "2007",
        "highlights": ["Installation and servicing of electronic equipment."],
    },
]


SKILLS = {
    "Data Science & ML": [
        "Python",
        "R",
        "Data analysis",
        "Machine Learning",
        "Deep Learning",
        "Statistical modeling",
        "Experimental design",
        "PyTorch",
        "TensorFlow/Keras",
    ],
    "Signals, Vision & Biomechanics": [
        "Time series",
        "Signal processing",
        "Feature extraction",
        "Computer Vision",
        "OpenCV",
        "Human pose estimation",
        "Wearable sensors",
        "Functional assessment",
    ],
    "LLM & Knowledge Systems": [
        "LLMs",
        "VLMs",
        "NLP",
        "RAG",
        "GraphRAG",
        "LangChain",
        "LangGraph",
        "Tool calling",
        "AI agents",
    ],
    "Data Engineering & MLOps": [
        "Docker",
        "Qdrant",
        "ChromaDB",
        "FAISS",
        "Ollama",
        "Reproducible pipelines",
        "Data lifecycle",
        "Traceability",
        "Basic MLOps",
    ],
    "Professional Strengths": [
        "Analytical thinking",
        "Problem solving",
        "Effective communication",
        "Adaptability",
        "Teamwork",
        "Organization",
        "Multidisciplinary collaboration",
    ],
}


SELECTED_WORKS = [
    {
        "title": "AI document intelligence systems",
        "summary": (
            "LLM, VLM, NLP, RAG and GraphRAG workflows for technical and clinical document "
            "analysis, semantic search, information extraction, summarization and knowledge discovery."
        ),
        "tags": ["LLMs", "RAG", "GraphRAG", "Vector databases", "Tool calling"],
    },
    {
        "title": "Knowledge automation with AI agents",
        "summary": (
            "Automated knowledge-management workflows combining LLM orchestration, tool calling, "
            "vector stores and structured retrieval over specialized documentation."
        ),
        "tags": ["LangChain", "LangGraph", "Qdrant", "ChromaDB", "Ollama"],
    },
    {
        "title": "Functional mobility assessment pipelines",
        "summary": (
            "Analytics pipelines using wearable and smartphone sensors to assess gait, balance, "
            "sit-to-stand performance, fall risk and neurodegenerative disease impact."
        ),
        "tags": ["Python", "Time series", "Signal processing", "Clinical validation"],
    },
    {
        "title": "Computer vision for biomechanics and ergonomics",
        "summary": (
            "Computer-vision workflows for human movement analysis, ergonomic assessment and "
            "biomechanical validation of assistive devices and exoskeletons."
        ),
        "tags": ["OpenCV", "Computer Vision", "Human pose", "Ergonomics"],
    },
]


PUBLICATIONS = [
    {
        "journal": "BMJ Open",
        "theme": "Digital health / Clinical assessment",
        "quartile": "To be completed",
        "count": 1,
    },
    {
        "journal": "Frontiers in Aging Neuroscience",
        "theme": "Active ageing / Frailty",
        "quartile": "To be completed",
        "count": 1,
    },
    {
        "journal": "Biomedical Signal Processing and Control",
        "theme": "Signals / Biomechanics",
        "quartile": "To be completed",
        "count": 1,
    },
]


EXCLUDED_PUBLICATION_TITLES = {
    "A Case Study with OWAS",
    "Ergonomic assessment with Artificial Vision and Neural Networks",
}


EXTRA_PROJECTS = [
    {
        "name": "ANESTECH",
        "full_title": (
            "Estratificación del riesgo preanestésico a través de la valoración remota "
            "de pacientes utilizando herramientas basadas en IA ciberseguras."
        ),
        "duration": "01/11/2025 - 31/12/2027",
        "type": "Proyectos Estratégicos en Cooperación",
        "year": "2025",
        "funder": "Agencia Valenciana de la Innovación (AVI) / IVACE+i Innovación / FEDER",
        "relationship": "Participante",
        "start": "01/11/2025",
        "end": "31/12/2027",
        "category": "Inteligencia Artificial / Salud digital / Ciberseguridad",
        "country": "España",
        "notes": (
            "Metodología de evaluación preanestésica remota mediante smartphone, análisis de "
            "movimiento y reconstrucción 3D con IA, interoperabilidad con HCE y análisis de "
            "ciberseguridad para datos clínicos."
        ),
        "url": "https://www.ibv.org/proyecto/anestech-estratificacion-del-riesgo-preanestesico-a-traves-de-la-valoracion-remota-de-pacientes-utilizando-herramientas-basadas-en-ia-ciberseguras/",
        "reference": "INNEST/2025/311",
    },
    {
        "name": "GUARDIANES",
        "full_title": "Red de Excelencia en Tecnologías de Inteligencia Artificial para la Seguridad y la Defensa.",
        "duration": "01/01/2026 - 31/12/2028",
        "type": "Red de Excelencia CERVERA",
        "year": "2026",
        "funder": "CDTI / Ministerio de Ciencia, Innovación y Universidades",
        "relationship": "Participante",
        "start": "01/01/2026",
        "end": "31/12/2028",
        "category": "Inteligencia Artificial / Seguridad / Defensa",
        "country": "España",
        "notes": (
            "Red estratégica de I+D para IA aplicada a seguridad y defensa, centrada en datos, "
            "computación, algoritmia, simulación y gobierno ético de la IA."
        ),
        "url": "https://www.ibv.org/proyecto/guardianes-red-de-excelencia-en-tecnologias-de-inteligencia-artificial-para-la-seguridad-y-la-defensa/",
        "reference": "EXP 00180232 / CER-20251017",
    },
    {
        "name": "Fall-in-Age",
        "full_title": "Innovative Training for Technology-based Frailty and Falls Management.",
        "duration": "2018 - 2020",
        "type": "Erasmus+ KA203",
        "year": "2018",
        "funder": "Erasmus+",
        "relationship": "Participante",
        "start": "01/01/2018",
        "end": "31/12/2020",
        "category": "Proyecto europeo / Fragilidad / Prevención de caídas / Formación",
        "country": "Internacional",
        "notes": (
            "Desarrollo e implementación de un curso online abierto para estudiantes, especialistas "
            "y profesionales sanitarios sobre tecnologías biomecánicas aplicadas a la valoración de "
            "fragilidad y riesgo de caídas en personas mayores."
        ),
        "url": "https://fallinage.tecnico.ulisboa.pt/project.html#",
        "reference": "2018-1-PT01-KA203-047343",
    },
]


AWARDS = [
    {
        "title": "Caballe-Gomar Research Award, 4th Edition",
        "issuer": "Faculty of Physiotherapy, Universitat de Valencia",
        "date": "Jun. 2020",
        "associated_with": "Institute of Biomechanics of Valencia (IBV)",
        "work": "Mobility assessment in people with Alzheimer Disease using smartphone sensors",
        "description": (
            "Recognition as co-author of the awarded work by the Faculty of Physiotherapy "
            "through the 4th edition of the Caballe-Gomar Research Award."
        ),
    }
]


TEACHING_PROPOSAL = {
    "headline": "Applied, measurable biomechanics transferable to digital environments",
    "summary": (
        "Teaching proposal designed to help students reason biomechanically through real cases: "
        "functional mobility, balance, gait, fall risk, clinical assessment and wearable "
        "health technologies."
    ),
    "pillars": [
        {
            "title": "Applied biomechanics",
            "items": [
                "Analysis of human movement and function.",
                "Gait, balance, sit-to-stand, mobility and fall risk.",
                "Clinical interpretation of biomechanical variables.",
            ],
        },
        {
            "title": "Clinical Biomechanical Assessment Master's teaching",
            "items": [
                (
                    'Teaching in the <a href="https://master.ibv.org/" target="_blank">'
                    "IBV Master's degree in Clinical Biomechanical Assessment</a>."
                ),
                "Instrumental techniques for biomechanical analysis.",
                "Biomechanical signal analysis techniques and statistical techniques in biomechanics.",
            ],
        },
        {
            "title": "Technology and transfer",
            "items": [
                "Wearable sensors, smartphones, video and signal analysis.",
                "Cases derived from applied research and IBV projects.",
                "Bridge between laboratory, clinic, industry and the virtual classroom.",
            ],
        },
    ],
    "activities": [
        {
            "name": "CAE 1 - Biomechanical reading of a functional case",
            "goal": "Identify phases, variables and compensations in a mobility task.",
            "evidence": "Short report with a biomechanical hypothesis and clinical justification.",
        },
        {
            "name": "CAE 2 - Remote mini-lab with video or smartphone",
            "goal": "Extract observable variables from gait, balance or sit-to-stand tasks.",
            "evidence": "Variable table, interpretation and methodological limitations.",
        },
        {
            "name": "CAE 3 - Risk assessment and decision-making",
            "goal": "Relate biomechanical data to functionality, risk and intervention proposals.",
            "evidence": "Resolved case with a reasoning and professional communication rubric.",
        },
        {
            "name": "CAE 4 - Transfer and innovation",
            "goal": "Design a teaching, clinical or technological solution based on applied biomechanics.",
            "evidence": "Defensible final proposal with validity, usefulness and ethics criteria.",
        },
    ],
    "interview_points": [
        "Direct experience in applied biomechanics, digital health and functional assessment.",
        "Ability to transform research into assessable teaching activities.",
        "Hybrid profile: teacher, applied researcher and technologist.",
        "Natural fit with continuous assessment, autonomous learning and real cases.",
    ],
}


st.set_page_config(
    page_title="Jose Pedrero | CV Dashboard",
    page_icon="JP",
    layout="wide",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
          --ink: #edf7f5;
          --muted: #a9bdc0;
          --line: #263b40;
          --panel: #101d21;
          --accent: #33c7ba;
          --accent-2: #ffb35c;
          --soft: #193338;
        }
        .stApp {
          background:
            radial-gradient(circle at 12% 8%, rgba(51, 199, 186, .16), transparent 30rem),
            radial-gradient(circle at 82% 0%, rgba(255, 179, 92, .10), transparent 24rem),
            linear-gradient(180deg, #071113 0%, #0c171a 48%, #111a1d 100%);
          color: var(--ink);
        }
        .block-container {
          padding-top: 2rem;
          padding-bottom: 2rem;
          max-width: 1380px;
        }
        h1, h2, h3 {
          letter-spacing: 0;
        }
        .hero {
          display: grid;
          grid-template-columns: 170px minmax(0, 1fr);
          gap: 1.4rem;
          align-items: center;
          padding: 1.4rem;
          border: 1px solid var(--line);
          border-radius: 8px;
          background: rgba(16, 29, 33, .92);
          box-shadow: 0 18px 48px rgba(0, 0, 0, .32);
        }
        .hero img {
          width: 150px;
          height: 150px;
          object-fit: cover;
          border-radius: 8px;
          border: 1px solid #39565d;
        }
        .hero-title {
          font-size: clamp(2.1rem, 4vw, 4.2rem);
          line-height: 1;
          margin: 0 0 .55rem 0;
          color: var(--ink);
        }
        .hero-role {
          margin: 0 0 .8rem 0;
          color: var(--accent);
          font-weight: 700;
          font-size: 1.05rem;
        }
        .hero-summary {
          max-width: 980px;
          color: #c9d9dc;
          font-size: 1rem;
          line-height: 1.65;
          margin: 0;
        }
        .contact-row {
          display: flex;
          flex-wrap: wrap;
          gap: .55rem;
          margin-top: .95rem;
        }
        .contact-pill {
          border: 1px solid var(--line);
          background: var(--soft);
          border-radius: 999px;
          padding: .38rem .7rem;
          color: #d8e9e8;
          font-size: .86rem;
        }
        .section-title {
          margin-top: .4rem;
          margin-bottom: .25rem;
          font-size: 1.35rem;
          font-weight: 800;
          color: var(--ink);
        }
        .muted {
          color: var(--muted);
        }
        .timeline-item,
        .skill-box,
        .project-card,
        .award-card,
        .teaching-card,
        .activity-card {
          border: 1px solid var(--line);
          border-radius: 8px;
          background: rgba(16, 29, 33, .88);
          padding: 1rem;
          height: 100%;
        }
        .award-card {
          border-color: rgba(255, 179, 92, .42);
          background: linear-gradient(135deg, rgba(255, 179, 92, .12), rgba(16, 29, 33, .92));
        }
        .teaching-card {
          border-color: rgba(51, 199, 186, .42);
          background: linear-gradient(135deg, rgba(51, 199, 186, .12), rgba(16, 29, 33, .92));
        }
        .activity-card {
          background: rgba(20, 39, 45, .88);
        }
        .timeline-date {
          color: var(--accent-2);
          font-weight: 800;
          font-size: .9rem;
        }
        .timeline-title {
          font-size: 1.08rem;
          font-weight: 800;
          margin: .15rem 0;
        }
        .tag {
          display: inline-block;
          margin: .16rem .22rem .16rem 0;
          padding: .22rem .48rem;
          border-radius: 999px;
          background: #18343a;
          color: #dcefed;
          font-size: .78rem;
          border: 1px solid #2e535a;
        }
        .quality-note {
          color: #c8d7da;
          font-size: .9rem;
          line-height: 1.55;
        }
        [data-testid="stMetric"] {
          background: rgba(16, 29, 33, .9);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: .8rem 1rem;
        }
        [data-testid="stTabs"] button {
          font-weight: 700;
        }
        a {
          color: #65ddd3;
        }
        @media (max-width: 760px) {
          .hero {
            grid-template-columns: 1fr;
          }
          .hero img {
            width: 120px;
            height: 120px;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def read_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def scholar_metrics() -> dict[str, int]:
    if not SCHOLAR_METRICS_PATH.exists():
        return PROFILE["metrics"]

    metrics = PROFILE["metrics"].copy()
    loaded = json.loads(SCHOLAR_METRICS_PATH.read_text(encoding="utf-8"))
    if "citations_all" in loaded:
        metrics["Citations"] = int(loaded["citations_all"])
    if "h_index_all" in loaded:
        metrics["h-index"] = int(loaded["h_index_all"])
    if "i10_index_all" in loaded:
        metrics["i10-index"] = int(loaded["i10_index_all"])
    return metrics


def scholar_publications() -> pd.DataFrame:
    frames = []
    if SCHOLAR_PUBLICATIONS_PATH.exists():
        frames.append(pd.read_csv(SCHOLAR_PUBLICATIONS_PATH).fillna(""))
    if MANUAL_PUBLICATIONS_PATH.exists():
        frames.append(pd.read_csv(MANUAL_PUBLICATIONS_PATH).fillna(""))
    if frames:
        pubs = pd.concat(frames, ignore_index=True).fillna("")
        return pubs[~pubs["title"].isin(EXCLUDED_PUBLICATION_TITLES)].reset_index(drop=True)

    pubs = pd.DataFrame(PUBLICATIONS)
    pubs["title"] = ""
    pubs["authors"] = ""
    pubs["year"] = ""
    pubs["citations"] = ""
    return pubs


def venue_quality() -> pd.DataFrame:
    if not VENUE_QUALITY_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(VENUE_QUALITY_PATH).fillna("")


def enrich_publications(pubs: pd.DataFrame) -> pd.DataFrame:
    pubs = pubs.copy()
    quality = venue_quality()
    defaults = {
        "clean_venue": "",
        "publication_type": "Unclassified",
        "quartile": "To review",
        "ranking_source": "",
        "ranking_note": "",
        "source_url": "",
    }
    for column, value in defaults.items():
        if column not in pubs:
            pubs[column] = value

    weather_station = pubs["title"].astype(str).str.contains(
        "Desarrollo de una estación meteorológica",
        case=False,
        na=False,
    )
    pubs.loc[weather_station, "journal"] = "Universitat Politècnica de València"
    pubs.loc[weather_station, "year"] = 2012
    pubs.loc[weather_station, "clean_venue"] = "Universitat Politècnica de València"
    pubs.loc[weather_station, "publication_type"] = "Thesis/academic work"
    pubs.loc[weather_station, "quartile"] = "No journal quartile"
    pubs.loc[weather_station, "ranking_source"] = "Academic repository"
    pubs.loc[weather_station, "ranking_note"] = "Trabajo final de carrera realizado en la Universitat Politècnica de València."

    ergonomic_owas = pubs["title"].astype(str).str.contains(
        "Ergonomic assessment with a convolutional neural network",
        case=False,
        na=False,
    )
    pubs.loc[ergonomic_owas, "journal"] = (
        "Proceedings of the 8th International Ergonomics Conference. "
        "ERGONOMICS 2020. Advances in Intelligent Systems and Computing 1313, 65-71"
    )
    pubs.loc[ergonomic_owas, "year"] = 2021
    pubs.loc[ergonomic_owas, "scholar_link"] = "https://link.springer.com/chapter/10.1007/978-3-030-66937-9_8"
    pubs.loc[ergonomic_owas, "clean_venue"] = "Proceedings of the 8th International Ergonomics Conference"
    pubs.loc[ergonomic_owas, "publication_type"] = "Conference paper"
    pubs.loc[ergonomic_owas, "quartile"] = "Conference; no journal quartile"
    pubs.loc[ergonomic_owas, "ranking_source"] = "Springer conference proceedings"
    pubs.loc[ergonomic_owas, "ranking_note"] = (
        "Conference paper in ERGONOMICS 2020, Advances in Intelligent Systems and Computing "
        "vol. 1313, pp. 65-71. DOI: 10.1007/978-3-030-66937-9_8."
    )

    parkinson_smartphone = pubs["title"].astype(str).str.contains(
        "Assessment of functional activities in individuals with Parkinson",
        case=False,
        na=False,
    )
    pubs.loc[parkinson_smartphone, "quartile"] = "Q1"
    pubs.loc[parkinson_smartphone, "ranking_note"] = (
        "Classified as Q1 for the publication record in International Journal of "
        "Environmental Research and Public Health."
    )

    if quality.empty or "journal" not in pubs:
        return pubs

    for index, publication in pubs.iterrows():
        venue = str(publication.get("journal", "")).lower()
        if not venue:
            continue
        matches = quality[quality["match"].str.lower().apply(lambda match: match in venue)]
        if matches.empty:
            continue
        match = matches.iloc[matches["match"].str.len().argmax()]
        for column in defaults:
            pubs.at[index, column] = match.get(column, defaults[column])
    pubs.loc[weather_station, "publication_type"] = "Thesis/academic work"
    pubs.loc[weather_station, "quartile"] = "No journal quartile"
    pubs.loc[weather_station, "ranking_source"] = "Academic repository"
    pubs.loc[weather_station, "ranking_note"] = "Trabajo final de carrera realizado en la Universitat Politècnica de València."
    pubs.loc[ergonomic_owas, "publication_type"] = "Conference paper"
    pubs.loc[ergonomic_owas, "quartile"] = "Conference; no journal quartile"
    pubs.loc[ergonomic_owas, "ranking_source"] = "Springer conference proceedings"
    pubs.loc[ergonomic_owas, "ranking_note"] = (
        "Conference paper in ERGONOMICS 2020, Advances in Intelligent Systems and Computing "
        "vol. 1313, pp. 65-71. DOI: 10.1007/978-3-030-66937-9_8."
    )
    pubs.loc[parkinson_smartphone, "quartile"] = "Q1"
    pubs.loc[parkinson_smartphone, "ranking_note"] = (
        "Classified as Q1 for the publication record in International Journal of "
        "Environmental Research and Public Health."
    )
    for column, value in defaults.items():
        pubs[column] = pubs[column].replace("", value)
    return pubs


def infer_theme(title: str, journal: str) -> str:
    text = f"{title} {journal}".lower()
    if any(word in text for word in ["parkinson", "alzheimer", "frailty", "aging", "falls", "fall risk"]):
        return "Neurodegeneration / Active ageing"
    if any(word in text for word in ["sensor", "smartphone", "portable", "functional mobility"]):
        return "Wearables / Functional assessment"
    if any(word in text for word in ["neural network", "deep", "classification", "artificial vision"]):
        return "AI / Machine learning"
    if any(word in text for word in ["ergonomic", "owas", "biomecánica", "biomechanical"]):
        return "Biomechanics / Ergonomics"
    if any(word in text for word in ["knee", "prosthesis", "clinical", "patient"]):
        return "Clinical follow-up / Medical devices"
    return "Other research outputs"


def parse_projects(path: Path) -> list[dict[str, str]]:
    text = read_file(path)
    blocks = re.split(r"\n-{8,}\n", text)
    projects: list[dict[str, str]] = []

    for block in blocks:
        title_match = re.search(r"^##\s+\d+\.\s+(.+)$", block, re.MULTILINE)
        if not title_match:
            continue

        project = {
            "name": title_match.group(1).strip(),
            "full_title": "",
            "duration": "",
            "type": "",
            "year": "",
            "funder": "",
            "relationship": "",
            "start": "",
            "end": "",
            "category": "",
            "country": "",
            "notes": "",
            "url": "",
            "reference": "",
        }

        full_title = re.search(r"\*\*Título completo:\*\*\s*(.+?)(?=\n\n-|\Z)", block, re.S)
        if full_title:
            project["full_title"] = " ".join(full_title.group(1).split())

        field_map = {
            "Títol del projecte": "name",
            "Durada del projecte": "duration",
            "Tipus de projecte": "type",
            "Any de concessió": "year",
            "Entitat finançadora": "funder",
            "Tipus de relació": "relationship",
            "Inici": "start",
            "Fi": "end",
            "Categoria": "category",
            "País": "country",
            "Observacions": "notes",
        }
        for label, key in field_map.items():
            pattern = rf"-\s+\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n-\s+\*\*|\Z)"
            match = re.search(pattern, block, re.S)
            if match:
                project[key] = " ".join(match.group(1).split())

        if "CER-20211003" in project["notes"]:
            project["name"] = "IBERUS"
            project["full_title"] = (
                "Red tecnológica de Ingeniería biomédica aplicada a patologías degenerativas "
                "del sistema neuromusculoesquelético en entornos clínicos y extrahospitalarios."
            )
            project["type"] = "Red de Excelencia CERVERA"
            project["funder"] = "CDTI / Ministerio de Ciencia e Innovación"
            project["category"] = "Ingeniería biomédica / Smart health data / Salud digital"
            project["notes"] = (
                "Fortalecimiento de capacidades tecnológicas para diagnóstico, rehabilitación, "
                "tratamiento y asistencia de enfermedades degenerativas neuromusculoesqueléticas. "
                "Incluye smart health data, wearables, visión artificial, ingeniería neuromórfica, "
                "algoritmos de IA e integración de datos heterogéneos para valoración funcional."
            )
            project["reference"] = "EXP 00139943 / CER-20211003"
            project["url"] = (
                "https://www.ibv.org/proyecto/iberus-red-tecnologica-de-ingenieria-biomedica-"
                "aplicada-a-patologias-degenerativas-del-sistema-neuromusculoesqueletico-en-"
                "entornos-clinicos-y-extrahospitalarios/"
            )

        if project["name"] in {"GUARDIANES", "MEDUSA", "IBERUS"}:
            project["funder"] = "Centro para el Desarrollo Tecnológico Industrial (CDTI)"

        if project["name"] == "my-AHA":
            project["funder"] = "European Commission (H2020)"

        projects.append(project)

    projects = projects + EXTRA_PROJECTS
    for project in projects:
        if project["name"] in {"GUARDIANES", "MEDUSA", "IBERUS"}:
            project["funder"] = "Centro para el Desarrollo Tecnológico Industrial (CDTI)"
        if project["name"] == "my-AHA":
            project["funder"] = "European Commission (H2020)"
    return projects


def project_dataframe(projects: list[dict[str, str]]) -> pd.DataFrame:
    df = pd.DataFrame(projects)
    if df.empty:
        return df

    df["start_date"] = pd.to_datetime(df["start"], dayfirst=True, errors="coerce")
    df["end_date"] = pd.to_datetime(df["end"], dayfirst=True, errors="coerce")
    df["year_num"] = pd.to_numeric(df["year"], errors="coerce")
    df["topics"] = df["category"].str.split("/").apply(
        lambda items: [item.strip() for item in items if item.strip()] if isinstance(items, list) else []
    )
    return df


def render_hero() -> None:
    image_html = ""
    if PHOTO_PATH.exists():
        import base64

        encoded = base64.b64encode(PHOTO_PATH.read_bytes()).decode("ascii")
        image_html = f'<img src="data:image/jpeg;base64,{encoded}" alt="{PROFILE["name"]}">'

    st.markdown(
        f"""
        <div class="hero">
          <div>{image_html}</div>
          <div>
            <h1 class="hero-title">{PROFILE["name"]}</h1>
            <p class="hero-role">{PROFILE["role"]}</p>
            <p class="hero-summary">{PROFILE["summary"]}</p>
            <div class="contact-row">
              <span class="contact-pill">{PROFILE["location"]}</span>
              <span class="contact-pill">{PROFILE["email"]}</span>
              <span class="contact-pill">{PROFILE["phone"]}</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(projects: list[dict[str, str]]) -> None:
    metrics = scholar_metrics()
    cols = st.columns(5)
    cols[0].metric("Citations", metrics["Citations"])
    cols[1].metric("h-index", metrics["h-index"])
    cols[2].metric("i10-index", metrics["i10-index"])
    cols[3].metric("Projects", len(projects))
    cols[4].metric("Years at IBV", metrics["Years at IBV"])


def render_profile(projects: list[dict[str, str]]) -> None:
    render_metrics(projects)
    st.markdown('<div class="section-title">Positioning</div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        st.write(
            "Hybrid profile spanning applied research, advanced data analytics and solution "
            "engineering. The professional narrative is centered on digital health, biomechanics, "
            "applied AI, experimental validation and technology transfer."
        )
        st.link_button("LinkedIn", PROFILE["linkedin"])
        st.link_button("Google Scholar", PROFILE["scholar"])
        st.link_button("ResearchGate", PROFILE["researchgate"])
    with right:
        cv_text = read_file(CV_TEXT_PATH)
        word_count = len(re.findall(r"\w+", cv_text))
        st.metric("CV text words", word_count)
        if DEVELOP_CV_PDF_PATH.exists():
            st.download_button(
                "Download developer CV PDF",
                data=DEVELOP_CV_PDF_PATH.read_bytes(),
                file_name=DEVELOP_CV_PDF_PATH.name,
                mime="application/pdf",
            )


def render_experience() -> None:
    st.markdown('<div class="section-title">Professional Timeline</div>', unsafe_allow_html=True)
    for item in EXPERIENCE:
        st.markdown(
            f"""
            <div class="timeline-item">
              <div class="timeline-date">{item["period"]}</div>
              <div class="timeline-title">{item["role"]}</div>
              <div class="muted">{item["company"]}</div>
              <ul>
                {"".join(f"<li>{highlight}</li>" for highlight in item["highlights"])}
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_education() -> None:
    st.markdown('<div class="section-title">Academic Background</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for index, item in enumerate(EDUCATION):
        with cols[index % 2]:
            st.markdown(
                f"""
                <div class="timeline-item">
                  <div class="timeline-date">{item["year"]}</div>
                  <div class="timeline-title">{item["degree"]}</div>
                  <div class="muted">{item["institution"]}</div>
                  <p>{item["note"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_skills() -> None:
    st.markdown('<div class="section-title">Capabilities Map</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for index, (group, skills) in enumerate(SKILLS.items()):
        with cols[index % 3]:
            st.markdown(
                f"""
                <div class="skill-box">
                  <div class="timeline-title">{group}</div>
                  {"".join(f'<span class="tag">{skill}</span>' for skill in skills)}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">Selected Applied Work</div>', unsafe_allow_html=True)
    work_cols = st.columns(2)
    for index, work in enumerate(SELECTED_WORKS):
        with work_cols[index % 2]:
            st.markdown(
                f"""
                <div class="project-card">
                  <div class="timeline-title">{work["title"]}</div>
                  <p>{work["summary"]}</p>
                  {"".join(f'<span class="tag">{tag}</span>' for tag in work["tags"])}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_research(projects: list[dict[str, str]]) -> None:
    df = project_dataframe(projects)
    st.markdown('<div class="section-title">Research Activity</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No project data found yet.")
        return

    funders = sorted(df["funder"].dropna().unique())
    selected_funders = st.multiselect("Funding entities", funders, default=funders)
    years = sorted(int(year) for year in df["year_num"].dropna().unique())
    selected_years = st.slider("Award year range", min(years), max(years), (min(years), max(years)))

    filtered = df[
        df["funder"].isin(selected_funders)
        & df["year_num"].between(selected_years[0], selected_years[1], inclusive="both")
    ].copy()

    summary_cols = st.columns(4)
    summary_cols[0].metric("Filtered projects", len(filtered))
    summary_cols[1].metric("Funding entities", filtered["funder"].nunique())
    summary_cols[2].metric("First year", int(filtered["year_num"].min()) if not filtered.empty else "-")
    summary_cols[3].metric("Latest year", int(filtered["year_num"].max()) if not filtered.empty else "-")

    chart_left, chart_right = st.columns([1.1, 0.9], gap="large")
    with chart_left:
        counts = filtered.groupby("year_num", as_index=False).size()
        fig = px.bar(
            counts,
            x="year_num",
            y="size",
            text="size",
            labels={"year_num": "Year", "size": "Projects"},
            color_discrete_sequence=["#147d87"],
        )
        fig.update_layout(
            height=330,
            margin=dict(l=12, r=12, t=16, b=12),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
    with chart_right:
        funder_counts = filtered["funder"].value_counts().reset_index()
        funder_counts.columns = ["funder", "projects"]
        fig = px.pie(
            funder_counts,
            names="funder",
            values="projects",
            hole=0.48,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(
            height=330,
            margin=dict(l=12, r=12, t=16, b=12),
            showlegend=True,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    topic_counter: Counter[str] = Counter()
    for topics in filtered["topics"]:
        topic_counter.update(topics)
    topic_df = pd.DataFrame(topic_counter.most_common(), columns=["topic", "projects"])

    if not topic_df.empty:
        fig = px.bar(
            topic_df,
            x="projects",
            y="topic",
            orientation="h",
            labels={"projects": "Projects", "topic": "Theme"},
            color="projects",
            color_continuous_scale=["#dcefed", "#147d87"],
        )
        fig.update_layout(
            height=360,
            margin=dict(l=12, r=12, t=16, b=12),
            coloraxis_showscale=False,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Project Explorer</div>', unsafe_allow_html=True)
    search = st.text_input("Search project, category or notes")
    if search:
        mask = filtered.apply(
            lambda row: search.lower() in " ".join(str(value).lower() for value in row.values),
            axis=1,
        )
        filtered = filtered[mask]

    for _, row in filtered.sort_values("start_date", ascending=False).iterrows():
        source_link = ""
        if row.get("url", ""):
            source_link = f'<p><a href="{row["url"]}" target="_blank">Project source</a></p>'
        reference = f' · {row["reference"]}' if row.get("reference", "") else ""
        st.markdown(
            f"""
            <div class="project-card">
              <div class="timeline-date">{row["duration"]}</div>
              <div class="timeline-title">{row["name"]}</div>
              <div class="muted">{row["funder"]} · {row["category"]}{reference}</div>
              <p>{row["full_title"] or row["notes"]}</p>
              {source_link}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_publications() -> None:
    st.markdown('<div class="section-title">Publications by Theme and Quartile</div>', unsafe_allow_html=True)
    st.caption("Data imported from Google Scholar and enriched with a local table of venues, publication types and quartiles.")
    pubs = enrich_publications(scholar_publications())
    pubs["clean_venue"] = pubs["clean_venue"].where(
        pubs["clean_venue"].astype(str).str.len() > 0,
        pubs.get("journal", pd.Series(dtype=str)).replace("", "Venue to review"),
    )
    if "theme" not in pubs:
        pubs["theme"] = ""
    blank_theme = pubs["theme"].astype(str).str.strip().eq("")
    pubs.loc[blank_theme, "theme"] = pubs.loc[blank_theme].apply(
        lambda row: infer_theme(row.get("title", ""), row.get("journal", "")),
        axis=1,
    )
    pubs["quartile"] = pubs["quartile"].replace("", "To review")
    pubs["count"] = 1

    metric_cols = st.columns(4)
    metric_cols[0].metric("Scholar records", len(pubs))
    metric_cols[1].metric("Total citations", int(pd.to_numeric(pubs.get("citations", 0), errors="coerce").fillna(0).sum()))
    metric_cols[2].metric("Indexed journals", int(pubs["publication_type"].eq("Journal").sum()))
    metric_cols[3].metric("Conferences / other", int(pubs["publication_type"].ne("Journal").sum()))

    st.markdown(
        """
        <p class="quality-note">
        The table separates indexed journals, conferences, theses and reports. Conferences and
        institutional publications do not receive journal JCR/SJR quartiles; they are shown as
        output types to avoid artificially inflating research activity.
        </p>
        """,
        unsafe_allow_html=True,
    )

    chart_left, chart_right = st.columns([1.15, 0.85], gap="large")

    theme_type = (
        pubs.groupby(["theme", "publication_type"], as_index=False)
        .size()
        .rename(columns={"size": "publications"})
    )
    theme_order = (
        theme_type.groupby("theme")["publications"]
        .sum()
        .sort_values(ascending=True)
        .index.tolist()
    )
    with chart_left:
        fig = px.bar(
            theme_type,
            x="publications",
            y="theme",
            color="publication_type",
            text="publications",
            orientation="h",
            category_orders={"theme": theme_order},
            labels={
                "publications": "Publications",
                "theme": "Theme",
                "publication_type": "Type",
            },
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_traces(textposition="inside", insidetextanchor="middle")
        fig.update_layout(
            title="Publications by Theme and Type",
            height=430,
            barmode="stack",
            margin=dict(l=12, r=12, t=44, b=12),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title_text="Type",
        )
        st.plotly_chart(fig, use_container_width=True)

    heatmap_data = (
        theme_type.pivot(index="publication_type", columns="theme", values="publications")
        .fillna(0)
        .astype(int)
    )
    heatmap_long = heatmap_data.reset_index().melt(
        id_vars="publication_type",
        var_name="theme",
        value_name="publications",
    )
    with chart_right:
        fig = px.density_heatmap(
            heatmap_long,
            x="theme",
            y="publication_type",
            z="publications",
            text_auto=True,
            color_continuous_scale=["#13262b", "#33c7ba", "#ffb35c"],
            labels={
                "theme": "Theme",
                "publication_type": "Type",
                "publications": "Publications",
            },
        )
        fig.update_layout(
            title="Type x Theme Matrix",
            height=430,
            margin=dict(l=12, r=12, t=44, b=12),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
        )
        fig.update_xaxes(tickangle=35)
        st.plotly_chart(fig, use_container_width=True)

    quartile_counts = (
        pubs.groupby(["quartile", "publication_type"], as_index=False)
        .size()
        .rename(columns={"size": "publications"})
        .sort_values("publications", ascending=False)
    )
    fig = px.bar(
        quartile_counts,
        x="quartile",
        y="publications",
        color="publication_type",
        text="publications",
        labels={
            "quartile": "Quartile / classification",
            "publications": "Publications",
            "publication_type": "Type",
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        title="Publications by Quartile or Output Classification",
        height=340,
        barmode="stack",
        margin=dict(l=12, r=12, t=44, b=12),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Type",
    )
    fig.update_xaxes(tickangle=20)
    st.plotly_chart(fig, use_container_width=True)

    columns = [
        column
        for column in [
            "title",
            "authors",
            "clean_venue",
            "publication_type",
            "year",
            "citations",
            "theme",
            "quartile",
            "ranking_source",
            "ranking_note",
        ]
        if column in pubs
    ]
    st.dataframe(
        pubs[columns].sort_values(["citations", "year"], ascending=[False, False]),
        use_container_width=True,
        hide_index=True,
    )


def render_awards() -> None:
    st.markdown('<div class="section-title">Recognitions and Awards</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for index, award in enumerate(AWARDS):
        with cols[index % 2]:
            st.markdown(
                f"""
                <div class="award-card">
                  <div class="timeline-date">{award["date"]}</div>
                  <div class="timeline-title">{award["title"]}</div>
                  <div class="muted">Issued by {award["issuer"]}</div>
                  <p><strong>Associated with:</strong> {award["associated_with"]}</p>
                  <p><strong>Awarded work:</strong> {award["work"]}</p>
                  <p>{award["description"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_teaching_proposal() -> None:
    st.markdown('<div class="section-title">Biomechanics Teaching Proposal</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="teaching-card">
          <div class="timeline-title">{TEACHING_PROPOSAL["headline"]}</div>
          <p>{TEACHING_PROPOSAL["summary"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    pillar_cols = st.columns(3)
    for index, pillar in enumerate(TEACHING_PROPOSAL["pillars"]):
        with pillar_cols[index]:
            st.markdown(
                f"""
                <div class="teaching-card">
                  <div class="timeline-title">{pillar["title"]}</div>
                  <ul>
                    {"".join(f"<li>{item}</li>" for item in pillar["items"])}
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">Example Continuous Assessment Activities</div>', unsafe_allow_html=True)
    activity_cols = st.columns(2)
    for index, activity in enumerate(TEACHING_PROPOSAL["activities"]):
        with activity_cols[index % 2]:
            st.markdown(
                f"""
                <div class="activity-card">
                  <div class="timeline-title">{activity["name"]}</div>
                  <p><strong>Goal:</strong> {activity["goal"]}</p>
                  <p><strong>Evidence:</strong> {activity["evidence"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">Interview Positioning</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="teaching-card">
          <ul>
            {"".join(f"<li>{point}</li>" for point in TEACHING_PROPOSAL["interview_points"])}
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.divider()
    st.caption(f"Last local refresh: {datetime.now().strftime('%Y-%m-%d %H:%M')} · Data source: Info/")


def main() -> None:
    inject_styles()
    projects = parse_projects(PROJECTS_PATH)
    render_hero()
    st.write("")

    tabs = st.tabs(["Overview", "Experience", "Education", "Skills", "Research", "Publications", "Teaching", "Awards"])
    with tabs[0]:
        render_profile(projects)
    with tabs[1]:
        render_experience()
    with tabs[2]:
        render_education()
    with tabs[3]:
        render_skills()
    with tabs[4]:
        render_research(projects)
    with tabs[5]:
        render_publications()
    with tabs[6]:
        render_teaching_proposal()
    with tabs[7]:
        render_awards()

    render_footer()


if __name__ == "__main__":
    main()
