from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from .serializers import RechercheLibelleAutocompletionSerializer, RechercheLibelleIDSerializer, RecherchePostePCSCodeSerializer
from .elastic.recherche import rechercher_informations_codepcs,rechercher_profession_par_id,rechercher_professions_par_autocompletion
from rest_framework.generics import GenericAPIView



class RechercheProfessionAutocompletionView(GenericAPIView):
    """
    Recherche par autocomplétion des professions dans l'index PCS 2020
    """
    serializer_class = RechercheLibelleAutocompletionSerializer


    def post(self,request,format=None):
        serializer = RechercheLibelleAutocompletionSerializer(data=request.data)
        if serializer.is_valid():
            output = rechercher_professions_par_autocompletion(
                hosts = settings.ELASTIC['HOST'],
                nom_index=settings.ELASTIC['INDEX']['index_professions'],
                libelle=serializer.validated_data['libelle'],
                genre=serializer.validated_data['genre']
            )
            return Response(data={"echos":output,"nb_echos":len(output)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RechercheProfessionIDView(GenericAPIView):
    """
    Retrouver un libellé de profession dans l'index PCS 2020 à artir de son identifiant
    """
    serializer_class = RechercheLibelleIDSerializer


    def post(self,request,format=None):
        serializer = RechercheLibelleAutocompletionSerializer(data=request.data)
        if serializer.is_valid():
            output = rechercher_profession_par_id(
                hosts = settings.ELASTIC['HOST'],
                nom_index=settings.ELASTIC['INDEX']['index_professions'],
                id=serializer.validated_data['id']
            )
            return Response(data={"echo":output}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecherchePosteNomenclaturePCS2020View(GenericAPIView):
    """
    Retrouver un poste dans la nomenclature PCS 2020 à partir du code
    """
    serializer_class = RecherchePostePCSCodeSerializer


    def post(self,request,format=None):
        serializer = RecherchePostePCSCodeSerializer(data=request.data)
        if serializer.is_valid():
            output = rechercher_informations_codepcs(
                hosts = settings.ELASTIC['HOST'],
                nom_index=settings.ELASTIC['INDEX']['nomenclature_pcs2020'],
                codepcs=serializer.validated_data['id']
            )
            return Response(data={"echo":output}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)