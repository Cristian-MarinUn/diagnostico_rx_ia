from django.urls import path
from . import views

app_name = 'medical_images'

urlpatterns = [
    path('upload/', views.UploadImageView.as_view(), name='upload-image'),
    path('images/', views.ListImagesView.as_view(), name='list-images'),
]
