from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin
from meme_feed import views


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()
router.register(r'authors', views.AuthorsViewSet)
meme_router = router.register(r'memes', views.MemeViewSet)

meme_router.register(
    r'comments',
    views.CommentViewSet,
    base_name='comments',
    parents_query_lookups=['commented_object']
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^facebook-login', views.facebook_login, name='facebook_login'),
    url(r'^get-owner', views.jwt_get_owner, name='jwt_get_owner'),
    url(r'^toggle-real-photo', views.toggle_real_photo, name='toggle_real_photo'),
    url(r'^toggle-real-name', views.toggle_real_name, name='toggle_real_photo'),
]
