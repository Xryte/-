from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.home, name='home'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
]