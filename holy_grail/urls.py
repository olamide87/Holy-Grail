from holygrailapi.views.product import ProductViewSet
from django.conf.urls import include
from django.urls import path
from holygrailapi.views import register_user, login_user
from holygrailapi.views import ProductViewSet,ClosetProductViewset, ClosetViewset
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'product', ProductViewSet, 'product')
router.register(r'closetProduct', ClosetProductViewset, 'closetProduct')
router.register(r'closet', ClosetViewset, 'closet')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')
    
    ),
]
