import re
from .utils import initialiser_instance_elastic, ConsultationIndexProfessionInternalException, ConsultationIndexProfessionBadRequestException


def rechercher_professions_par_autocompletion(hosts,nom_index,libelle,genre,ratio_max_min_score=0.4):
    try:
        es = initialiser_instance_elastic(hosts)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible de se connecter à ElasticSearch')
        
    if genre is None:
        body = {
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
        }
    elif genre in ['masculin','feminin']:
        genre_short = str(genre[0])
        body={
            "query":{
                "bool":{
                    "must":[{
                        "match": { "lib"+genre_short: {"query": libelle} }
                    }],
                    "should":[{
                        "match": { "lib"+genre_short+"_first": {"query":re.split(r'\W+',libelle)[0], "boost":10}}
                    }]
                }
            },
            "highlight":{
                    "fields":{
                        "lib"+genre_short:{"pre_tags" : ["<b>"], "post_tags" : ["</b>"]}
                    }
            }
        }
    else:
        raise ConsultationIndexProfessionBadRequestException('Genre inconnu (i.e différent de \'masculin\', \'feminin\' ou null')
    
    try:
        res = es.search(index=nom_index,size=1000,body=body,request_timeout=100)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible d\'interroger ElasticSearch')
    
    if len(res['hits']['hits'])==0:
        return []
    max_score =  float(res['hits']['max_score'])
    echos = res['hits']['hits']
    nb_echos=len(echos)
    k=0
    output = []
    while k<nb_echos and float(echos[k]['_score'])/max_score>ratio_max_min_score:
        try:
            libelle_masculinise_formate = echos[k]['highlight']['libm'][0]
        except:
            libelle_masculinise_formate = None
        try:
            libelle_feminise_formate = echos[k]['highlight']['libf'][0]
        except:
            libelle_feminise_formate = None
        output.append({
            'id':int(echos[k]['_id']),
            'libelle_masculinise':echos[k]['_source']['libm'],
            'libelle_masculinise_formate':libelle_masculinise_formate,
            'libelle_feminise':echos[k]['_source']['libf'],
            'libelle_feminise_formate':libelle_feminise_formate,
            'priv_cad':echos[k]['_source']['priv_cad'],
            'priv_tec':echos[k]['_source']['priv_tec'],
            'priv_am':echos[k]['_source']['priv_am'],
            'priv_emp':echos[k]['_source']['priv_emp'],
            'priv_onq':echos[k]['_source']['priv_onq'],
            'priv_oq':echos[k]['_source']['priv_oq'],
            'priv_nr':echos[k]['_source']['priv_nr'],
            'pub_catA':echos[k]['_source']['pub_catA'],
            'pub_catB':echos[k]['_source']['pub_catB'],
            'pub_catC':echos[k]['_source']['pub_catC'],
            'pub_nr':echos[k]['_source']['pub_nr'],
            'inde_0_9':echos[k]['_source']['inde_0_9'],
            'inde_10_49':echos[k]['_source']['inde_10_49'],
            'inde_sup49':echos[k]['_source']['inde_sup49'],
            'inde_nr':echos[k]['_source']['inde_nr'],
            'aid_fam':echos[k]['_source']['aid_fam'],
            'ssvaran':echos[k]['_source']['ssvaran'],
            'score':echos[k]['_score']
        })
        k+=1
    return output


def rechercher_profession_par_id(hosts,nom_index,id):
    try:
        es = initialiser_instance_elastic(hosts)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible de se connecter à ElasticSearch')

    try:
        res = es.search(index=nom_index,body={
                "query":{
                    "term":{
                        "_id":{
                            "value":str(id)
                        }
                    }
            }},request_timeout=30)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible d\'interroger ElasticSearch')
    try:
        obs = res['hits']['hits'][0]
    except:
        raise ConsultationIndexProfessionBadRequestException('Le libellé de profession avec l\'identifiant {} est introuvable.'.format(id))
    return {
            'id':int(obs['_id']),
            'libelle_masculinise':obs['_source']['libm'],
            'libelle_masculinise_formate':obs['_source']['libm'],
            'libelle_feminise':obs['_source']['libf'],
            'libelle_feminise_formate':obs['_source']['libm'],
            'priv_cad':obs['_source']['priv_cad'],
            'priv_tec':obs['_source']['priv_tec'],
            'priv_am':obs['_source']['priv_am'],
            'priv_emp':obs['_source']['priv_emp'],
            'priv_onq':obs['_source']['priv_onq'],
            'priv_oq':obs['_source']['priv_oq'],
            'priv_nr':obs['_source']['priv_nr'],
            'pub_catA':obs['_source']['pub_catA'],
            'pub_catB':obs['_source']['pub_catB'],
            'pub_catC':obs['_source']['pub_catC'],
            'pub_nr':obs['_source']['pub_nr'],
            'inde_0_9':obs['_source']['inde_0_9'],
            'inde_10_49':obs['_source']['inde_10_49'],
            'inde_sup49':obs['_source']['inde_sup49'],
            'inde_nr':obs['_source']['inde_nr'],
            'aid_fam':obs['_source']['aid_fam'],
            'ssvaran':obs['_source']['ssvaran'],
            'score':0.0
        }


def rechercher_profession_strict(hosts,nom_index,libelle,genre):
    try:
        es = initialiser_instance_elastic(hosts)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible de se connecter à ElasticSearch')
    if genre is None:
        body = {
            "query":{
                "bool":{
                    "must":{
                        "bool":{
                            "should":[
                                {
                                    "match_phrase":{
                                        "libm_full":'STARTDEBUT '+libelle+' STOPFIN'
                                    }
                                },
                                {
                                "match_phrase":{
                                    "libf_full":'STARTDEBUT '+libelle+' STOPFIN'
                                }
                                }
                            ]

                            }
                        }
                    }
                }
            }
    else:
        body = {
            "query":{
                "bool":{
                    "must":{
                        "match_phrase":{
                                "lib"+str(genre[0])+"_full":'STARTDEBUT '+libelle+' STOPFIN'
                            }
                        }
                    }
                }
            }
    try:
        res = es.search(index=nom_index,body=body,request_timeout=30)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible d\'interroger ElasticSearch')
    if len(res['hits']['hits'])==0:
        return []
    max_score =  float(res['hits']['max_score'])
    echos = res['hits']['hits']
    nb_echos=len(echos)
    k=0
    output = []
    while k<nb_echos:
        try:
            libelle_masculinise_formate = echos[k]['_source']['libm']
        except:
            libelle_masculinise_formate = None
        try:
            libelle_feminise_formate = echos[k]['_source']['libf']
        except:
            libelle_feminise_formate = None
        output.append({
            'id':int(echos[k]['_id']),
            'libelle_masculinise':echos[k]['_source']['libm'],
            'libelle_masculinise_formate':libelle_masculinise_formate,
            'libelle_feminise':echos[k]['_source']['libf'],
            'libelle_feminise_formate':libelle_feminise_formate,
            'priv_cad':echos[k]['_source']['priv_cad'],
            'priv_tec':echos[k]['_source']['priv_tec'],
            'priv_am':echos[k]['_source']['priv_am'],
            'priv_emp':echos[k]['_source']['priv_emp'],
            'priv_onq':echos[k]['_source']['priv_onq'],
            'priv_oq':echos[k]['_source']['priv_oq'],
            'priv_nr':echos[k]['_source']['priv_nr'],
            'pub_catA':echos[k]['_source']['pub_catA'],
            'pub_catB':echos[k]['_source']['pub_catB'],
            'pub_catC':echos[k]['_source']['pub_catC'],
            'pub_nr':echos[k]['_source']['pub_nr'],
            'inde_0_9':echos[k]['_source']['inde_0_9'],
            'inde_10_49':echos[k]['_source']['inde_10_49'],
            'inde_sup49':echos[k]['_source']['inde_sup49'],
            'inde_nr':echos[k]['_source']['inde_nr'],
            'aid_fam':echos[k]['_source']['aid_fam'],
            'ssvaran':echos[k]['_source']['ssvaran'],
            'score':0
        })
        k+=1
    return output
    
def rechercher_informations_codepcs(hosts,nom_index,codepcs):
    code = codepcs
    if code in ['NC','NSP','ATT']:
        code_complet = code
        description = None
        professions_typiques = None
        autres_professions = None
    else:
        code_complet = code + "0"*(4-len(code))
        try:
            es = initialiser_instance_elastic(hosts)
        except:
            raise ConsultationIndexProfessionInternalException('Impossible de se connecter à ElasticSearch')
        try:
            res = es.search(index=nom_index,body={
                "query":{
                    "term":{
                        "code_key":{
                            "value":code
                        }
                    }
            }},request_timeout=30)
        except:
            raise ConsultationIndexProfessionInternalException('Impossible d\'interroger ElasticSearch')

        try:
            obs = res['hits']['hits'][0]
        except:
            raise ConsultationIndexProfessionBadRequestException('Code PCS "{}" non trouvé'.format(codepcs),200)
        
        
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
            professions_typiques = [x.strip() for x in professions_typiques.split('|')]
        except:
            professions_typiques = []
        try:
            autres_professions = obs['_source']['autres_professions']
            autres_professions = [x.strip() for x in  autres_professions.split('|')]
        except:
            autres_professions = []
    return {'intitule': libelle,'code':code_complet,'description':description,'professions_typiques':professions_typiques,'autres_professions':autres_professions} 
