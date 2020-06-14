from django.urls import path, re_path, include
from billApp import views


urlpatterns = [

    path('', views.DashboardView.as_view(), name="dashboard"),
    path('category/create/', views.CategoryCreateView.as_view(), name="category-create"),

    path('fournisseur/create/', views.FournisseurCreateView.as_view(), name="fournisseur-create"),
    path('fournisseur/', views.FournisseurView.as_view(), name="fournisseur-list"),
    path('fournisseur/delete/<int:pk>', views.FournisseurDeleteView.as_view(), name="fournisseur-delete"),
    path('fournisseur/update/<int:pk>', views.FournisseurUpdateView.as_view(), name='fournisseur-update'),

    path('clients/', views.ClientDetailView.as_view(), name="client-list"),
    path('clients/create/', views.ClientCreateView.as_view(), name="client-create"),
    path('clients/delete/<int:pk>', views.ClientDeleteView.as_view(), name="client-delete"),
    path('clients/update/<int:pk>', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/facture/<int:pk>', views.FactureDetailView.as_view(), name='facture_client'),

    path('facture/create/', views.FactureCreateView.as_view(), name="facture-create"),
    path('newfacture/create/', views.FactureCreate.as_view(), name="newFacture-create"),
    path('factures/', views.FactureView.as_view(), name="facture-list"),




    re_path(r'^facture_table_create/(?P<facture_pk>\d+)/$', views.LigneFactureCreateView.as_view(),name='facture_table_create'),
    re_path(r'^lignefacture_delete/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureDeleteView.as_view(), name='lignefacture_delete'),
    re_path(r'^lignefacture_update/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureUpdateView.as_view(), name='lignefacture_update'),
]