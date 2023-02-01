from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

from api.views import create_single_direct_poap_claim_view,create_multiple_direct_poap_claim_view ,get_poap_view,paid_direct_poap_claim_view,public_paid_direct_poap_claim_view, receive_poap_view
from api.views import create_non_direct_poap_claim_view,public_paid_non_direct_poap_claim_view
from api.views import email_test_view,get_extension_test_view


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
    path('create_multiple_direct_poap_claim/', create_multiple_direct_poap_claim_view, name ='create_multiple_direct_poap_claim_view'),
    path('create_non_direct_poap_claim/', create_non_direct_poap_claim_view, name ='create_non_direct_poap_claim_view'),
    path('receive_poap/', receive_poap_view, name ='receive_poap_view'),

    path('get_poap/<int:poapId>', get_poap_view, name ='get_poap_view'),
    path('paid_direct_poap_claim/', paid_direct_poap_claim_view, name ='paid_direct_poap_claim_view'),
    path('public_paid_non_direct_poap_claim/', public_paid_non_direct_poap_claim_view, name ='public_paid_non_direct_poap_claim'),
    path('public_paid_direct_poap_claim/', public_paid_direct_poap_claim_view, name ='public_paid_direct_poap_claim_view'),
    path('email_test/', email_test_view, name ='email_test_view'),
    path('get_extension_test/', get_extension_test_view, name ='get_extension_test_view'),

    

    

    path('', include(router.urls))
]