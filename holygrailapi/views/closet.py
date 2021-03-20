# from stockxsdk import Stockx

# stockx = Stockx()

# email = 'nijaboi@yahoo.com'
# password = 'Nigeria1$'
# logged_in = stockx.authenticate(email, password)
# stockx.authenticate(email, password)

# print(logged_in)

"""View module for handling requests about closet"""
from holygrailapi.models import closet
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from holygrailapi.models import Closet

class ClosetViewSet(ViewSet):
    """Holygrail Closets"""

    def list(self, request):
        """Handle GET requests to get all closets
        Returns:
            Response -- JSON serialized list of closets
        """
        closet = Closet.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ClosetSerializer(
            closet, many=True, context={'request': request})
        return Response(serializer.data)



class ClosetSerializer(serializers.ModelSerializer):
    """JSON serializer for closet
    Arguments:
        serializers
    """
    class Meta:
        model = Closet
        fields = ('title', 'user')

