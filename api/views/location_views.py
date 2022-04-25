from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


from ..models.location import Location
from ..serializers import LocationSerializer

# Views
class Locations(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = LocationSerializer
    def get(self):
        """Index request"""
        locations = Location.objects.all()
        data = LocationSerializer(locations, many=True).data
        return Response({ 'locations': data })
