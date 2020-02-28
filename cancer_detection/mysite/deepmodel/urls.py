from django.urls import path
from deepmodel import views
app_name = 'deepmodel'
urlpatterns = [
    path('', views.index, name='index'),
    path('Examine/<int:patient_id>/', views.Examine, name='Examine')
]
