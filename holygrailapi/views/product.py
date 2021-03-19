"""View module for handling requests about products"""
import base64
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.http import HttpResponseServerError
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from holygrailapi.models import Product, Closet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import PermissionDenied

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class ProductViewSet(ViewSet):
    """Holygrailapi"""
    permission_classes = [ IsOwnerOrReadOnly ]
    queryset = Product.objects.none()

def retrieve(self, request, pk=None):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8800/product/2
            #
            # The `2` at the end of the route becomes `pk`
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)    

def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
        # Get all product records from the database
        product = Product.objects.all()

        # Support filtering product by closet_id
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        closet_id = self.request.query_params.get('closet_id', None)
        if closet_id is not None:
            product = product.filter(closet__id=closet_id)

        serializer = ProductSerializer(
            product, many=True, context={'request': request})
        return Response(serializer.data)    




class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products"""
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='closet_id'
        )
        fields = ('closet_id', 'product_name', 'price', 'color', 'image_path',
                  'owns', 'image')
        depth = 1

