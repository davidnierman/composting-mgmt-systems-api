from django.urls import path

from api.views.location_views import LocationDetail, Locations, LocationsSearch
from api.views.route_views import Routes, RouteDetail
from api.views.bin_views import BinDetail, Bins, BinsSearch
from api.views.order_bin_views import Order_Bins, Order_BinDetail
from .views.mango_views import Mangos, MangoDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    #### Mangos ###
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    #### Location ####
    path('locations/', Locations.as_view(), name='locations'),
    path('locations/search/', LocationsSearch.as_view(), name='locations_search'),
    path('locations/<int:pk>/', LocationDetail.as_view(), name = 'location_detail'),
    #### Bins ####
    path('bins/', Bins.as_view(), name='bins'),
    path('bins/search/', BinsSearch.as_view(), name='bin_search'),
    path('bins/<int:pk>/', BinDetail.as_view(), name='bins'),
    #### Order_Bins ####
    path('order_bins/', Order_Bins.as_view(), name='order_bins'),
    path('order_bins/<int:pk>/', Order_BinDetail.as_view(), name='order_bins_detail'),
    #### Routes ####
    path('routes/', Routes.as_view(), name='routes'),
    path('routes/<int:pk>/', RouteDetail.as_view(), name='routes'),
    #### Auth ####
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
