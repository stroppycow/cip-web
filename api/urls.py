from django.urls import path
from .views import RecherchePosteNomenclaturePCS2020View, RechercheProfessionAutocompletionView, RechercheProfessionIDView

urlpatterns = [
    path('profession_auto/', RechercheProfessionAutocompletionView.as_view()),
    path('profession_id/', RechercheProfessionIDView.as_view()),
    path('poste_pcs/', RecherchePosteNomenclaturePCS2020View.as_view()),
]