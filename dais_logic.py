from google.colab import userdata
from google.colab.userdata import SecretNotFoundError
from IPython.display import Markdown, display
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Importeren van de gestructureerde data
from data import ContentType, VraagNummer, get_prompt, get_vraagdata_object


# Functie om markdown te tonen
def show_md(text):
    display(Markdown(text))

def setup_llm():
    # API-sleutel uit environment variable halen
    try:
        api_key = userdata.get('OPENAI_API_KEY')
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key,
        )
    except SecretNotFoundError:
        print("⚠️ Waarschuwing: OpenAI API-sleutel is niet ingesteld in Colab secrets.")
        return None
    except Exception as e:
        print(f"⚠️ Fout bij het instellen van het LLM: {str(e)}")
        print("💡 Tip: Stel je API-sleutel in via Colab's Secrets management:")
        print("   1. Klik in het linkermenu op het slotje 🔒")
        print("   2. Voeg een nieuwe secret toe met naam 'OPENAI_API_KEY' en jouw sleutel als waarde")
        return None

llm = setup_llm()

# Functie om antwoorden te genereren op basis van vraag en content type
def stuur_vraag_naar_llm(vraag_nummer_int:int, content_type_int:int = 3, custom_prompt:bool = False):
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
    gebruikte_prompt = get_prompt().custom_prompt if custom_prompt else get_prompt().default_prompt

    try:
        content_type = ContentType(content_type_int)
    except ValueError:
        return "Ongeldige content keuze. Kies 1, 2, 3 of 4."
    # Controleer of de vraag en content keuzes geldig zijn
    try:
        vraag_nummer = VraagNummer(vraag_nummer_int)
    except ValueError:
        return "Ongeldige vraag keuze. Kies 1, 2, 3 of 4."

    vraagdata = get_vraagdata_object(vraag_nummer)
    # Map van content_keuze naar de juiste content dictionary


    # Haal de vraag en content op
    vraag = vraagdata.vraag
    content = vraagdata.get_content(content_type)
    huidig_antwoord = vraagdata.antwoord

    # Log wat er gebeurt
    print(f"Beantwoorden van vraag {vraag_nummer.value} met {content_type.get_description()}")
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

### Gegenereerd antwoord met {content_type.get_description()}:
{response.content}

### Huidig antwoord in het systeem:
{huidig_antwoord}
    """
    show_md(result_md)

    return response.content
