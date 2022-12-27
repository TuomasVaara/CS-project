from django.urls import path

from .views import homePageView, transferView, mailView, errorView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('mail/', mailView, name='mail'),
    path('error/', errorView, name='error'),
]
