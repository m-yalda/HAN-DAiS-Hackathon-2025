# Centraal databestand voor alle vragen en content
import tomllib
from dataclasses import dataclass
from enum import Enum, auto

class VraagNummer(Enum):
    ENERGIE = auto()
    TOLVIGNET = auto()
    WEGENWACHT = auto()
    LAADPAS = auto()

    def get_description(self) -> str:
        if self == VraagNummer.ENERGIE:
            return "Hoe sluit ik ANWB Energie af?"
        elif self == VraagNummer.TOLVIGNET:
            return "Heb ik een tolvignet nodig?"
        elif self == VraagNummer.WEGENWACHT:
            return "Welke wegenwachtpakketten zijn er?"
        elif self == VraagNummer.LAADPAS:
            return "Hoe activeer ik de ANWB Laadpas?"
        else:
            raise ValueError("Ongeldig vraagnummer.")

class ContentType(Enum):
    WEB = auto()
    CHAT = auto()
    GECOMBINEERD = auto()
    AANGEPAST = auto()

    def get_description(self) -> str:
        if self == ContentType.WEB:
            return "Web content (van ANWB website)"
        elif self == ContentType.CHAT:
            return "Chat content (van Iris chatbot)"
        elif self == ContentType.GECOMBINEERD:
            return "Gecombineerde content (combinatie van web + chat)"
        elif self == ContentType.AANGEPAST:
            return "Aangepaste content (experimenteel)"
        else:
            raise ValueError("Ongeldige content type.")

@dataclass
class Vraagdata:
  vraag:str
  antwoord:str
  web_content:str
  web_bronnen:list[str]
  chat_content:str
  aangepaste_content:str
  gecombineerde_content:str

  def get_content(self, content_type: ContentType) -> str:
    if content_type == ContentType.WEB:
      return self.web_content
    elif content_type == ContentType.CHAT:
      return self.chat_content
    elif content_type == ContentType.GECOMBINEERD:
      return self.gecombineerde_content
    elif content_type == ContentType.AANGEPAST:
      return self.aangepaste_content
    else:
      raise ValueError("Ongeldige content keuze. Kies 1, 2, 3 of 4.")

def get_vraagdata_object(vraag_nummer: VraagNummer) -> Vraagdata:

    with open(f'/content/DAiS_files/vraag{vraag_nummer.value}.py', 'rb') as f:
      vraag_data = tomllib.load(f)

      # Haal de vraag en content op
      vraag = vraag_data['vraag']
      antwoord = vraag_data['antwoord']
      web_content = vraag_data['web_content']
      web_bronnen = vraag_data['web_bronnen']
      chat_content = vraag_data['chat_content']
      aangepaste_content = vraag_data['aangepaste_content']
      gecombineerde_content = f"{web_content}\n\n{chat_content}"

      return Vraagdata(
        vraag=vraag,
        antwoord=antwoord,
        web_content=web_content,
        web_bronnen=web_bronnen,
        chat_content=chat_content,
        aangepaste_content=aangepaste_content,
        gecombineerde_content=gecombineerde_content
        )
      
@dataclass  
class Prompt:
  default_prompt:str
  custom_prompt:str

def get_prompt():
    with open('/content/DAiS_files/prompt.py', 'rb') as f:
        prompt_data = tomllib.load(f)
        
    return Prompt(
        default_prompt=prompt_data['prompt'],
        custom_prompt=prompt_data['custom_prompt']
    )
          
    

# Content type namen voor referentie TODO checken of deze nog nodig is
# content_type_namen = {
#     1: "Web content (van ANWB website)",
#     2: "Chat content (van Iris chatbot)",
#     3: "Gecombineerde content (combinatie van web + chat)",
#     4: "Aangepaste content (experimenteel)"
# }

# Dan in je main.py importeer je simpelweg uit data.py
# from data import vragen, web_content, chat_content, aangepaste_content, huidige_antwoorden, web_bronnen, content_type_namen