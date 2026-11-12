from django.urls import path, include
from pets import views

app_name = 'pets'

urlpatterns = [
    path('add/', views.AddPetView.as_view(), name='add'),
    path('/pet/<slug:pet_slug>/', include([
        path('', views.PetDetailView.as_view(), name='details'),
        path('edit/', views.EditPetView.as_view(), name='edit'),
        path('delete/', views.DeletePetView.as_view(), name='delete'),
    ]))
]