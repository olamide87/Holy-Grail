"""View module for handling requests about products"""
import base64
from django.contrib.auth.models import User
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
from holygrailapi.models import Product, Closet, ClosetProduct
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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        # product = Product.objects.get(user=request.auth.user)

        # Create a new Python instance of the Product class
        # and set its properties from what was sent in the
        # body of the request from the client.
        product = Product()
        product.product_name = request.data["product_name"]
        product.color = request.data["color"]
        product.image = request.data["image"]
        product.price = request.data["price"]
        product.owns = request.data["owns"]

        closetProduct = ClosetProduct()


        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.
        closet = Closet.objects.get(pk=request.data["closet_id"])
        closetProduct.closet_id = closet

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            product.save()
            closetProduct.product_id = product
            closetProduct.save()
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a product
        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)

        # product.product_name = request.data["product_name"]
        # product.color = request.data["color"]
        # product.image = request.data["image"]
        # product.price = request.data["price"]
        product.owns = request.data["owns"]


    
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
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


        closetId = self.request.query_params.get('type', None)
        if closetId is not None:
            product = product.filter(closetproduct__closet_id=closetId)

        # Support filtering product by closet_id
        #    http://localhost:8000/games?type=1
        #
        

        serializer = ProductSerializer(
            product, many=True, context={'request': request})
        return Response(serializer.data)

            

            



class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products"""
    class Meta:
        model = Product
        fields = ('product_name', 'price', 'color', 'image',
                  'owns', 'image', 'id')
        depth = 1

