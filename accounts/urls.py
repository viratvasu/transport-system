from django.urls import path
from .views import getInfo
urlpatterns = [
    path('get_info/',getInfo.as_view()),
]