from django.urls import path

from .views import homePageView, transferView, mailView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('mail/', mailView, name='mail'),
]
