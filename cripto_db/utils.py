import os

def get_uri(username: str, password: str, cluster_domain: str) -> str:
    return f"mongodb+srv://{username}:{password}@{cluster_domain}/?retryWrites=true&w=majority"

def get_cripto_uri() -> str:
    username = os.getenv('MONGO_CRIPTO_USER')
    password = os.getenv('MONGO_CRIPTO_PASSWORD')
    cluster_domain = os.getenv("MONGO_CRIPTO_CLUSTER_DOMAIN")
    return get_uri(username, password, cluster_domain)
