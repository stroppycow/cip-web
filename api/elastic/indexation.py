
from .params import parametrage_index_nomenclature, parametrage_index_profession
import re

def indexer_nomenclature_pcs2020(data,es,nom_index):
    if es.indices.exists(nom_index):
        es.indices.delete(nom_index)
    es.indices.create(index = nom_index, body = parametrage_index_nomenclature, request_timeout=300)
    bulk_data = []
    for i,n in enumerate(data):
        n['code'] = n['code'][:int(n['niveau'])]
        n['code_key'] = n['code']
        n['description'] = None if isinstance(n['description'],float) else n['description']
        n['professions_typiques'] = None if isinstance(n['professions_typiques'],float) else n['professions_typiques']
        n['professions_exclues'] = None if isinstance(n['professions_exclues'],float) else n['professions_exclues']
        op_dict = {
            "index": {
                "_index": nom_index,
                "_id": i,
            }
        }
        bulk_data.append(op_dict)
        bulk_data.append(n)
    es.bulk(index = nom_index, body = bulk_data,request_timeout=300)

def indexer_index_profession(data,es,nom_index):
    if es.indices.exists(nom_index):
        es.indices.delete(nom_index)
    es.indices.create(index = nom_index, body = parametrage_index_profession, request_timeout=300)

    bulk_data = []
    for i,n in enumerate(data):
        op_dict = {
            "index": {
                "_index": nom_index,
                "_id": n['id'],
            }
        }
        n['libm_full'] = 'STARTDEBUT '+ str(n['libm']) +' STOPFIN'
        n['libf_full'] = 'STARTDEBUT '+ str(n['libf']) +' STOPFIN'
        n['libm_first'] = re.split(r'\W+', str(n['libm']))[0]
        n['libf_first'] = re.split(r'\W+', str(n['libf']))[0]
        bulk_data.append(op_dict)
        bulk_data.append(n)
    es.bulk(index = nom_index, body = bulk_data,request_timeout=300)