from django.urls import path
from . import views

app_name = 'pdf_processor'

urlpatterns = [
    path('', views.home, name='home'),
    path('merge/', views.merge_pdfs, name='merge_pdfs'),
    path('split/', views.split_pdf, name='split_pdf'),
    path('compress/', views.compress_pdf, name='compress_pdf'),
    path('extract-text/', views.extract_text, name='extract_text'),
    path('extract-images/', views.extract_images, name='extract_images'),
    path('protect/', views.protect_pdf, name='protect_pdf'),
]
