from django.urls import path
from django.urls.conf import re_path
from django.urls.resolvers import URLPattern
from . import views
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', views.shelter_list, name='shelter_list'),
    path('shelter/<int:pk>', views.shelter_detail, name='shelter_detail'),
    path('shelter_list', views.shelter_list, name='shelter_list'),
    path('dog/<int:pk>', views.DogDetailView.as_view(), name='dog_detail'),
    path('dog_list', views.DogListView.as_view(), name='dog_list'),
    path('dog/register', views.DogCreateView.as_view(), name='dog_register'),
    path('dog/delete/<int:pk>', views.DogDeleteView.as_view(), name='dog_delete'),
    
    # API
    path('api/shelter_list', views.api_shelter),
    path('api/shelter', views.api_shelter),
    path('api/shelter/<int:pk>', views.api_shelter),
    path('schema/', get_schema_view())
]

