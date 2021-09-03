
from pandas.io.pytables import DataCol
from .params import parametrage_index_nomenclature, parametrage_index_profession
import re
from .utils import initialiser_instance_elastic,ConsultationIndexProfessionInternalException,ConsultationIndexProfessionBadRequestException
import pandas as pd

def first_true(liste):
    return liste.index(True)


def indexer_nomenclature_pcs2020(hosts,nom_index,fichier):
    try:
        es = initialiser_instance_elastic(hosts)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible de se connecter à ElasticSearch')
    try:
        data = pd.read_csv(fichier)
        print(data)
    except:
        raise ConsultationIndexProfessionBadRequestException('Impossible d\'interpréter le fichier csv')  
    valider_data_nomenclature(data)
    indexer_data_nomenclature_pcs2020(data.to_dict('records'),es,nom_index)
    return "{} observations ont été indexées".format(data.shape[0])

def valider_data_nomenclature(data):
    #tester la présence des colonnes
    for x in ['code', 'niveau', 'libelle', 'description', 'professions_typiques', 'professions_exclues']:
        if x not in data.columns:
            raise ConsultationIndexProfessionBadRequestException('La colonne "{}" n\'est pas présente dans le csv fourni'.format(x))

    if data.shape[0]<=0:
         raise ConsultationIndexProfessionBadRequestException('La table ne contient aucune observation.')

    # Vérifier que les codes sont de longueur 4
    test = [len(x) != 4 for x in data.code]
    if any(test):
        rang = first_true(test)
        raise ConsultationIndexProfessionBadRequestException('Certains codes ne sont pas de longueur 4 comme "{}" ligne {}.'.format(
            list(data.code)[rang],
            rang+2
        ))
    
    # Vérifier que les niveaux sont entre 1 et 4
    test = [x not in [1,2,3,4] for x in data.niveau]
    if any(test):
        rang = first_true(test)
        raise ConsultationIndexProfessionBadRequestException('Certains niveaux ne sont pas compris entre 1 et 4 comme le niveau "{}" ligne {}'.format(
            list(data.niveau)[rang],
            rang+2
        ))
    
    # Vérifier la cohérence entre le code et le niveau à partir des 0 en dernière position
    test = [a[b:4]!='0'*(4-b) for (a,b) in zip(data.code,data.niveau)]
    if any(test):
        rang = first_true(test)
        raise ConsultationIndexProfessionBadRequestException('Certains codes ne sont pas cohérents avec le niveau comme le code "{}" avec le niveau "{}" ligne {}.'.format(
            list(data.code)[rang],
            list(data.niveau)[rang],
            rang+2
        ))

    # Vérifier que chaque couple (code,niveau) est unique
    couples_code_niveau = {cle:0 for cle in list(set([(a,b) for a,b in zip(data.code,data.niveau)]))}
    for a,b in zip(data.code,data.niveau):
        couples_code_niveau[(a,b)]+=1
    test = [x>1 for x in couples_code_niveau.values()]
    if any(test):
        raise ConsultationIndexProfessionBadRequestException('Certains couple (code,niveau) apparaissent en doublon "{}".'.format(
            couples_code_niveau[first_true(test)]
        ))
    
    # Vérifier que tous les intitulés sont présents
    test = [isinstance(x,float) for x in data.libelle]
    if any(test):
        raise ConsultationIndexProfessionBadRequestException('Certains intitule de poste de la nomenclature sont manquants comme celui ligne {}.'.format(
            first_true(test)+2
        ))


def indexer_data_nomenclature_pcs2020(data,es,nom_index):
    try:
        if es.indices.exists(nom_index):
            es.indices.delete(nom_index)
        es.indices.create(index = nom_index, body = parametrage_index_nomenclature, request_timeout=300)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible de créer l\'index ElasticSearch')
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
    try:
        es.bulk(index = nom_index, body = bulk_data,request_timeout=300)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible d\'indexer les données dans ElasticSearch')

def indexer_index_professions(hosts,nom_index,fichier):
    try:
        es = initialiser_instance_elastic(hosts)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible de se connecter à ElasticSearch')
    try:
        data = pd.read_csv(fichier)
        print(data)
    except:
        raise ConsultationIndexProfessionBadRequestException('Impossible d\'interpréter le fichier csv')  
    valider_data_index(data)
    indexer_data_index_professions(data.to_dict('records'),es,nom_index)
    return "{} observations ont été indexées".format(data.shape[0])

def valider_data_index(data):
    #tester la présence des colonnes
    for x in ['id','libm','libf','priv_cad','priv_tec','priv_am','priv_emp','priv_oq','priv_onq','priv_nr','pub_catA','pub_catB','pub_catC','pub_nr','inde_0_9','inde_10_49','inde_sup49','inde_nr','aid_fam','ssvaran']:
        if x not in data.columns:
            raise ConsultationIndexProfessionBadRequestException('La colonne "{}" n\'est pas présente dans le csv fourni'.format(x))

    if data.shape[0]<=0:
         raise ConsultationIndexProfessionBadRequestException('La table ne contient aucune observation.')

    # Vérifier que les id sont uniques
    if len(list(set(data.id))) != len(list(data.id)):
        raise ConsultationIndexProfessionBadRequestException('La colonne id ne contient pas uniquement des identifiants uniques.')
    
    # Vérifier que tous les intitulés sont présents
    test = [isinstance(x,float) for x in data.libm]
    if any(test):
        raise ConsultationIndexProfessionBadRequestException('Certains libelle de profession au masculin sont manquants comme celui ligne {}.'.format(
            first_true(test)+2
        ))

    #Vérifier que les codes pcs sont au bon format
    pattern_pcs = re.compile(r'(r|[1-6][0-9][A-Z0][0-9])')
    for i in data.index:
        for c in ['priv_cad','priv_tec','priv_am','priv_emp','priv_oq','priv_onq','priv_nr','pub_catA','pub_catB','pub_catC','pub_nr','inde_0_9','inde_10_49','inde_sup49','inde_nr','aid_fam','ssvaran']:
            if data.at[i,c] is None:
                raise ConsultationIndexProfessionBadRequestException('Le code PCS 2020 pour la variable "{}" ligne {} est manquant.'.format(
                    c,
                    int(i)+2
                ))
            if pattern_pcs.fullmatch(data.at[i,c]) is None:
                raise ConsultationIndexProfessionBadRequestException('Le code PCS 2020 "{}" pour la variable "{}" ligne {} est invalide.'.format(
                    data.at[i,c],
                    c,
                    int(i)+2
                ))
    
def indexer_data_index_professions(data,es,nom_index):
    try:
        if es.indices.exists(nom_index):
            es.indices.delete(nom_index)
        es.indices.create(index = nom_index, body = parametrage_index_profession, request_timeout=300)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible de créer l\'index ElasticSearch')

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
    try:
        es.bulk(index = nom_index, body = bulk_data,request_timeout=300)
    except:
        raise ConsultationIndexProfessionInternalException('Impossible d\'indexer les données dans ElasticSearch')