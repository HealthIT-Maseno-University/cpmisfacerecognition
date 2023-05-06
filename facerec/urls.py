from django.urls import path

from facerec import views

urlpatterns = [
    path('', views.index, name='index'),
]
