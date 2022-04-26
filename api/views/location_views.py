from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse # this will be better in the future using react
from django.shortcuts import get_object_or_404


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

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the location to show
        location = get_object_or_404(Location, pk=pk)
        # Only want to show owned locations?
        if request.user != location.user:
            raise PermissionDenied('Unauthorized, you do not own this mango')

        # Run the data through the serializer so it's formatted
        data = LocationSerializer(location).data
        return Response({ 'location': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate location to delete
        print('DELETE REQUEST RUNNNING')
        location = get_object_or_404(Location, pk=pk)
        # Check the location's user against the user making this request
        if request.user != location.user:
            raise PermissionDenied('Unauthorized, you do not own this location')
        # Only delete if the user owns the location
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate location
        # get_object_or_404 returns a object representation of our Location
        location = get_object_or_404(Location, pk=pk)
        # Check the location's owner against the user making this request
        if request.user != location.user:
            raise PermissionDenied('Unauthorized, you do not own this location')

        # Ensure the owner field is set to the current user's ID
        request.data['location']['user'] = request.user.id
        # Validate updates with serializer
        data = LocationSerializer(location, data=request.data['location'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
