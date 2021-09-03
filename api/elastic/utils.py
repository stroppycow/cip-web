
from elasticsearch import Elasticsearch

def initialiser_instance_elastic(host):
    return Elasticsearch(host)

class ConsultationIndexProfessionInternalException(Exception):
    def __init__(self,message: str):
        super().__init__(message)


class ConsultationIndexProfessionBadRequestException(Exception):
    def __init__(self,message: str):
        super().__init__(message)