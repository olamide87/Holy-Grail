from holygrailapi.models import Product, Closet
from holygrailapi.models.closetProduct import ClosetProduct
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers


class ClosetProductViewSet(ViewSet):
  """HolyGrail ClosetProduct"""

  def retrieve(self, request, pk=None):
        """Handle GET requests for single closetProduct

        Returns:
            Response -- JSON serialized closetProduct
        """
        try:
            closetProduct = ClosetProduct.objects.get(pk=pk)
            serializer = ClosetProductSerializer(closetProduct, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

  def list(self, request):
        """Handle GET requests to get all closetProduct

        Returns:
            Response -- JSON serialized list of closetProduct
        """
        closetProduct = ClosetProduct.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ClosetProductSerializer(
            closetProduct, many=True, context={'request': request})
        return Response(serializer.data)

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product"""
    class Meta:
        model = Product
        fields = ('product_name','color','image','price','owns')       


class ClosetProductSerializer(serializers.ModelSerializer):
    """JSON serializer for closetProduct

    Arguments:
        serializers
    """
    product_id = ProductSerializer(many=False)

    class Meta:
        model = ClosetProduct
        fields = ('product_id', 'closet_id', 'id')
        depth = 1
 
