from django.conf.urls import include
from django.urls import path
from holygrailapi.views import register_user, login_user
from rest_framework import routers

from holygrailapi.views import ProductViewSet,ClosetProductViewSet, ClosetViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'product', ProductViewSet, 'product')
router.register(r'closetProduct', ClosetProductViewSet, 'closetProduct')
router.register(r'closet', ClosetViewSet, 'closet')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')
    
    ),
]
