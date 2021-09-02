import re
from .utils import initialiser_instance_elastic, ConsultationIndexProfessionException

def rechercher_professions_par_autocompletion(hosts,nom_index,libelle,genre,ratio_max_min_score=0.4):
    es = initialiser_instance_elastic(hosts)
    if genre is None:
        res = es.search(index=nom_index,size=1000,body={
            "query":{
                "bool":{
                    "must":[{
                        "dis_max": {
                            "queries": [
                                { "match": { "libm": {"query": libelle} }},
                                { "match": { "libf": {"query":libelle } }}
                            ],
                            "tie_breaker": 0.0
                            }
                    }],
                    "should":[{
                        "dis_max": {
                            "queries": [
                                { "match": { "libm_first": {"query":re.split(r'\W+',libelle)[0], "boost":10}}},
                                { "match": { "libf_first": {"query":re.split(r'\W+',libelle)[0] , "boost":10}}}
                            ],
                            "tie_breaker": 0.0
                            }
                    }]
                }
            },
            "highlight":{
                    "fields":{
                        "libm":{"pre_tags" : ["<b>"], "post_tags" : ["</b>"]},
                        "libf":{"pre_tags" : ["<b>"], "post_tags" : ["</b>"]}
                }
            }
        },request_timeout=30)
    elif genre in ["m","f"]:
        res = es.search(index=nom_index,size=1000,body={
            "query":{
                "bool":{
                    "must":[{
                        "match": { "lib"+genre: {"query": libelle} }
                    }],
                    "should":[{
                        "match": { "lib"+genre+"_first": {"query":re.split(r'\W+',libelle)[0], "boost":10}}
                    }]
                }
            },
            "highlight":{
                    "fields":{
                        "lib"+genre:{"pre_tags" : ["<b>"], "post_tags" : ["</b>"]}
                    }
            }
        },request_timeout=30)
    max_score =  float(res['hits']['max_score'])
    echos = res['hits']['hits']
    nb_echos=len(echos)
    k=0
    while k<nb_echos and float(echos[k]['_score'])/max_score>ratio_max_min_score:
        k+=1
    return echos[:min(k,nb_echos)]


def rechercher_profession_par_id(hosts,nom_index,id):
    try:
        es = initialiser_instance_elastic(hosts)
        res = es.search(index=nom_index,body={
                "query":{
                    "term":{
                        "id":{
                            "value":str(id)
                        }
                    }
            }},request_timeout=30)
    except:
        raise ConsultationIndexProfessionException('Impossible d\'interroger ElasticSearch')
    try:
        obs = res['hits']['hits'][0]
    except:
        raise ConsultationIndexProfessionException('Le libellé de profession avec l\'identifiant {} est introuvable.'.format(id))
    return res

def rechercher_informations_codepcs(hosts,nom_index,codepcs):
    code = codepcs
    if code in ['NC','NSP','ATT']:
        code_complet = code
        description = None
        professions_typiques = None
        profesions_exclues = None
    else:
        code_complet = code + "0"*(4-len(code))
        try:
            es = initialiser_instance_elastic(hosts)
            res = es.search(index=nom_index,body={
                "query":{
                    "term":{
                        "code_key":{
                            "value":code
                        }
                    }
            }},request_timeout=30)
        except:
            raise ConsultationIndexProfessionException('Impossible d\'interroger ElasticSearch')

        try:
            obs = res['hits']['hits'][0]
        except:
            raise ConsultationIndexProfessionException('Code PCS "{}" non trouvé'.format(codepcs),200)
        
        try:
            libelle = obs['_source']['libelle']
        except:
            libelle = None
        try:
            description = obs['_source']['description']
        except:
            description = None
        try:
            professions_typiques = obs['_source']['professions_typiques']
            professions_typiques = professions_typiques.split('|')
        except:
            professions_typiques = []
        try:
            profesions_exclues = obs['_source']['profesions_exclues']
            profesions_exclues = profesions_exclues.split('|')
        except:
            profesions_exclues = []
    return {'intitule': libelle,'code':code_complet,'description':description,'professions_typiques':professions_typiques,'profesions_exclues':profesions_exclues} 