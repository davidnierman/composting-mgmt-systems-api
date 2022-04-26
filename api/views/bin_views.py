from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse # this will be better in the future using react
from django.shortcuts import get_object_or_404


from ..models.bin import Bin
from ..serializers import BinSerializer

# Create your views here.
# reference doc: https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class Bins(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = BinSerializer
    def get(self, request):
        """Index request"""
        # Get all the bins:
        bins = Bin.objects.all()
        # Filter the Bin by owner, so you can only see your owned Bins
        # bin = Bin.objects.filter(owner=request.user.id)
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

class BinDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the bin to show
        bin = get_object_or_404(Bin, pk=pk)
        # Run the data through the serializer so it's formatted
        data = BinSerializer(bin).data
        return Response({ 'bin': data })

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
