from django.conf.urls import url, include
from rest_framework import routers
from meme_feed import views


router = routers.DefaultRouter()
router.register(r'memes', views.MemeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]