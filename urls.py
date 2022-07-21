from django.urls import path
from . import views

urlpatterns = [
   path('', views.CreateShortURLView.as_view(), name='create-short'),
   path('<short>/', views.RetrieveShortURLView.as_view(), name='short-url')
]
