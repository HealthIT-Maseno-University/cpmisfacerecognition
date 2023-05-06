from django.urls import path

from facerec import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report_missing/', views.add_missing_child, name="report_missing")

]
