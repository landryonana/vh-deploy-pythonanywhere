from django.urls import path


from rapport import views



app_name = 'rapport'

urlpatterns = [
    path('', views.index_rapport, name="index_rapport"),
    path('rapport-detail/<str:mois>/', views.rapport_evang_detail_sortie, name="rapport_evang_detail_sortie"),
    path('rapport-pdf', views.rapport_pdf, name="rapport_pdf"),
    path('rapport-excel', views.rapport_excel, name="rapport_excel"),
]
