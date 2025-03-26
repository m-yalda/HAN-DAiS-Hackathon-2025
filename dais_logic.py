import os

from IPython.display import Markdown, display
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Importeren van de gestructureerde data
from data import (aangepaste_content, chat_content, content_type_namen,
                  gecombineerde_content, huidige_antwoorden, vragen,
                  web_content)
from prompt import prompt

# API-sleutel uit environment variable halen
api_key = os.environ.get("OPENAI_API_KEY", "")

def check_api_key():
    # Controleer of de API-sleutel is ingesteld
    if api_key == "":
        print("⚠️ Let op: Je hebt nog geen API-sleutel ingevoerd!")
    else:
        masked_key = "sk-" + "*" * 8 + api_key[-4:]
        print(f"✓ API-sleutel is ingesteld als environment variable: {masked_key}")


# Functie om markdown te tonen
def show_md(text):
    display(Markdown(text))

def setup_llm():
    # Controleer of de API-sleutel is ingesteld
    if not api_key:
        print("⚠️ Waarschuwing: Geen OpenAI API-sleutel gevonden in environment variables.")
        print("   Stel eerst je API-sleutel in met `os.environ['OPENAI_API_KEY'] = 'jouw-api-sleutel'`")
        return None

    return ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,
    )
llm = setup_llm()

# Functie om antwoorden te genereren op basis van vraag en content type
def stuur_vraag_naar_llm(vraag_nummer, content_type, custom_prompt=None):
    """
    Genereert een antwoord op een vraag met behulp van het LLM
    op basis van het gekozen content type.

    Parameters:
    - vraag_nummer: Nummer van de vraag (1-4)
      1: Hoe sluit ik ANWB Energie af?
      2: Heb ik een tolvignet nodig?
      3: Welke wegenwachtpakketten zijn er?
      4: Hoe activeer ik de ANWB Laadpas?

    - content_type: Nummer van het content type (1-4)
      1: Web content (van ANWB website)
      2: Chat content (van Iris chatbot)
      3: Gecombineerde content (combinatie van web + chat)
      4: Aangepaste content (experimenteel)

    - custom_prompt: Optionele aangepaste prompt instructies

    Returns:
    - Het gegenereerde antwoord naast het huidige antwoord in het systeem
    """
    # Controleer of het LLM correct is ingesteld
    if llm is None:
        return "⚠️ Error: Het LLM is niet geïnitialiseerd. Controleer je API-sleutel."

    # Gebruik de meegegeven prompt of de standaard prompt
    gebruikte_prompt = custom_prompt if custom_prompt else prompt

    # Zorg ervoor dat de keuzes numeriek zijn
    vraag_nummer = int(vraag_nummer)
    content_type = int(content_type)

    # Controleer of de vraag en content keuzes geldig zijn
    if vraag_nummer not in vragen:
        return "Ongeldige vraag keuze. Kies 1, 2, 3 of 4."

    # Map van content_keuze naar de juiste content dictionary
    content_maps = {
        1: web_content,
        2: chat_content,
        3: gecombineerde_content,
        4: aangepaste_content
    }

    if content_type not in content_maps:
        return "Ongeldige content keuze. Kies 1, 2, 3 of 4."

    # Haal de vraag en content op
    vraag = vragen[vraag_nummer]
    content = content_maps[content_type][vraag_nummer]
    huidig_antwoord = huidige_antwoorden[vraag_nummer]

    # Log wat er gebeurt
    print(f"Beantwoorden van vraag {vraag_nummer} met {content_type_namen[content_type]}")
    print('-----------------------------------')

    # Stel de berichten samen
    messages = [
        SystemMessage(content=gebruikte_prompt),
        HumanMessage(content=vraag),
        # HumanMessage(content=f"VRAAG: {vraag}"),
        AIMessage(content=content)
        # AIMessage(content=f"BESCHIKBARE CONTENT:\n{content}")
    ]
    # Stuur naar LLM en haal resultaat op
    response = llm.invoke(messages)

    # Toon resultaat in markdown formaat
    result_md = f"""
### Vraag:
{vraag}

### Gegenereerd antwoord met {content_type_namen[content_type]}:
{response.content}

### Huidig antwoord in het systeem:
{huidig_antwoord}
    """
    show_md(result_md)

    return response.content
