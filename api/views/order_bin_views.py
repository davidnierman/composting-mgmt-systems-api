from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse # this will be better in the future using react
from django.shortcuts import get_object_or_404


from ..models.order_bin import Order_Bin
from ..serializers import Order_BinSerializer

# Create your views here.
# reference doc: https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class Order_Bins(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = Order_BinSerializer
    def get(self, request):
        """Index request"""
        # Get all the bin orders:
        order_bins = Order_Bin.objects.all()
        # Run the data through the serializer
        data = Order_BinSerializer(order_bins, many=True).data
        return Response({ 'order_bins': data })

    def post(self, request):
        """Create request"""
        order_bin = Order_BinSerializer(data=request.data['order_bin'])
        if order_bin.is_valid():
            order_bin.save()
            return JsonResponse({ 'order_bin': order_bin.data }, status=status.HTTP_201_CREATED)
        return JsonResponse(order_bin.errors, status=status.HTTP_400_BAD_REQUEST)

class Order_BinDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the order_bin to show
        order_bin = get_object_or_404(Order_Bin, pk=pk)
        # Run the data through the serializer so it's formatted
        data = Order_BinSerializer(order_bin).data
        return Response({ 'order_bin': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate order_bin to delete
        print('DELETE REQUEST RUNNNING')
        order_bin = get_object_or_404(Order_Bin, pk=pk)
        # Check the order_bin's user against the user making this request
        if(request.user.is_superuser):
            order_bin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("Unauthorized, you do not have permission to delete this bin order")


    def partial_update(self, request, pk):
        """Update Request"""
        # Locate order_bin
        # get_object_or_404 returns a object representation of our Location
        order_bin = get_object_or_404(Order_Bin, pk=pk)
        # Check the order_bin's owner against the user making this request
        if request.user != order_bin.user:
            raise PermissionDenied('Unauthorized, you do not own this bin order')

        # Ensure the owner field is set to the current user's ID
        request.data['order_bin']['user'] = request.user.id
        # Validate updates with serializer
        data = Order_BinSerializer(order_bin, data=request.data['order_bin'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
