import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API Groq
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY=st.secrets["GROQ_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Application Streamlit
st.title("DreamCatcher : application d'interprétation des rêves")

# Zone de saisie pour le rêve
dream_input = st.text_area("Entrez votre rêve ici :", height=150)

# Fonction pour générer l'interprétation via l'API Groq
def generate_interpretation(prompt):
    data = {
        "model": "mixtral-8x7b-32768",  # ou un autre modèle disponible sur Groq
        "messages": [
            {"role": "system", "content": "Vous êtes un assistant IA avec une compréhension approfondie de l'interprétation et du symbolisme des rêves. Votre tâche est de fournir aux utilisateurs des analyses perspicaces et significatives des symboles, des émotions et des récits présents dans leurs rêves. Proposer des interprétations potentielles tout en encourageant l'utilisateur à réfléchir à ses propres expériences et émotions."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 1
    }

    response = requests.post(GROQ_API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Erreur : {response.status_code} - {response.text}"

# Bouton pour déclencher l'interprétation
if st.button("Interpréter le rêve"):
    if dream_input:
        # Générer l'interprétation
        interpretation = generate_interpretation(dream_input)

        # Afficher l'interprétation
        st.subheader("Interprétation des rêves :")
        st.write(interpretation)
    else:
        st.warning("Veuillez saisir un rêve à interpréter.")

# Ajouter des informations sur l'application
st.sidebar.header("À propos de DreamCatcher")
st.sidebar.info(
    "DreamCatcher est une application d'interprétation des rêves alimentée par l'IA. "
    "Entrez votre rêve dans la zone de texte, et notre IA fournira des informations "
    "et des significations potentielles basées sur le symbolisme des rêves et les "
    "techniques d'interprétation."
)

# Avertissement
st.sidebar.header("Avertissement")
st.sidebar.warning(
    "Les interprétations fournies par cette application sont générées par un modèle d'IA "
    "et doivent être considérées comme des possibilités plutôt que des significations définitives. "
    "Les rêves sont très personnels et leur véritable signification ne peut souvent être "
    "déterminée par le rêveur qu'après réflexion."
)
