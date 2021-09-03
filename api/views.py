from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from .serializers import RechercheLibelleAutocompletionSerializer, RechercheLibelleIDSerializer, RecherchePostePCSCodeSerializer, IndexationNomenclaturePCS2020Serializer, IndexationIndexProfessionSerializer
from .elastic.recherche import rechercher_informations_codepcs,rechercher_profession_par_id,rechercher_professions_par_autocompletion
from .elastic.indexation import indexer_nomenclature_pcs2020, indexer_index_professions
from .elastic.utils import ConsultationIndexProfessionInternalException,ConsultationIndexProfessionBadRequestException
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser


class RechercheProfessionAutocompletionView(GenericAPIView):
    """
    Recherche par autocomplétion des professions dans l'index PCS 2020
    """
    serializer_class = RechercheLibelleAutocompletionSerializer


    def post(self,request,format=None):
        serializer = RechercheLibelleAutocompletionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                output = rechercher_professions_par_autocompletion(
                    hosts = settings.ELASTIC['HOST'],
                    nom_index=settings.ELASTIC['INDEX']['index_professions'],
                    libelle=serializer.validated_data['libelle'],
                    genre=serializer.validated_data['genre']
                )
            except ConsultationIndexProfessionInternalException:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ConsultationIndexProfessionBadRequestException:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"echos":output,"nb_echos":len(output)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RechercheProfessionIDView(GenericAPIView):
    """
    Retrouver un libellé de profession dans l'index PCS 2020 à partir de son identifiant
    """
    serializer_class = RechercheLibelleIDSerializer

    def post(self,request,format=None):
        serializer = RechercheLibelleIDSerializer(data=request.data)
        if serializer.is_valid():
            try:
                output = rechercher_profession_par_id(
                    hosts = settings.ELASTIC['HOST'],
                    nom_index=settings.ELASTIC['INDEX']['index_professions'],
                    id=serializer.validated_data['id']
                )
            except ConsultationIndexProfessionInternalException:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ConsultationIndexProfessionBadRequestException:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            try:
                output = rechercher_informations_codepcs(
                    hosts = settings.ELASTIC['HOST'],
                    nom_index=settings.ELASTIC['INDEX']['nomenclature_pcs2020'],
                    codepcs=serializer.validated_data['code_pcs']
                )
            except ConsultationIndexProfessionInternalException:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ConsultationIndexProfessionBadRequestException:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"echo":output}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndexationNomenclaturePCS2020View(GenericAPIView):
    """
    Indexation des postes dans la nomenclature dans la PCS 2020
    """
    serializer_class  = IndexationNomenclaturePCS2020Serializer

    def put(self,request,format=None):
        serializer = IndexationNomenclaturePCS2020Serializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['cle_secrete'] == settings.SECRET_KEY:
                try:
                    output = indexer_nomenclature_pcs2020(
                        hosts = settings.ELASTIC['HOST'],
                        nom_index=settings.ELASTIC['INDEX']['nomenclature_pcs2020'],
                        fichier=serializer.validated_data['fichier']
                    )
                except ConsultationIndexProfessionInternalException:
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except ConsultationIndexProfessionBadRequestException:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
            return Response(data={"message":output}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class IndexationIndexProfessionPCS2020View(GenericAPIView):
    """
    Indexation de l'index de profession de la PCS 2020
    """
    serializer_class  = IndexationIndexProfessionSerializer

    def put(self,request,format=None):
        serializer = IndexationIndexProfessionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['cle_secrete'] == settings.SECRET_KEY:
                try:
                    output = indexer_index_professions(
                        hosts = settings.ELASTIC['HOST'],
                        nom_index=settings.ELASTIC['INDEX']['index_professions'],
                        fichier=serializer.validated_data['fichier']
                    )
                except ConsultationIndexProfessionInternalException:
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except ConsultationIndexProfessionBadRequestException:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
            return Response(data={"message":output}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)