from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse # this will be better in the future using react


from ..models.location import Location
from ..serializers import LocationSerializer

# Create your views here.
# reference doc: https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class Locations(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = LocationSerializer
    def get(self, request):
        """Index request"""
        # Get all the mangos:
        locations = Location.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        # location = Location.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = LocationSerializer(locations, many=True).data
        return Response({ 'locations': data })

    def post(self, request):
        """Create request"""
        request.data['location']['user_id'] = request.user.id
        location = LocationSerializer(data=request.data['location'])
        if location.is_valid():
            location.save()
            return JsonResponse({ 'location': location.data }, status=status.HTTP_201_CREATED)
        return JsonResponse(location.errors, status=status.HTTP_400_BAD_REQUEST)