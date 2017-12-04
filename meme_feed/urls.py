from django.conf.urls import url, include
from rest_framework import routers
from meme_feed import views


router = routers.DefaultRouter()
router.register(r'memes', views.MemeViewSet)
router.register(r'authors', views.AuthorsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^facebook-login', views.facebook_login, name='facebook_login')
]