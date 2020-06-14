from django.db.models import Avg, Count, Min, Sum,ExpressionWrapper,fields,F
from .models import Facture, Category
from jchart import Chart
from jchart.config import DataSet

class DailyStatChart(Chart):
    chart_type = 'line'
    qs = Facture.objects.values('date').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('lignes__qte') * F('lignes__produit__prix'),
                output_field=fields.FloatField()
            )
        ))
    
    def get_datasets(self, **kwargs):
        
        return [DataSet(
            color=(60, 170, 20),
            data=list(self.qs.values_list('chiffre_affaire',flat=True)),
            label="l'évolution du chiffre d'affaire"
            )]

    def get_labels(self, **kwargs):
        return list(self.qs.values_list('date',flat=True))

class CategoryStatChart(Chart):
    chart_type = 'radar'
    qs = Category.objects.values('nom').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('produit__lignefacture__qte') * F('produit__prix'),
                output_field=fields.FloatField()
            )
        ))
    
    def get_datasets(self, **kwargs):
        
        return [DataSet(
            color=(245, 66, 170), 
            data=list(self.qs.values_list('chiffre_affaire',flat=True)),
            label="chiffre d'affaire par Categorie"
            )]

    def get_labels(self, **kwargs):
        return list(self.qs.values_list('nom',flat=True))