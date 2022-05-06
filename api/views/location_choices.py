from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from ..models.location import Location

# this request takes the field from url and then uses it to pull its choices
class LocationChoices(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request, field):
        print('this is the request: ', request)
        choices = Location._meta.get_field(field).choices 
        return Response(choices)
