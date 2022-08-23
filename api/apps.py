from django.apps import AppConfig
import os
from .elastic.indexation import indexer_nomenclature_pcs2020, indexer_index_professions
from django.conf import settings
from datetime import datetime, timedelta


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        if os.getenv("DATA_CLASSIFICATION_OCCUPATION") is not None and os.getenv("DATA_INDEX_OCCUPATION") is not None:
            first_timestamp = datetime.now()
            continue_bool = True
            while continue_bool and datetime.now() - first_timestamp < timedelta(minutes=1):
                try:
                    indexer_nomenclature_pcs2020(
                                hosts = settings.ELASTIC['HOST'],
                                nom_index=settings.ELASTIC['INDEX']['nomenclature_pcs2020'],
                                fichier=os.getenv("DATA_CLASSIFICATION_OCCUPATION")
                            )
                    indexer_index_professions(
                        hosts = settings.ELASTIC['HOST'],
                        nom_index=settings.ELASTIC['INDEX']['index_professions'],
                        fichier=os.getenv("DATA_INDEX_OCCUPATION")
                    )
                    continue_bool = False
                except:
                    pass
