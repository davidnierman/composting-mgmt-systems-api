from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse # this will be better in the future using react
from django.shortcuts import get_object_or_404


from ..models.bin import Bin
from ..serializers import BinSerializer, LocationSerializer

# Create your views here.
# reference doc: https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class Bins(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = BinSerializer
    def get(self, request):
        """Index request"""
        print('THIS IS THE REQUEST: ', request.data)
        # Filter the Bin by location, so you can only see bins at a specific location
        bins = Bin.objects.filter(location_id = request.data['location']['id'])
        # Run the data through the serializer
        data = BinSerializer(bins, many=True).data
        return Response({ 'bins': data })

    def post(self, request):
        """Create request"""
        request.data['bin']['user_id'] = request.user.id
        bin = BinSerializer(data=request.data['bin'])
        if bin.is_valid():
            bin.save()
            return JsonResponse({ 'bin': bin.data }, status=status.HTTP_201_CREATED)
        return JsonResponse(bin.errors, status=status.HTTP_400_BAD_REQUEST)

# LocationSearch will search thru bins based on users search term and criteria
class BinsSearch(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = BinSerializer
    def get(self, request):
        """Search request"""
        # Get URL request Params
        # query params reference link: https://www.django-rest-framework.org/api-guide/requests/
        search_criteria = request.query_params['search_criteria']
        search_term = request.query_params['search_term']
        if(search_criteria == 'id'):
            bins = Bin.objects.filter(id = search_term)
        elif(search_criteria == 'barcode'):
            bins = Bin.objects.filter(barcode__contains = search_term)
        elif (search_criteria == 'location_id'):
            bins = Bin.objects.filter(location_id = search_term)
        else:
            # more info on exception handling can be found here: https://www.django-rest-framework.org/api-guide/exceptions/
            raise ValidationError({'search_criteria ERROR', "Please use one of the following valid search criteria 'id', 'barcode', 'location_id' "})
        # Run the data through the serializer
        data = BinSerializer(bins, many=True).data
        return Response({ 'bins': data })

class BinDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the bin to show
        bin = get_object_or_404(Bin, pk=pk)
        # Run the bin data through the serializer so it's formatted
        data = BinSerializer(bin).data
        # use select_related to populate the location_id (location_id is a foreign key for the location objet)
        # documentationc an be found here: https://docs.djangoproject.com/en/2.2/ref/models/querysets/#select-related
        bin_with_location_info = Bin.objects.select_related('location_id').get(id=pk) # id=pk => since you only want to populate the location related to the foreign key
        # import the LocationSerialer from above --> this will be used to parse the location data
        # pass the bin_with_location_info as an argument and call the foreignkey using dot notation and then call its method as_dict
        # use dot notation to call the data key to get the data within the return of the locationSerializer
        location = LocationSerializer(bin_with_location_info.location_id.as_dict()).data
        # create a new object that combines the bin data and the location data
        allData = {
                "bin": data,
                "location": location
        }
        # return the new object that has all the data
        return Response({ 'AllData': allData })

    def delete(self, request, pk):
        """Delete request"""
        # Locate bin to delete
        print('DELETE REQUEST RUNNNING')
        bin = get_object_or_404(Bin, pk=pk)
        # Only delete if the user making the request is a superuser
        if(request.user.is_superuser):
            bin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("Unauthorized, you do not have permission to delete this bin")

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate bin
        # get_object_or_404 returns a object representation of our bin
        bin = get_object_or_404(Bin, pk=pk)


        # Ensure the owner field is set to the current user's ID
        request.data['bin']['user'] = request.user.id
        # Validate updates with serializer
        data = BinSerializer(bin, data=request.data['bin'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
