import django_tables2 as tables
from . import models




class ClientTable(tables.Table):

    class Meta:
        model = models.Client
        template_name = "django_tables2/bootstrap.html"
        fields = ("id","nom","prenom","adresse","tel","sexe","chiffre_affaire","actions")

class FactureTable(tables.Table):
    class Meta:
        model = models.Facture
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','date','total')


class FournisseurTable(tables.Table):

    class Meta:
        model = models.Fournisseur
        template_name = "django_tables2/bootstrap.html"
        fields = ('id','nom','actions')
    
class FournisseurWithChiffreAffaireTable(tables.Table):
    class Meta:
        model = models.Fournisseur
        template_name = "django_tables2/bootstrap.html"
        fields = ('nom','chiffre_affaire')

class ClientWithChiffreAffaireTable(tables.Table):
    class Meta:
        model = models.Client
        template_name = "django_tables2/bootstrap.html"
        fields = ('nom','prenom','chiffre_affaire')

