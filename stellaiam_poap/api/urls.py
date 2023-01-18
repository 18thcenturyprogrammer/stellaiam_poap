from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

from api.views import create_single_direct_poap_claim_view, get_direct_poap_claim_view



# ref) https://youtu.be/xsQRMZxpg9I?t=1303
# 
# defaultrouter doc 
# ref) https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
router = DefaultRouter()
# router.register('path',views.Pathapi)
# router.register('price',views.Priceapi)


app_name = 'api'

urlpatterns = [
    path('create_single_direct_poap_claim/', create_single_direct_poap_claim_view, name ='create_single_direct_poap_claim_view'),
    path('get_direct_poap_claim/<int:directPoapClaimId>', get_direct_poap_claim_view, name ='get_direct_poap_claim_view'),

    
    
    path('', include(router.urls))
]