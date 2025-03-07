import datasets

def load_dataset(name: str, split: str, subset: str = ""):
    """Load a dataset from hugging face"""
    if subset != "":
        dataset = datasets.load_dataset(name, subset, split=split)
    else:
        dataset = datasets.load_dataset(name, split=split)
    print(f"Split '{split}' of size {len(dataset)} from '{name}' loaded !")
    return dataset


def get_ai4privacy_to_presidio_mapping(presidio_entities: list[str] = []):
    mapping = {
        "EMAIL": "EMAIL_ADDRESS",
        "PHONEIMEI": "PHONE_NUMBER",
        "FIRSTNAME": "PERSON",
        "MIDDLENAME": "PERSON",
        "LASTNAME": "PERSON",
        "USERNAME": "PERSON",
        "IBAN": "IBAN_CODE",
        "IPV6": "IP_ADDRESS",
        "IP": "IP_ADDRESS",
        "IPV4": "IP_ADDRESS",
        "CREDITCARDNUMBER": "CREDIT_CARD",
        "ETHEREUMADDRESS": "CRYPTO",
        "BITCOINADDRESS": "CRYPTO",
        "LITECOINADDRESS": "CRYPTO"
    }

    if len(presidio_entities) == 0:
        return mapping
    
    filtered_mapping = {key: value for key, value in mapping.items() if value in presidio_entities}
    return filtered_mapping