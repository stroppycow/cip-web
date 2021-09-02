
from elasticsearch import Elasticsearch

def initialiser_instance_elastic(host):
    return Elasticsearch(host)

class ConsultationIndexProfessionException(Exception):
    def __init__(message: str):
        super().__init__(message)