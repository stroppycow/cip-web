parametrage_index_nomenclature = {
        'settings' : {
            'refresh_interval' : '2s',
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'index' : {
                    'analysis': {
                        'analyzer': {
                            'lib_analyzer':{
                                'type'     : 'custom',
                                'tokenizer': 'lib_autocomplete_tokenizer',
                                'filter'   : ['asciifolding' ,'lowercase','french_stop','french_stemmer','french_elision']
                            },
                            'code_analyzer':{
                                'type' : 'custom',
                                'tokenizer':    'code_autocomplete_tokenizer',
                                'char_filter' : ['espace_supp'],
                                'filter'   :    ['asciifolding','lowercase']
                            }
                         },
                         'tokenizer':{
                            'lib_autocomplete_tokenizer':{
                                'type': 'edge_ngram',
                                'min_gram': 2,
                                'max_gram': 10,
                                'token_chars': ['letter','digit']
                            },
                            'code_autocomplete_tokenizer':{
                                'type':     'edge_ngram',
                                'min_gram': 1,
                                'max_gram': 4,
                                'token_chars': ['letter','digit']
                            },
                        },
                         'char_filter' : {
                            'espace_supp': {
                                'type':'pattern_replace',
                                'pattern':'(\u0020|\u002d)',
                                'replacement':''
                            }
                        },
                        'filter':{
                            'french_elision':{
                                'type':'elision',
                                'articles_case': True,
                                'articles': ['l', 'm', 't', 'qu', 'n', 's', 'j', 'd', 'c'],
                             },
                             'french_stop':{
                              'type':       'stop',
                              'stopwords':  '_french_' 
                            },
                            'french_stemmer':{
                                'type': 'stemmer',
                                'language': 'light_french'
                            },
                            'lib_autocomplete_filter':{
                                'type':     'edge_ngram',
                                'min_gram': 1,
                                'max_gram': 20
                            },
                            'code_autocomplete_filter':{
                                'type':     'edge_ngram',
                                'min_gram': 1,
                                'max_gram': 4
                            }
                        }
                    }
            }
        },
        'mappings': {
            'properties': {
                'niveau': {'type': 'keyword'},
                'code': {'type':'text','analyzer':'code_analyzer','search_analyzer':'code_analyzer'},
                'code_key': {'type':'keyword'},
                'libelle': {'type': 'text','analyzer': 'lib_analyzer', 'search_analyzer': 'lib_analyzer'},
                'description':{'type':'text'},
                'professions_typiques':{'type':'text'},
                'autres_professions':{'type':'text'}
            }
        }
}

parametrage_index_profession = {
        'settings' : {
            'refresh_interval' : '2s',
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'index' : {
                    'analysis': {
                        'analyzer': {
                            'lib_auto_analyzer':{
                                'type'     : 'custom',
                                'tokenizer': 'lib_autocomplete_tokenizer',
                                'filter'   : ['asciifolding' ,'lowercase','french_stop','french_stemmer','french_elision']
                            },
                            'lib_analyzer':{
                                'type'     : 'custom',
                                'tokenizer': 'standard',
                                'char_filter': 'stopword_french',
                                'filter'   : ['asciifolding' ,'lowercase']
                            }
                         },
                         'char_filter' : {
                            'espace_supp': {
                                'type':'pattern_replace',
                                'pattern':'(\u0020|\u002d)',
                                'replacement':''
                            },
                            'stopword_french':{
                                'type':'pattern_replace',
                                'pattern':'( (a|au|aux|avec|ce|ces|dans|de|des|du|elle|en|et|eux|il|je|la|le|leur|lui|ma|mais|me|même|mes|moi|mon|ne|nos|notre|nous|on|ou|par|pas|pour|qu|que|qui|sa|se|ses|sur|ta|te|tes|toi|ton|tu|un|une|vos|votre|vous|c|d|j|l|à|m|n|s|t|y|étée|étées|étant|suis|es|êtes|sont|serai|seras|sera|serons|serez|seront|serais|serait|serions|seriez|seraient|étais|était|étions|étiez|étaient|fus|fut|fûmes|fûtes|furent|sois|soit|soyons|soyez|soient|fusse|fusses|fussions|fussiez|fussent|ayant|eu|eue|eues|eus|ai|avons|avez|ont|aurai|aurons|aurez|auront|aurais|aurait|aurions|auriez|auraient|avais|avait|aviez|avaient|eut|eûmes|eûtes|eurent|aie|aies|ait|ayons|ayez|aient|eusse|eusses|eût|eussions|eussiez|eussent|ceci|cela|celà|cet|cette|ici|ils|les|leurs|quel|quels|quelle|quelles|sans|soi))+ ',
                                'replacement':' ',
                                'flags': 'CASE_INSENSITIVE'
                            }
                        },
                        'tokenizer':{
                            'lib_autocomplete_tokenizer':{
                                'type':     'edge_ngram',
                                'min_gram': 2,
                                'max_gram': 10,
                                'token_chars': ['letter','digit']
                            },
                        },
                        'filter':{
                            'french_elision':{
                                'type':'elision',
                                'articles_case': True,
                                'articles': ['l', 'm', 't', 'qu', 'n', 's', 'j', 'd', 'c'],
                             },
                             'french_stop':{
                              'type':       'stop',
                              'stopwords':  ["au","aux","avec","ce","ces","dans","de","des","du","elle","en","et","eux","il","je","la","le","leur","lui","ma","mais","me","même","mes","moi","mon","ne","nos","notre","nous","on","ou","par","pas","pour","qu","que","qui","sa","se","ses","sur","ta","te","tes","toi","ton","tu","un","une","vos","votre","vous","c","d","j","l","à","m","n","s","t","y","étée","étées","étant","suis","es","êtes","sont","serai","seras","sera","serons","serez","seront","serais","serait","serions","seriez","seraient","étais","était","étions","étiez","étaient","fus","fut","fûmes","fûtes","furent","sois","soit","soyons","soyez","soient","fusse","fusses","fussions","fussiez","fussent","ayant","eu","eue","eues","eus","ai","avons","avez","ont","aurai","aurons","aurez","auront","aurais","aurait","aurions","auriez","auraient","avais","avait","aviez","avaient","eut","eûmes","eûtes","eurent","aie","aies","ait","ayons","ayez","aient","eusse","eusses","eût","eussions","eussiez","eussent","ceci","cela","celà","cet","cette","ici","ils","les","leurs","quel","quels","quelle","quelles","sans","soi"] 
                            },
                            'french_stemmer':{
                                'type': 'stemmer',
                                'language': 'light_french'
                            },
                            'code_autocomplete_filter':{
                                'type':     'edge_ngram',
                                'min_gram': 1,
                                'max_gram': 4
                            }
                        }
                    }
            }
        },
        'mappings': {
            'properties': {
                'id' : {'type': 'keyword'},
                'libm': {'type': 'text','analyzer': 'lib_auto_analyzer', 'search_analyzer': 'lib_auto_analyzer'},
                'libf': {'type': 'text','analyzer': 'lib_auto_analyzer', 'search_analyzer': 'lib_auto_analyzer'},
                'libm_full': {'type': 'text','analyzer': 'lib_analyzer', 'search_analyzer': 'lib_analyzer'},
                'libf_full': {'type': 'text','analyzer': 'lib_analyzer', 'search_analyzer': 'lib_analyzer'},
                'libm_first': {'type': 'text','analyzer': 'lib_analyzer', 'search_analyzer': 'lib_analyzer'},
                'libf_first': {'type': 'text','analyzer': 'lib_analyzer', 'search_analyzer': 'lib_analyzer'},
                'priv_cad': {'type': 'keyword'},
                'priv_tec': {'type': 'keyword'},
                'priv_am': {'type': 'keyword'},
                'priv_emp': {'type': 'keyword'},
                'priv_oq': {'type': 'keyword'},
                'priv_onq': {'type': 'keyword'},
                'priv_nr': {'type': 'keyword'},
                'pub_catA': {'type': 'keyword'},
                'pub_catB': {'type': 'keyword'},
                'pub_catC': {'type': 'keyword'},
                'pub_nr': {'type': 'keyword'},
                'inde_0_9': {'type': 'keyword'},
                'inde_10_49': {'type': 'keyword'},
                'inde_sup49': {'type': 'keyword'},
                'inde_nr': {'type': 'keyword'},
                'aid_fam': {'type': 'keyword'},
                'ssvaran': {'type': 'keyword'}
            }
        }
}
