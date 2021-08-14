from django.urls import path


from gallerie import views



app_name = 'gallerie'

urlpatterns = [
    path('', views.gallerie_index, name="gallerie_index"),
    path('ajouter-image/', views.gallerie_add_image_gallerie, name="gallerie_add_image_gallerie"),
    path('evangelisation/<int:pk>/', views.gallerie_add_image, name="gallerie_add_image"),
    path('gallerie_detail_image_ajax/<int:pk>/', views.gallerie_detail_image, name="gallerie_detail_image"),
    path('gallerie/<int:pk>/modifier', views.gallerie_update, name="gallerie_update"),
    path('gallerie/<int:pk>/supprimer', views.gallerie_delete, name="gallerie_delete"),
]
