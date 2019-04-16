from django.urls import path, include
from . import views

api_patterns = [
    path('chat', views.chat),
]
urlpatterns = [
    path('api/', include(api_patterns)),
]
