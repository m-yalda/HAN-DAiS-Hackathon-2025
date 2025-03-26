# Centraal databestand voor alle vragen en content
from vraag1 import (aangepaste_content1, antwoord1, chat_content1, vraag1,
                    web_bronnen1, web_content1)
from vraag2 import (aangepaste_content2, antwoord2, chat_content2, vraag2,
                    web_bronnen2, web_content2)
from vraag3 import (aangepaste_content3, antwoord3, chat_content3, vraag3,
                    web_bronnen3, web_content3)
from vraag4 import (aangepaste_content4, antwoord4, chat_content4, vraag4,
                    web_bronnen4, web_content4)

vragen = {
    1: vraag1,
    2: vraag2,
    3: vraag3,
    4: vraag4
}

huidige_antwoorden = {
    1: antwoord1,
    2: antwoord2,
    3: antwoord3,
    4: antwoord4
}

web_content = {
    1: web_content1,
    2: web_content2,
    3: web_content3,
    4: web_content4
}

chat_content = {
    1: chat_content1,
    2: chat_content2,
    3: chat_content3,
    4: chat_content4
}

gecombineerde_content = {
    1: "\n\n".join([web_content1, chat_content1]),
    2: "\n\n".join([web_content2, chat_content2]),
    3: "\n\n".join([web_content3, chat_content3]),
    4: "\n\n".join([web_content4, chat_content4])
}

# Aangepaste content - dit kan initieel leeg zijn
aangepaste_content = {
    1: aangepaste_content1,
    2: aangepaste_content2,
    3: aangepaste_content3,
    4: aangepaste_content4
}

# Bronnen voor extra informatie
web_bronnen = {
    1: web_bronnen1,
    2: web_bronnen2,
    3: web_bronnen3,
    4: web_bronnen4
}

# Content type namen voor referentie
content_type_namen = {
    1: "Web content (van ANWB website)",
    2: "Chat content (van Iris chatbot)",
    3: "Gecombineerde content (combinatie van web + chat)",
    4: "Aangepaste content (experimenteel)"
}

# Dan in je main.py importeer je simpelweg uit data.py
# from data import vragen, web_content, chat_content, aangepaste_content, huidige_antwoorden, web_bronnen, content_type_namen