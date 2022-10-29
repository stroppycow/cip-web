from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from .serializers import RechercheLibelleTexteSerializer, RechercheLibelleIDSerializer, RecherchePostePCSCodeSerializer, IndexationNomenclaturePCS2020Serializer, IndexationIndexProfessionSerializer, GetInputFileNomenclatureSerializer
from .elastic.recherche import rechercher_informations_codepcs,rechercher_profession_par_id,rechercher_professions_par_autocompletion, rechercher_profession_strict, get_all_data_nomenclature_pcs2020,get_all_data_index_profession
from .elastic.indexation import indexer_nomenclature_pcs2020, indexer_index_professions
from .elastic.utils import ConsultationIndexProfessionInternalException,ConsultationIndexProfessionBadRequestException
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework import renderers
from rest_framework.decorators import renderer_classes
from rest_framework.views import APIView



class RechercheProfessionAutocompletionView(GenericAPIView):
    """
    Recherche par autocomplétion des professions dans l'index PCS 2020
    """
    serializer_class = RechercheLibelleTexteSerializer


    def post(self,request,format=None):
        serializer = RechercheLibelleTexteSerializer(data=request.data)
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
    
    
class RechercheProfessionStricteView(GenericAPIView):
    """
    Retrouver un libellé de profession dans l'index PCS 2020 à partir de son identifiant
    """
    serializer_class = RechercheLibelleTexteSerializer

    def post(self,request,format=None):
        serializer = RechercheLibelleTexteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                output = rechercher_profession_strict(
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


class CSVRenderer(renderers.BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data.to_csv(sep=",",na_rep="",index=False,encoding="utf-8")


@renderer_classes([CSVRenderer])
class GetInputFileNomenclatureView(APIView):
    """
    Téléchargement la nomenclature actuellement disponible dans l'application
    """
    
    serializer_class  = GetInputFileNomenclatureSerializer
    def get(self,request,format=None):
        serializer = GetInputFileNomenclatureSerializer(data=request.data)
        if serializer.is_valid():
            try:
                output = get_all_data_nomenclature_pcs2020(
                    hosts = settings.ELASTIC['HOST'],
                    nom_index=settings.ELASTIC['INDEX']['nomenclature_pcs2020']
                )
                return Response(data=output,status=status.HTTP_200_OK)
            except ConsultationIndexProfessionInternalException:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@renderer_classes([CSVRenderer])
class GetInputFileIndexView(APIView):
    """
    Téléchargement l'index des professions disponible dans l'application
    """
    
    serializer_class  = GetInputFileNomenclatureSerializer
    def get(self,request,format=None):
        serializer = GetInputFileNomenclatureSerializer(data=request.data)
        if serializer.is_valid():
            try:
                output = get_all_data_index_profession(
                    hosts = settings.ELASTIC['HOST'],
                    nom_index=settings.ELASTIC['INDEX']['index_professions']
                )
                return Response(data=output,status=status.HTTP_200_OK)
            except ConsultationIndexProfessionInternalException:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


