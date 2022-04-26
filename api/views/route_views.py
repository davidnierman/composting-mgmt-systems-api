from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse # this will be better in the future using react
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from ..models.route import Route
from ..serializers import RouteSerializer

# Create your views here.
# reference doc: https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class Routes(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = RouteSerializer
    def get(self, request):
        """Index request"""
        # Get all the routes:
        routes = Route.objects.all()
        data = RouteSerializer(routes, many=True).data
        return Response({ 'routes': data })

class RouteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the route to show
        route = get_object_or_404(Route, pk=pk)
        # Only want to show owned routes?
        if request.user != route.user_id:
            raise PermissionDenied('Unauthorized, you do not own this route')

        # Run the data through the serializer so it's formatted
        data = RouteSerializer(route).data
        return Response({ 'route': data })