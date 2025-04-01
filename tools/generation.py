#installed ollama with conda install conda-forge::ollama-python 
#installed langchain_community with pip install langchain-community
from langchain_community.llms import Ollama
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

llm = Ollama(model='deepseek-r1:1.5b')
chat_template = ChatPromptTemplate([
    ("system", """

            **Tu es GenData, un LLM de génération de données. Tu crée des jeux de données synthétiques en francais destinés à benchmarquer les validateurs comme Guardrails et LLMguard.**
            
            **Règles d'or :**
            - **Ne jamais inventer de réponses !**
            
            **Actions :**
            - **Génération :** Analyse la demande de l'utilisateur et génére des bases de données avec ces colonnes : Texte, Text masqué, Privacy masque utilisé, span_label et bio_label 
         
            
            **Format des réponses :**
            - Utilise le Markdown pour une présentation claire et agréable.
            
            **Tonalité :**
            - Sois direct et pragmatique ! Ne donne jamais des exemples incomplets.
             
        """),
    ("human", "{user_input}"),
])

messages = chat_template.format_messages(name="Data Scientist", user_input=input(">> "))
print(messages)
print(llm.invoke(messages))
'''
system_prompt = """
Tu es GenData, un LLM de génération de données. Tu crée des jeux de données synthétiques en francais destinés à benchmarquer les validateurs comme Guardrails et LLMguard. Ces données doivent facilement s'interfacer avec les validators par rapport au mapping des entités surtout. Les datasets doivent être fournis au format .database, facilement téléchargeable et utilisable
Soit direct est donne au data scientist juste la database avec une colonne Texte, Text masqué, Privacy masque utilisé, span_label et bio_label.
Voici un exemple d'une ligne qui pourrait être générée pour le validator PII masking :
Cher [PREFIX_1] [LASTNAME_1], nous organisons un programme d'alphabétisation à [CITY_1] en collaboration avec [COMPANYNAME_1]. Contactez [EMAIL_1] pour plus de détails.
Cher Ms. Keebler, nous organisons un programme d'alphabétisation à West Shemar en collaboration avec Morissette - Russel. Contactez Hulda44@yahoo.com pour plus de détails.
{'[PREFIX_1]': 'Ms.', '[LASTNAME_1]': 'Keebler', '[CITY_1]': 'West Shemar', '[COMPANYNAME_1]': 'Morissette - Russel', '[EMAIL_1]': 'Hulda44@yahoo.com'}
[[0, 5, 'O'], [5, 8, 'PREFIX_1'], [8, 9, 'O'], [9, 16, 'LASTNAME_1'], [16, 67, 'O'], [67, 78, 'CITY_1'], [78, 101, 'O'], [101, 120, 'COMPANYNAME_1'], [120, 132, 'O'], [132, 149, 'EMAIL_1'], [149, 171, 'O']]
[ "O", "B-PREFIX", "I-PREFIX", "B-LASTNAME", "I-LASTNAME", "I-LASTNAME", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-CITY", "I-CITY", "I-CITY", "O", "O", "O", "O", "B-COMPANYNAME", "I-COMPANYNAME", "I-COMPANYNAME", "I-COMPANYNAME", "I-COMPANYNAME", "I-COMPANYNAME", "O", "O", "O", "B-EMAIL", "I-EMAIL", "I-EMAIL", "I-EMAIL", "I-EMAIL", "I-EMAIL", "I-EMAIL", "O", "O", "O", "O", "O" ]
"""
'''
'''
chat_prompt = load_prompt()
graph = StateGraph(MessagesState)
graph.add_node("node_call_llm", node_call_llm)
llm_response = llm.invoke(chat_prompt)
print(llm_response)'''