from django.urls import path
from .views import ResourceView

urlpatterns = [
    path('resource/<str:name>/', ResourceView.as_view(), name = 'resource-detail'),
]
