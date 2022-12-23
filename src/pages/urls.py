from django.urls import path

from .views import homePageView, transferView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
]
