## Logs : 
Donne moi 30 exemples
Je comprends les règles d'or et les actions pour créer une base de données synthétique en français. Voici 30 exemples pour vous :

| **masked_text** | **unmasked_text** | **privacy_mask** | **labels** |
| --- | --- | --- | --- |
| L'entreprise ORGANIZATION a envoyé un email à EMAIL pour obtenir plus d'informations sur le projet. | L'entreprise X a envoyé un email à john.doe@example.com pour obtenir plus d'informations sur le projet. | `{"ORGANIZATION": "X", "EMAIL": "john.doe@example.com"}` | `[["13,14","ORGANIZATION"],["35,56","EMAIL"]]` |
| Le site web WEBSITE a été visité 10 fois ce mois-ci. | Le site web amazon.fr a été visité 10 fois ce mois-ci. | `{"WEBSITE": "amazon.fr"}` | `[["25,30","WEBSITE"]]` |
| L'utilisateur IDENTITY a effectué un achat de valeur 100€. | L'utilisateur John Doe a effectué un achat de valeur 100€. | `{"IDENTITY": "John Doe"}` | `[["18,22","IDENTITY"]]` |
| La ville LOCALISATION est située dans le département 91. | La ville Paris est située dans le département 75. | `{"LOCALISATION": {"ville": "Paris", "département": "75"}}` | `[["5,10","LOCALISATION"]]` |
| L'entreprise ORGANIZATION a obtenu un prêt bancaire de valeur 50000€. | L'entreprise X a obtenu un prêt bancaire de valeur 50000€. | `{"ORGANIZATION": "X", "montant": "50000"}` | `[["15,20","ORGANIZATION"],["25,30","montant"]]` |
| Le site web WEBSITE a été hacké il y a quelques jours. | Le site web amazon.fr a été hacké il y a quelques jours. | `{"WEBSITE": "amazon.fr", "détails": "hack"}` | `[["20,25","WEBSITE"],["30,35","détails"]]` |
| L'utilisateur IDENTITY a effectué un paiement de valeur 50€. | L'utilisateur John Doe a effectué un paiement de valeur 50€. | `{"IDENTITY": "John Doe", "montant": "50"}` | `[["18,22","IDENTITY"],["25,30","montant"]]` |
| La ville LOCALISATION est située dans le pays FRANCE. | La ville Paris est située dans le pays France. | `{"LOCALISATION": {"ville": "Paris", "pays": "France"}}` | `[["5,10","LOCALISATION"],["15,20","pays"]]` |
| L'entreprise ORGANIZATION a créé un nouveau produit appelé PRODUIT. | L'entreprise X a créé un nouveau produit appelé Smartphone. | `{"ORGANIZATION": "X", "PRODUIT": "Smartphone"}` | `[["15,20","ORGANIZATION"],["25,30","PRODUIT"]]` |
| Le site web WEBSITE a été mis en ligne il y a quelques mois. | Le site web amazon.fr a été mis en ligne il y a quelques mois. | `{"WEBSITE": "amazon.fr", "date": "dernier mois"}` | `[["20,25","WEBSITE"],["30,35","date"]]` |
| L'utilisateur IDENTITY a effectué un dépôt de document de valeur 200€. | L'utilisateur John Doe a effectué un dépôt de document de valeur 200€. | `{"IDENTITY": "John Doe", "montant": "200"}` | `[["18,22","IDENTITY"],["25,30","montant"]]` |
| La ville LOCALISATION est située dans la région ÎLE-DE-FRANCE. | La ville Paris est située dans la région Île-de-France. | `{"LOCALISATION": {"ville": "Paris", "région": "Île-de-France"}}` | `[["5,10","LOCALISATION"],["15,20","région"]]` |
| L'entreprise ORGANIZATION a créé un nouveau service appelé SERVICE. | L'entreprise X a créé un nouveau service appelé Assistance Technique. | `{"ORGANIZATION": "X", "SERVICE": "Assistance Technique"}` | `[["15,20","ORGANIZATION"],["25,30","SERVICE"]]` |
| Le site web WEBSITE a été abandonné il y a quelques mois. | Le site web amazon.fr a été abandonné il y a quelques mois. | `{"WEBSITE": "amazon.fr", "détails": "abandon"}` | `[["20,25","WEBSITE"],["30,35","détails"]]` |
| L'utilisateur IDENTITY a effectué un paiement de valeur 75€. | L'utilisateur John Doe a effectué un paiement de valeur 75€. | `{"IDENTITY": "John Doe", "montant": "75"}` | `[["18,22","IDENTITY"],["25,30","montant"]]` |
| La ville LOCALISATION est située dans le département 92. | La ville Paris est située dans le département 75. | `{"LOCALISATION": {"ville": "Paris", "département": "75"}}` | `[["5,10","LOCALISATION"]]` |
| L'entreprise ORGANIZATION a obtenu un financement de valeur 30000€. | L'entreprise X a obtenu un financement de valeur 30000€. | `{"ORGANIZATION": "X", "montant": "30000"}` | `[["15,20","ORGANIZATION"],["25,30","montant"]]` |
| Le site web WEBSITE a été piraté il y a quelques jours. | Le site web amazon.fr a été piraté il y a quelques jours. | `{"WEBSITE": "amazon.fr", "détails": "pirate"}` | `[["20,25","WEBSITE"],["30,35","détails"]]` |
| L'utilisateur IDENTITY a effectué un dépôt de document de valeur 150€. | L'utilisateur John Doe a effectué un dépôt de document de valeur 150€. | `{"IDENTITY": "John Doe", "montant": "150"}` | `[["18,22","IDENTITY"],["25,30","montant"]]` |
| La ville LOCALISATION est située dans la ville de Paris. | La ville Paris est située dans la ville de Paris. | `{"LOCALISATION": {"ville": "Paris"}}` | `[["5,10","LOCALISATION"]]` |
| L'entreprise ORGANIZATION a créé un nouveau produit appelé PRODUIT. | L'entreprise X a créé un nouveau produit appelé Smartphone. | `{"ORGANIZATION": "X", "PRODUIT": "Smartphone"}` | `[["15,20","ORGANIZATION"],["25,30","PRODUIT"]]` |
| Le site web WEBSITE a été mis en ligne il y a quelques mois. | Le site web amazon.fr a été mis en ligne il y a quelques mois. | `{"WEBSITE": "amazon.fr", "date": "dernier mois"}` | `[["20,25","WEBSITE"],["30,35","date"]]` |
| L'utilisateur IDENTITY a effectué un paiement de valeur 250€. | L'utilisateur John Doe a effectué un paiement de valeur 250€. | `{"IDENTITY": "John Doe", "montant": "250"}` | `[["18,22","IDENTITY"],["25,30","montant"]]` |
| La ville LOCALISATION est située dans la région CORSE. | La ville Paris est située dans la région Corse. | `{"LOCALISATION": {"ville": "Paris", "région": "Corse"}}` | `[["5,10","LOCALISATION"],["15,20","région"]]`

## Test avant push:
$ python tools/generation.py 
/home/jovyan/BenchAISecTools/tools/generation.py:9: LangChainDeprecationWarning: The class `Ollama` was deprecated in LangChain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the :class:`~langchain-ollama package and should be used instead. To use it run `pip install -U :class:`~langchain-ollama` and import as `from :class:`~langchain_ollama import OllamaLLM``.
  llm = Ollama(model='llama3.1')
>> donne moi une base de données avec 10 exemples de textes contenant différentes entités sensibles (organisation, email, numéro de téléphone, adresse, etc.)
Voici une base de données avec 10 exemples de textes contenant différentes entités sensibles :
```
| masked_text | unmasked_text | privacy_mask | labels |
|-------------|---------------|--------------|-------|
| L'entreprise ORGANIZATION a envoyé un email à EMAIL pour obtenir plus d'informations sur le projet. | L'entreprise Banque populaire a envoyé un email à jack@mail.fr pour obtenir plus d'informations sur le projet. | {'ORGANIZATION': 'Banque populaire', 'EMAIL': 'jack@mail.fr'} | [[13,29,'ORGANIZATION'],[38,62,'EMAIL']] |
| Le propriétaire du PERSON a reçu un email de la part de l'entreprise ORGANIZATION pour rappeler une rendez-vous. | Le propriétaire de John a reçu un email de la part de l'entreprise Apple pour rappeler une rendez-vous. | {'PERSON': 'John', 'ORGANIZATION': 'Apple'} | [[15,30,'PERSON'],[38,51,'ORGANIZATION']] |
| L'adresse IP IP_ADDRESS est utilisée par le réseau ORGANIZATION pour accéder à Internet. | L'adresse IP 192.168.1.100 est utilisée par le réseau Google pour accéder à Internet. | {'IP_ADDRESS': '192.168.1.100', 'ORGANIZATION': 'Google'} | [[20,36,'IP_ADDRESS'],[41,55,'ORGANIZATION']] |
| Le numéro de téléphone PHONE_NUMBER de la personne a été utilisé pour contacter le service client de l'entreprise ORGANization. | Le numéro de téléphone 01 23 45 67 89 de John a été utilisé pour contacter le service client de l'entreprise Apple. | {'PHONE_NUMBER': '01 23 45 67 89', 'ORGANIZATION': 'Apple'} | [[25,43,'PHONE_NUMBER'],[49,62,'ORGANIZATION']] |
| La carte bancaire CREDIT_CARD a été utilisée pour effectuer une transaction en ligne avec l'entreprise ORGANIZATION. | La carte bancaire Visa 1234 5678 9012 3456 a été utilisée pour effectuer une transaction en ligne avec l'entreprise Amazon. | {'CREDIT_CARD': 'Visa 1234 5678 9012 3456', 'ORGANIZATION': 'Amazon'} | [[30,49,'CREDIT_CARD'],[54,67,'ORGANIZATION']] |
| L'iban IBAN_CODE a été utilisé pour effectuer un virement bancaire avec la banque ORGANIZATION. | L'iban FR76 3000 6000 0001 2345 6789 a été utilisé pour effectuer un virement bancaire avec la banque BNP Paribas. | {'IBAN_CODE': 'FR76 3000 6000 0001 2345 6789', 'ORGANIZATION': 'BNP Paribas'} | [[35,53,'IBAN_CODE'],[60,73,'ORGANIZATION']] |
| Le propriétaire du PERSON a envoyé un courrier à l'adresse ADRESSE de la personne. | Le propriétaire de John a envoyé un courrier à l'adresse 14 rue de la République de la personne. | {'PERSON': 'John', 'ADRESSE': '14 rue de la République'} | [[15,30,'PERSON'],[43,58,'ADRESSE']] |
| L'entreprise ORGANIZATION a organisé un événement à l'hôtel HÔTEL pour les clients. | L'entreprise Apple a organisé un événement à l'hôtel Sofitel pour les clients. | {'ORGANIZATION': 'Apple', 'HÔTEL': 'Sofitel'} | [[13,29,'ORGANIZATION'],[39,52,'HÔTEL']] |
| Le numéro de téléphone PHONE_NUMBER du PERSON a été utilisé pour contacter le service client de l'entreprise ORGANIZATION. | Le numéro de téléphone 01 23 45 67 89 du John a été utilisé pour contacter le service client de l'entreprise Apple. | {'PHONE_NUMBER': '01 23 45 67 89', 'ORGANIZATION': 'Apple'} | [[25,43,'PHONE_NUMBER'],[49,62,'ORGANIZATION']] |
| La carte bancaire CREDIT_CARD a été utilisée pour effectuer une transaction en ligne avec l'entreprise ORGANIZATION. | La carte bancaire Visa 1234 5678 9012 3456 a été utilisée pour effectuer une transaction en ligne avec l'entreprise Amazon. | {'CREDIT_CARD': 'Visa 1234 5678 9012 3456', 'ORGANIZATION': 'Amazon'} | [[30,49,'CREDIT_CARD'],[54,67,'ORGANIZATION']] |

Voici la liste des entités sensibles masquées :

* ORGANIZATION : nom d'une entreprise
* PERSON : nom d'une personne
* EMAIL_ADDRESS : adresse email
* PHONE_NUMBER : numéro de téléphone
* IP_ADDRESS : adresse IP
* IBAN_CODE : code IBAN
* CREDIT_CARD : numéro de carte bancaire
* ADRESSE : adresse
```
J'espère que cela répond à vos besoins !
