# Este bloque es la conexión que ocupamos para conectarnos con nuestra base de datos, en esta oportunidad MONGODB

from pymongo import MongoClient

def get_database():
    
    # El nombre requerido es el que uno especifique segun sea su criterio en su base de datos

    acme_smoked_fish = "mongodb://localhost:27017"
    client = MongoClient(acme_smoked_fish)
    
    # Crea la base de datos llamada 'acme_salmon_fish' en mongoDB una vez ejecutado el bloque seteo_programa.py
    # Junto con sus colecciones llamadas usuarios y stock

    return client["acme_smoked_fish"]
