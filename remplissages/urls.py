from django.urls import path

from remplissages import views



app_name = "rempl"

urlpatterns = [
    path('', views.index_rempl, name="index_rempl"),
    path('evangelisation/<int:pk>/detail/<str:passe>/', views.index_rempl, name="evang_detail_passe"),
    #==============================================================================================================
    #===============================CRUD EVANGELISSATION======================================
    path('ajouter-moment-evangelissation', views.add_rempl, name="add_rempl"),
    path('evangelisation/<int:pk>/modifier', views.change_rempl, name="change_rempl"),
    path('evangelisation/<int:pk>/supprimer', views.delete_rempl, name="delete_rempl"),

    #==============================================================================================================
    #===============================CRUD PERSONNE======================================
    path('ajouter-personne', views.add_personne, name="add_personne"),
    path('ajouter-personne/<int:pk>/evangelisation/<str:passe>', views.add_personne, name="add_personne_passe"),
    path('ajouter-personne/plus', views.add_personne_autre, name="add_personne_autre"),
    path('personne/<int:pk>/modifier', views.change_personne, name="change_personne"),
    path('personne/<int:pk>/modifier/evangelisation/<str:passe>/', views.change_personne, name="change_personne_passe"),
    path('personne/<int:pk>/supprimer', views.delete_personne, name="delete_personne"),
    path('personne/<int:pk>/supprimer/evangelisation/<str:passe>/', views.delete_personne, name="delete_personne_passe"),
    path('personne/<int:pk>/detail', views.detail_personne, name="detail_personne"),

    #==============================================================================================================
    #===============================CRUD SITE======================================
    path('ajouter-site', views.add_site, name="add_site"),
    path('site/<int:pk>/modifier', views.change_site, name="change_site"),
    path('site/<int:pk>/supprimer', views.delete_site, name="delete_site"),
    path('liste-site-evangelisation', views.liste_site_evang, name="liste_site"),
]
