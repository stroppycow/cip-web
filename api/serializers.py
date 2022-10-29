from rest_framework import serializers

class EchoLibelleProfessionEnrichi(serializers.Serializer):
    id = serializers.IntegerField(
        allow_null=False,
        label="Identifiant",
        help_text="Identifiant du libellé de profession dans l'index"
    )
    libelle_masculinise = serializers.CharField(
        max_length=255,
        allow_blank=False,
        label="Libellé de profession au masculin sans formatage",
        help_text="Libellé de profession masculinisé sans formatage"
    )
    libelle_masculinise_formate = serializers.CharField(
        max_length=255,
        allow_blank=True,
        label="Libellé de profession au masculin avec formatage",
        help_text="Libellé de profession masculinisé avec formatage (encadrement avec des balises html bold) de la partie du libellé correspondant à celui renseigné"
    )
    libelle_feminise = serializers.CharField(
        max_length=255,
        allow_blank=False,
        label="Libellé de profession au feminin sans formatage",
        help_text="Libellé de profession féminisé sans formatage"
    )
    libelle_feminise_formate = serializers.CharField(
        max_length=255,
        allow_blank=True,
        label="Libellé de profession au feminin avec formatage",
        help_text="Libellé de profession féminisé avec mise en gras (encadrement avec des balises html bold) de la partie du libellé correspondant à celui renseigné"
    )
    priv_cad = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les cadres du secteur privé",
        help_text="Codage PCS 2020 pour les cadres du secteur privé"
    )
    priv_tec = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les technicien.ne.s du secteur privé",
        help_text="Codage PCS 2020 pour les technicien.ne.s du secteur privé"
    )
    priv_am = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les agents de maitrise du secteur privé",
        help_text="Codage PCS 2020 pour les agents de maitrise du secteur privé"
    )
    priv_emp = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les employé.e.s du secteur privé",
        help_text="Codage PCS 2020 pour les employé.e.s du secteur privé"
    )
    priv_oq = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les ouvriers et ouvrières qualifié.e.s du secteur privé",
        help_text="Codage PCS 2020 pour les ouvriers et ouvrières du secteur privé"
    )
    priv_onq = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les ouvriers et ouvrières du secteur privé",
        help_text="Codage PCS 2020 pour les ouvriers et ouvrières du secteur privé"
    )
    priv_nr = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les salariés du secteur privé en cas de classification professionnelle inconnue",
        help_text="Codage PCS 2020 pour les salariés du secteur privé en cas de classification professionnelle inconnue"
    )
    pub_catA = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les agents de catégorie A de la fonction publique",
        help_text="Codage PCS 2020 pour les agents de catégorie A de la fonction publique"
    )
    pub_catB = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les agents de catégorie B de la fonction publique",
        help_text="Codage PCS 2020 pour les agents de catégorie B de la fonction publique"
    )
    pub_catC = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les agents de catégorie C de la fonction publique",
        help_text="Codage PCS 2020 pour les agents de catégorie C de la fonction publique"
    )
    pub_nr = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les salariés du public en cas de classification professionnelle inconnue",
        help_text="Codage PCS 2020 pour les salariés du secteur privé en cas de classification professionnelle inconnue"
    )
    inde_0_9 = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les independants et chefs d'entreprise de 0 à 9 salariés",
        help_text="Codage PCS 2020 pour les independants et chefs d'entreprise de 0 à 9 salariés"
    )
    inde_10_49 = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les independants et chefs d'entreprise de 10 à 49 salariés",
        help_text="Codage PCS 2020 pour les independants et chefs d'entreprise de 10 à 49 salariés"
    )
    inde_sup49 = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les independants et chefs d'entreprise de plus de 50 salariés",
        help_text="Codage PCS 2020 pour les independants et chefs d'entreprise de plus de 50 salariés"
    )
    inde_nr = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les independants et chefs d'entreprise où le nombre de salarié est inconnu",
        help_text="Codage PCS 2020 pour les independants et chefs d'entreprise où le nombre de salarié est inconnu"
    )
    aid_fam = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 pour les aides familiaux",
        help_text="Codage PCS 2020 pour les aides familiaux"
    )
    ssvaran = serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Codage PCS 2020 par défaut en l'absence d'information annexe disponible",
        help_text="Codage PCS 2020 par défaut en l'absence d'information annexe disponible"
    )
    score = serializers.FloatField(
        label="Score de pertinence de l'écho trouvé",
        help_text="Score provenant de la recherche par ElasticSearch de cet écho"
    )


class PosteNomenclaturePCS2020(serializers.Serializer):
    code =serializers.CharField(
        max_length=4,
        allow_blank=True,
        label="Code PCS 2020",
        help_text="Code PCS 2020"
    )
    intitule = serializers.CharField(
        max_length=255,
        allow_blank=True,
        label="Intitulé du poste dans la nomenclature PCS 2020",
        help_text="Intitulé du poste dans la nomenclature PCS 2020"
    )
    description = serializers.CharField(
        allow_blank=True,
        label="Description du poste nomenclature PCS 2020",
        help_text="Description du poste nomenclature PCS 2020"
    )
    professions_typiques = serializers.ListField(
        label="Liste des professions les plus typiques",
        help_text="Liste des professions les plus typiques",
        child=serializers.CharField(),
        allow_empty=True
    )
    autres_professions = serializers.ListField(
        label="Liste des professions exclues",
        help_text="Liste des professions exclues",
        child=serializers.CharField(),
        allow_empty=True
    )
   

class RechercheLibelleTexteSerializer(serializers.Serializer):
    libelle = serializers.CharField(
        max_length=255,
        allow_blank=True,
        write_only=True,
        label="Libellé de profession à rechercher dans l'index",
        help_text="Libellé de profession à rechercher dans l'index"
    )
    genre = serializers.ChoiceField(
        allow_blank=True,
        choices=['masculin','feminin'],
        write_only=True,
        label="Genre du libellé recherché",
        help_text="Genre du libellé recherché"
    )
    echos = serializers.ListField(
        label="Liste des échos trouvés",
        read_only=True,
        child=EchoLibelleProfessionEnrichi(),
        allow_empty=True
    )
    nb_echos = serializers.IntegerField(
        label="Nombre d'échos trouvés",
        read_only=True,
        min_value=0
    )
    
class RechercheLibelleIDSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label="Libellé de profession à rechercher dans l'index",
        write_only=True,
        help_text="Libellé de profession à rechercher dans l'index"
    )
    echo = EchoLibelleProfessionEnrichi(
        label='Echo trouvé',
        read_only=True
    )

class RecherchePostePCSCodeSerializer(serializers.Serializer):
    code_pcs = serializers.CharField(
        label="Code PCS 2020 à rechercher",
        write_only=True,
        help_text="Code PCS 2020"
    )
    echo = PosteNomenclaturePCS2020(
        label='Poste de la nomenclature PCS 2020 trouvé',
        read_only=True
    )

class IndexationNomenclaturePCS2020Serializer(serializers.Serializer):
    cle_secrete = serializers.CharField(
        label="Code secret de l'application",
        write_only=True,
        help_text="Code secret de l'application"
    )
    fichier = serializers.FileField(
        max_length=None,
        allow_empty_file=False,
        use_url=True
    )
    message = serializers.CharField(
        label="Message de retour lors de l'indexation",
        read_only=True
    )

class IndexationIndexProfessionSerializer(serializers.Serializer):
    cle_secrete = serializers.CharField(
        label="Code secret de l'application",
        write_only=True,
        help_text="Code secret de l'application"
    )
    fichier = serializers.FileField(
        max_length=None,
        allow_empty_file=False,
        use_url=True
    )
    message = serializers.CharField(
        label="Message de retour lors de l'indexation",
        read_only=True
    )

class GetInputFileNomenclatureSerializer(serializers.Serializer):
    fichier = serializers.FileField(
        max_length=None,
        allow_empty_file=False,
        use_url=True,
        read_only=True
    )
