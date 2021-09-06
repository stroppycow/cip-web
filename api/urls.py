from django.urls import path
from .views import RecherchePosteNomenclaturePCS2020View, RechercheProfessionAutocompletionView, RechercheProfessionIDView, IndexationNomenclaturePCS2020View,  IndexationIndexProfessionPCS2020View, RechercheProfessionStricteView

urlpatterns = [
    path('profession_auto/', RechercheProfessionAutocompletionView.as_view()),
    path('profession_id/', RechercheProfessionIDView.as_view()),
    path('profession_stricte/', RechercheProfessionStricteView.as_view()),
    path('poste_pcs/', RecherchePosteNomenclaturePCS2020View.as_view()),
    path('indexation_nomenclature_pcs2020/', IndexationNomenclaturePCS2020View.as_view()),
    path('indexation_index_profession/', IndexationIndexProfessionPCS2020View.as_view()),
]
