import sys
import traceback
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

            # use modified email address as filename 
            tempFileName = request.data['email'].replace("@","__").replace(".","_")

            address = request.data['address']
           
            with open(f'./media/csv/temp/{tempFileName}.csv', 'w+') as fp:
                fp.write(f'address\n{address}')

            # create csv file with single address
            with open(f'./media/csv/temp/{tempFileName}.csv','rb') as f:
          
                request.data['address']=File(f)
            
                serializer = DirectPoapClaimSerializer(data= request.data)

                if serializer.is_valid():
                    logger.info("serializer is valid")
                    serializer.save()

                    # save design image into pinata ipfs
                    imgCid = pinImg(serializer.data)

                    # get claim obj and update and save
                    directPoapClaim = DirectPoapClaim.objects.get(id=serializer.data['id'])
                    directPoapClaim.imgCid = imgCid
                    directPoapClaim.save()
                    
                    updatedClaim = DirectPoapClaim.objects.get(id=serializer.data['id'])
                    
                    data['status'] ='success'
                    data['msg'] = 'created'

                    temp= {}
                    temp['id'] = updatedClaim.id
                    temp['email'] = updatedClaim.email
                    temp['title'] = updatedClaim.title
                    temp['description'] = updatedClaim.description
                    temp['image'] = updatedClaim.image.name
                    temp['howMany'] = updatedClaim.howMany
                    temp['created'] = updatedClaim.created.isoformat()
                    temp['imgCid'] = updatedClaim.imgCid

                    data['data'] = temp

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

         # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" %ex_value)
        print("Stack trace : %s" %stack_trace)
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



   



def pinImg(claim):
    
    # get secret ref) https://stackoverflow.com/a/61437799
    pinataJwtToken = config('PINATA_JWT_TOKEN')

    # access media file in view ref) https://stackoverflow.com/a/43630328
    media_root = settings.MEDIA_ROOT

    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    payload={
        'pinataOptions': '{"cidVersion": 1}',
        'pinataMetadata': '{"name": "poap_img_'+str(claim['id'])+'", "keyvalues": {"claim_id": "'+str(claim['id'])+'","email":"'+claim['email']+'","title":"'+claim['title']+'","description":"'+claim['description']+'","howMany":"'+str(claim['howMany'])+'","created":"'+claim['created']+'","imgIpfsCreated":"'+ timezone.now().isoformat()+'"}}'
        }


    files=[
        ('file',('b.png',open(media_root +claim['image'].replace("/media",""),'rb')))
    ]

   
    headers = {
        'Authorization': 'Bearer '+pinataJwtToken,
    }

    # https://dweb.link/ipfs/
    # .ipfs.w3s.link    ``

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print("response")
    print(response)
    print(dir(response))

    jsonObj = json.loads(response.text)
    return jsonObj['IpfsHash']
    
   



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