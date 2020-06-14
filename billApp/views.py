from django.db.models import Sum, ExpressionWrapper, F, fields
from django.shortcuts import render, get_object_or_404
from . import tables
from billApp import models
from billApp.models import Facture, LigneFacture, LigneFactureTable, Client, LigneClientTable, Fournisseur, \
    LigneFournissTable, Category
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django_tables2.config import RequestConfig
from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django_tables2 import SingleTableView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Button
from django.urls import reverse
from . import charts
# Create your views here.

def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context={}
    context['facture'] = facture
    return render(request, 'bill/facture_detail.html', context)


class FactureDetailView(SingleTableView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)

        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')).annotate(total=Sum(
            ExpressionWrapper(
                F('qte') * F('produit__prix'),
                output_field=fields.FloatField()
            )
        )))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class FactureCreate(CreateView):
    model = models.Facture
    fields = ["date", "client"]
    template_name = "bill/create.html"

    def get_context_data(self, **kwargs):
        context = super(FactureCreate, self).get_context_data(**kwargs)
        context["object_name"] = "Facture"
        return context

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DateTimePickerInput()
        return form


class FactureView(SingleTableView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(FactureView, self).get_context_data(**kwargs)

        table = LigneFactureTable(LigneFacture.objects.all().annotate(total=Sum(
            ExpressionWrapper(
                F('qte') * F('produit__prix'),
                output_field=fields.FloatField()
            )
        )))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class ClientUpdateView(UpdateView):
    model = models.Client
    fields = ['nom', "prenom", "adresse", "tel", "sexe"]
    template_name = 'bill/update.html'

    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context["object_name"] = "Client"
        return context

class ClientDetailView(SingleTableView):
    template_name = 'bill/client.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)

        table = LigneClientTable(Client.objects.all().annotate(chiffre_affaire=Sum(ExpressionWrapper(F('facture__lignes__qte')*F('facture__lignes__produit__prix'), output_field=fields.FloatField()))))

        context['table'] = table
        return context

class ClientCreateView(CreateView):
    model = Client
    template_name = 'bill/create.html'
    fields = ['nom', 'prenom', 'adresse','tel','sexe']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()


        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        return form

class FactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/create.html'
    fields = ['facture','produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        return form



class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/create.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
        queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        return form


class LigneFactureUpdateView(SingleTableView):
    model = LigneFacture
    template_name = 'bill/update.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form
class LigneClientUpdateView(UpdateView):
    model = Client
    template_name = 'bill/client_table_update.html'
    fields = ['nom', 'prenom', 'adresse','tel','sexe']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        return form

class LigneFactureDeleteView(DeleteView):
    model = LigneFacture
    template_name = 'bill/delete.html'

    def get_success_url(self):
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/delete.html'

    def get_success_url(self):
        self.success_url = reverse('client-list')



class FournisseurCreateView(CreateView):
    model = Fournisseur
    template_name = 'bill/create.html'
    fields = ['nom', 'prenom', 'adresse','tel']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()


        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        return form
class FournisseurView(SingleTableView):
    template_name = 'bill/fourniss.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(FournisseurView, self).get_context_data(**kwargs)

        table = LigneFournissTable(Fournisseur.objects.all())
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context

class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = 'bill/delete.html'

    def get_success_url(self):
        self.success_url = reverse('fournisseur-list')

class FournisseurUpdateView(UpdateView):
    model = models.Fournisseur
    fields = ['nom', "prenom", "adresse", "tel"]
    template_name = 'bill/update.html'

    def get_context_data(self, **kwargs):
        context = super(FournisseurUpdateView, self).get_context_data(**kwargs)
        context["object_name"] = "Client"
        return context

class DashboardView(TemplateView):
    template_name = "bill/dashboard.html"

    def get_context_data(self,**kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        fournisseur_qs  = models.Fournisseur.objects.annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('produits_forni__lignefacture__qte') * F('produits_forni__prix'),
                output_field=fields.FloatField()
            )
        ))

        client_qs       = models.Client.objects.annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('facture__lignes__qte') * F('facture__lignes__produit__prix'),
                output_field=fields.FloatField()
            )
        )).order_by("-chiffre_affaire")

        context["fournisseur_table"]    = tables.FournisseurWithChiffreAffaireTable(fournisseur_qs)
        context["client_table"]         = tables.ClientWithChiffreAffaireTable(client_qs)
        context["daily_stat"]           = charts.DailyStatChart()
        context["category_stat"]        = charts.CategoryStatChart()
        return context


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'bill/create.html'
    fields = ['nom']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        return form