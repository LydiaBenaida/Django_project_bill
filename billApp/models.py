from tkinter import Button

from django.db import models
from django import utils
import datetime
import django_tables2 as tables
from django.db.models import ExpressionWrapper, Sum, F, FloatField


class Client(models.Model):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length = 10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices = SEXE)
    
    def __str__(self):
        return self.nom + ' ' + self.prenom



class Fournisseur(models.Model):
    """
    Model Fournisseur
    """
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nom + ' ' + self.prenom
class Category(models.Model):
    nom         = models.CharField(max_length=120)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, related_name="produits_forni")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation
    
class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(default=utils.timezone.now)

    # add __str__ magic method to facture.
    def __str__(self):
        return f"Client: {self.client}, {self.date}"

    """
    get total price of this facture.
    we used the aggregate function with the F class of models package so we can produce one query that
    basically sum the product of the price of a product and it quantity.
    """
    def get_total(self):
        return self.lignes.all().aggregate(total=models.Sum(models.F("produit__prix") * models.F("qte"), output_field=models.FloatField()))['total']

class LigneFacture(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField(default=1)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produit', 'facture'], name="produit-facture")
        ]

    def __str__(self):
        return f"{self.produit}, {self.qte}, {self.facture}"







class LigneFactureTable(tables.Table):
    action = '<a href= "{% url "lignefacture_delete" pk=record.id facture_pk=record.id %}" class ="btn btn-danger" > Supprimer </a> '

    edit = tables.TemplateColumn(action)


    edit = tables.TemplateColumn(action)
    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation','produit__prix', 'qte', 'produit__fournisseur' ,'total')

class LigneClientTable(tables.Table):
    action = '<a href="{% url "client_update" pk=record.id  %}" class ="btn btn-warning" > Modifier </a>\
    <a href= "{% url "facture_client" pk=record.id  %}" class ="btn btn-success" > lister </a>\
    <a href= "{% url "client-delete" pk=record.id  %}" class ="btn btn-danger" > Supprimer </a> '

    edit = tables.TemplateColumn(action)


    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nom','prenom', 'adresse', 'tel','chiffre_affaire')

class LigneFournissTable(tables.Table):
    action = '<a href="{% url "fournisseur-update" pk=record.id  %}" class ="btn btn-warning" > Modifier </a>\
    <a href= "{% url "fournisseur-delete" pk=record.id  %}" class ="btn btn-danger" > Supprimer </a> '

    edit = tables.TemplateColumn(action)


    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nom','prenom', 'adresse', 'tel')


