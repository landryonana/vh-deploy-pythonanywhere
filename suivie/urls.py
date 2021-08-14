from django.urls import path


from suivie import views



app_name = 'suivie'

urlpatterns = [
    path('', views.index_suivie, name="index_suivie"),
    path('ajout-suivi/<int:pk>', views.add_suivie, name="add_suivie"),
]
