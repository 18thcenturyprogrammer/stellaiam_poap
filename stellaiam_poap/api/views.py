import logging
import requests
import json
import datetime

# get secret ref) https://stackoverflow.com/a/61437799
from decouple import config

from web3 import Web3

import numpy as np

logger = logging.getLogger("mylogger")

from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone

from django.core.files.base import ContentFile, File

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import DirectPoapClaim
from api.Serializers import DirectPoapClaimSerializer





@api_view(['POST',])
def create_single_direct_poap_claim_view(request):
    print("= create_single_direct_poap_claim_view =")
    
    logger.info("===== create_single_direct_poap_claim_view =====")
    # logger.info(request.data['title'])
    # logger.info(request.data['description'])
    # logger.info(request.data['email'])
    # logger.info(request.data['address'])
    # logger.info(request.data['image'])
    # logger.info(request.data['howMany'])

    logger.info(dir(request.data['image']))

    logger.info(type(request.data['image']))
  
    try:

        data={}

        if request.method == 'POST':

            if not request.data['title'] or not request.data['description'] or not request.data['email'] or not request.data['address'] or not request.data['image'] or not request.data['howMany']:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            

            # try:
            #     writeTempSingleAddressCsv(request.data['email'],request.data['address'])

                
            # except Exception as e:
            #     logger.info(e, exc_info=True)
            #     logger.info("writting temp single address csv failed")
            #     return Response(data, status=status.HTTP_400_BAD_REQUEST)

            tempFileName = request.data['email'].replace("@","__").replace(".","_")

            logger.info("tempFileName : ")
            logger.info(tempFileName)

            address = request.data['address']
           
            with open(f'./media/csv/temp/{tempFileName}.csv', 'w+') as fp:
                fp.write(f'address\n{address}')

            # Using File
            with open(f'./media/csv/temp/{tempFileName}.csv','rb') as f:
                logger.info("#########################")
                logger.info(dir(f))
                logger.info(f)
                logger.info(type(f))
                request.data['address']=File(f)
            

                serializer = DirectPoapClaimSerializer(data= request.data)

                if serializer.is_valid():
                    logger.info("serializer is valid")
                    serializer.save()
                    data['status'] ='success'
                    data['msg'] = 'created'
                    data['data'] = serializer.data

                    return Response(data, status=status.HTTP_201_CREATED)
            
                logger.info("===== serializer.errors =====")
                logger.info(serializer.errors)


                logger.info("===== serializer.validated_data =====")
                logger.info(serializer.validated_data)
                
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print("===========e =========")
        print(e)
        print(dir(e))
        return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET',])
def get_direct_poap_claim_view(request, directPoapClaimId):
    logger.info("===== get_direct_poap_claim_view =====")
    logger.info(directPoapClaimId)


    data={}
    try:
        directPoapClaim = DirectPoapClaim.objects.get(id=directPoapClaimId)
    except DirectPoapClaim.DoesNotExist:
        return Response(data,status= status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        serializer =  DirectPoapClaimSerializer(directPoapClaim)
        data['status']='success'
        data['msg'] ='found direct poap claim'
        data['data'] = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    return Response(data, status=status.HTTP_400_BAD_REQUEST)



def writeTempSingleAddressCsv(email, address):
    logger.info("writting single address csv ING.....")
    logger.info(address)

   
    # ref) https://stackoverflow.com/a/41009026
    with open(f'./frontEnd/assets/for_django/images/temp/{email}.csv', 'w+') as fp:
        fp.write(f'''\
    address,
    {address}
    ''')

    # Using File
    with open(f'./frontEnd/assets/for_django/images/temp/{email}.csv') as f:
        logger.info("#########################")
        logger.info(dir(f))
        logger.info(f)
        logger.info(type(f))
        return File(f)    

   