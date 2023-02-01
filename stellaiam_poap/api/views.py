import os
import sys
import traceback
import logging
import requests
import json
import datetime
import time

import smtplib, ssl
from email.message import EmailMessage
from string import Template
import qrcode
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# get secret ref) https://stackoverflow.com/a/61437799
from decouple import config

from web3 import Web3

import numpy as np
import pandas as pd

logger = logging.getLogger("mylogger")

from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone

from django.core.files.base import ContentFile, File

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import PoapClaim, PoapReceipt
from api.Serializers import PoapClaimSerializer





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
            
                serializer = PoapClaimSerializer(data= request.data)

                if serializer.is_valid():
                    logger.info("serializer is valid")
                    serializer.save()

                    # save design image into pinata ipfs
                    imgCid = pinImg(serializer.data)

                    # get claim obj and update and save
                    poapClaim = PoapClaim.objects.get(id=serializer.data['id'])
                    poapClaim.imgCid = imgCid
                    poapClaim.save()
                    
                    updatedClaim = PoapClaim.objects.get(id=serializer.data['id'])
                    
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



@api_view(['POST',])
def create_multiple_direct_poap_claim_view(request):
    print("= create_multiple_direct_poap_claim_view =")
    
    logger.info("===== create_multiple_direct_poap_claim_view =====")
    logger.info(request.data['title'])
    logger.info(request.data['description'])
    logger.info(request.data['email'])
    logger.info(request.data['address'])
    logger.info("=============address dir===============")
    logger.info(dir(request.data['address']))
    logger.info(request.data['address'].name)
    logger.info(request.data['image'])
    logger.info(request.data['howMany'])

    logger.info(dir(request.data['image']))

    logger.info(type(request.data['image']))
  
    try:

        data={}

        if request.method == 'POST':

            if not request.data['title'] or not request.data['description'] or not request.data['email'] or not request.data['address'] or not request.data['image'] or not request.data['howMany']:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            # request.data._mutable = True

            extension = getFileExtension(request.data['address'].name)

            logger.info(extension)

            if extension != '.csv' and extension != '.xlsx':
                # only csv, xlsx acceptable
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            # use modified email address as filename 
            tempFileName = request.data['email'].replace("@","__").replace(".","_")

            request.data['address'].name = tempFileName+extension
           
            serializer = PoapClaimSerializer(data= request.data)

            if serializer.is_valid():
                logger.info("serializer is valid")
                serializer.save()
                
                # save design image into pinata ipfs
                imgCid = pinImg(serializer.data)

                # get claim obj and update and save
                poapClaim = PoapClaim.objects.get(id=serializer.data['id'])
                poapClaim.imgCid = imgCid
                poapClaim.save()
                    
                updatedClaim = PoapClaim.objects.get(id=serializer.data['id'])
                
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




@api_view(['POST',])
def create_non_direct_poap_claim_view(request):
    print("= create_non_direct_poap_claim_view =")
    
    logger.info("===== create_non_direct_poap_claim_view =====")
    logger.info(request.data['title'])
    logger.info(request.data['description'])
    logger.info(request.data['email'])
    logger.info(request.data['image'])
    logger.info(request.data['howMany'])
    logger.info(request.data['secret'])

    logger.info(dir(request.data['image']))

    logger.info(type(request.data['image']))
  
    try:

        data={}

        if request.method == 'POST':

            if not request.data['title'] or not request.data['description'] or not request.data['email'] or not request.data['image'] or not request.data['howMany'] or not request.data['secret']:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            serializer = PoapClaimSerializer(data= request.data)

            if serializer.is_valid():
                logger.info("serializer is valid")
                serializer.save()

                # save design image into pinata ipfs
                imgCid = pinImg(serializer.data)

                # get claim obj and update and save
                poapClaim = PoapClaim.objects.get(id=serializer.data['id'])
                poapClaim.imgCid = imgCid
                poapClaim.save()
                
                updatedClaim = PoapClaim.objects.get(id=serializer.data['id'])
                
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
def get_poap_view(request, poapId):
    try:  
        logger.info("===== get_direct_poap_claim_view =====")
        logger.info(poapId)


        data={}
        try:
            poap = PoapClaim.objects.get(id=poapId)
        except PoapClaim.DoesNotExist:
            return Response(data,status= status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            
            serializer =  PoapClaimSerializer(poap)
            data['status']='success'
            data['msg'] ='found poap'
            data['data'] = serializer.data

            logger.info("--------------")
            logger.info(data)
            logger.info(dir(data))

            return Response(data, status=status.HTTP_200_OK)
            

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST',])
def receive_poap_view(request):
    print("= receive_poap_view =")
    
    logger.info("===== receive_poap_view =====")
    logger.info(request.data['poapId'])
    logger.info(request.data['secret'])
    logger.info(request.data['address'])
  
    try:

        data={}

        if request.method == 'POST':

            if not request.data['poapId'] or not request.data['secret'] or not request.data['address']:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)


            try:
                poap = PoapClaim.objects.get(id=request.data['poapId'])
            except PoapClaim.DoesNotExist:
                return Response(data,status= status.HTTP_404_NOT_FOUND)
            
            poapReciptQuerySet = PoapReceipt.objects.filter(claim = poap, address= request.data['address'])          

            if(not Web3.isAddress(request.data['address'])):
                data['status']='failed'
                data['msg']="올바르지 않은 주소입니다"

                return Response(data, status=status.HTTP_200_OK)   

            if(request.data['secret'] != poap.secret):
                data['status']='failed'
                data['msg']="잘못된 인증 코드입니다"

                return Response(data, status=status.HTTP_200_OK)

            if(len(poapReciptQuerySet) == 1):
                data['status']='failed'
                data['msg']="이미 POAP을 받으셨습니다"

                return Response(data, status=status.HTTP_200_OK)
            
            if(len(poapReciptQuerySet) > 1):
                data['status']='failed'
                data['msg']="문제가 발생했습니다"

                return Response(data, status=status.HTTP_200_OK)

            address = request.data['address']

            receipt = sendPoap(address, poap)

            # receipt.transactionHash is HexBytes like below
            # b"\x07\xb8x\x11\xb1'\x0c\xcb\x17\xe8\xfe,=\n\x94\xf5\x1e\xdfs\xb1\xd0\x99\xa1Ht\x89\xd9\xc2G\xb7y\xad"
            # receipt.transactionHash.hex() => '07b87811b1270ccb17e8fe2c3d0a94f51edf73b1d099a1487489d9c247b779ad'
            directPoapReceipt = PoapReceipt(claim = poap, address= address, txHash='0x'+receipt.transactionHash.hex(), blockNumber = receipt.blockNumber)
            directPoapReceipt.save()

            data['status']='success'
            data['msg']="지갑으로 POAP을 보내드렸습니다"

            return Response(data, status=status.HTTP_200_OK)
            

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





#################################################################################################################### 
# paid claim poap

@api_view(['POST',])
def public_paid_direct_poap_claim_view(request):
    logger.info("===== public_paid_direct_poap_claim_view =====")


    logger.info(request.method)
    logger.info(request.data)

    # logger.info(request.data.values())

    # logger.info(request.POST['claimId'])
    # logger.info(request.data['claimId'])
    # logger.info(request.data['whoPaid'])
    # logger.info(request.data['howMany'])
    logger.info(request.data['paidTxHash'])
  
    try:

        data={}

        if request.method != 'POST':
             return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if not request.data['paidTxHash']:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        alchemy_url = config('ALCHEMY_MUMBAI_HTTP_URL')
        contract_address = config('MUMBAI_STELLAIAM_POAP_CONTRACT_ADDRESS')
        abi = config('ABI')

        w3 = Web3(Web3.HTTPProvider(alchemy_url))

        # get contract  
        stellaiam_poap_contract = w3.eth.contract(address=contract_address, abi=abi)

        # get transaction receipt
        txReceipt = w3.eth.get_transaction_receipt(request.data['paidTxHash'])
        
        # get event log
        # web3 py event log parse ref) https://ethereum.stackexchange.com/a/59288
        log = stellaiam_poap_contract.events.paidPoapClaim().processReceipt(txReceipt)

    
        # logger.info(log[0].args.whoPaid)
        # logger.info(log[0].args.whoPaid)
        # logger.info(log[0].args.claimId)
        # logger.info(log[0].args.howMany)

        whoPaid = log[0].args.whoPaid
        claimId = log[0].args.claimId
        howMany = log[0].args.howMany
        
    
        try:
            poapClaim = PoapClaim.objects.get(id=claimId, howMany = howMany)
        except PoapClaim.DoesNotExist:
            return Response(data,status= status.HTTP_404_NOT_FOUND)

        # save metadata in pinata 
        metaCid = pinMetadata(poapClaim)

        uriReceipt = setUriPoap(poapClaim, metaCid)

        # update poapClaim as paid
        poapClaim.paidTxHash = request.data['paidTxHash']
        
        # uriReceipt.transactionHash is HexBytes like below
        # b"\x07\xb8x\x11\xb1'\x0c\xcb\x17\xe8\xfe,=\n\x94\xf5\x1e\xdfs\xb1\xd0\x99\xa1Ht\x89\xd9\xc2G\xb7y\xad"
        # uriReceipt.transactionHash.hex() => '07b87811b1270ccb17e8fe2c3d0a94f51edf73b1d099a1487489d9c247b779ad'
        poapClaim.uriTxHash = '0x'+uriReceipt.transactionHash.hex()
        poapClaim.whoPaid = whoPaid
        poapClaim.isPaid = True
        poapClaim.metaCid = metaCid

        poapClaim.save()

        fileExtension = getFileExtension(poapClaim.address.name)

        if(fileExtension == '.csv'):
          addressDf = pd.read_csv(poapClaim.address, sep=',')
        else:
          addressDf = pd.read_excel(poapClaim.address,engine='openpyxl')

        logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        logger.info(addressDf)
        logger.info(dir(addressDf))
        logger.info(addressDf['address'])
        addressList = addressDf['address'].tolist()
        # logger.info("addressList : ")
        # logger.info(addressList)

        sentCounter = 0 
        for address in addressList:
            if(Web3.isAddress(address)):
              receipt = sendPoap(address, poapClaim)

              # receipt.transactionHash is HexBytes like below
              # b"\x07\xb8x\x11\xb1'\x0c\xcb\x17\xe8\xfe,=\n\x94\xf5\x1e\xdfs\xb1\xd0\x99\xa1Ht\x89\xd9\xc2G\xb7y\xad"
              # receipt.transactionHash.hex() => '07b87811b1270ccb17e8fe2c3d0a94f51edf73b1d099a1487489d9c247b779ad'
              directPoapReceipt = PoapReceipt(claim = poapClaim, address= address, txHash='0x'+receipt.transactionHash.hex(), blockNumber = receipt.blockNumber)
              directPoapReceipt.save()
          
              sentCounter += 1

              if sentCounter == howMany:
                  break

        sendEmail(poapClaim,sentCounter)


        return Response(data, status=status.HTTP_200_OK) 
       
    
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






@api_view(['POST',])
def public_paid_non_direct_poap_claim_view(request):
    logger.info("===== public_paid_non_direct_poap_claim_view =====")


    logger.info(request.method)
    logger.info(request.data)

    # logger.info(request.data.values())

    # logger.info(request.POST['claimId'])
    # logger.info(request.data['claimId'])
    # logger.info(request.data['whoPaid'])
    # logger.info(request.data['howMany'])
    logger.info(request.data['paidTxHash'])
  
    try:

        data={}

        if request.method != 'POST':
             return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if not request.data['paidTxHash']:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        alchemy_url = config('ALCHEMY_MUMBAI_HTTP_URL')
        contract_address = config('MUMBAI_STELLAIAM_POAP_CONTRACT_ADDRESS')
        abi = config('ABI')

        w3 = Web3(Web3.HTTPProvider(alchemy_url))

        # get contract  
        stellaiam_poap_contract = w3.eth.contract(address=contract_address, abi=abi)

        # get transaction receipt
        txReceipt = w3.eth.get_transaction_receipt(request.data['paidTxHash'])
        
        # get event log
        # web3 py event log parse ref) https://ethereum.stackexchange.com/a/59288
        log = stellaiam_poap_contract.events.paidPoapClaim().processReceipt(txReceipt)

    
        # logger.info(log[0].args.whoPaid)
        # logger.info(log[0].args.whoPaid)
        # logger.info(log[0].args.claimId)
        # logger.info(log[0].args.howMany)

        whoPaid = log[0].args.whoPaid
        claimId = log[0].args.claimId
        howMany = log[0].args.howMany
        
    
        try:
            poapClaim = PoapClaim.objects.get(id=claimId, howMany = howMany)
        except PoapClaim.DoesNotExist:
            return Response(data,status= status.HTTP_404_NOT_FOUND)

        # save metadata in pinata 
        metaCid = pinMetadata(poapClaim)

        uriReceipt = setUriPoap(poapClaim, metaCid)

        # update poapClaim as paid
        poapClaim.paidTxHash = request.data['paidTxHash']
        
        # uriReceipt.transactionHash is HexBytes like below
        # b"\x07\xb8x\x11\xb1'\x0c\xcb\x17\xe8\xfe,=\n\x94\xf5\x1e\xdfs\xb1\xd0\x99\xa1Ht\x89\xd9\xc2G\xb7y\xad"
        # uriReceipt.transactionHash.hex() => '07b87811b1270ccb17e8fe2c3d0a94f51edf73b1d099a1487489d9c247b779ad'
        poapClaim.uriTxHash = '0x'+uriReceipt.transactionHash.hex()
        poapClaim.whoPaid = whoPaid
        poapClaim.isPaid = True
        poapClaim.metaCid = metaCid

        poapClaim.save()


        # get link for spreading poap

        # create qr code


        sendEmail_non_direct(poapClaim)


        return Response(data, status=status.HTTP_200_OK) 
       
    
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















@api_view(['POST',])
def paid_direct_poap_claim_view(request):
    logger.info("===== paid_direct_poap_claim_view =====")

    password = config('PASSWORD')
    logger.info(password)

    logger.info(request.method)
    logger.info(request.data)

    # logger.info(request.data.values())

    # logger.info(request.POST['claimId'])
    # logger.info(request.data['claimId'])
    # logger.info(request.data['whoPaid'])
    # logger.info(request.data['password'])
    # logger.info(request.data['howMany'])
  
    try:

        data={}

        if request.method != 'POST':
             return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if request.data['password'] != password:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if not request.data['whoPaid'] or not request.data['claimId'] or not request.data['howMany']:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            poapClaim = PoapClaim.objects.get(id=request.data['claimId'], howMany = request.data['howMany'])
        except PoapClaim.DoesNotExist:
            return Response(data,status= status.HTTP_404_NOT_FOUND)

        if(poapClaim.isPaid):
            serializer =  PoapClaimSerializer(poapClaim)
            data['status']='success'
            data['msg'] ='paid already before'
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        

        addressDf = pd.read_csv(poapClaim.address, sep=',')

        addressList = addressDf['address'].tolist()

        sendPoap(addressList, poapClaim)


        logger.info("addressList : ")
        logger.info(addressList)

        serializer =  PoapClaimSerializer(poapClaim)
        data['status']='success'
        data['msg'] ='paid now'
        data['data'] = serializer.data
        return Response(data, status=status.HTTP_200_OK)


    
        # with open(f'./media/csv/temp/{tempFileName}.csv', 'w+') as fp:
        #     fp.write(f'address\n{address}')

        


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

#########################################################################################################################
# test
@api_view(['GET',])
def email_test_view(request):
    data={}
    sendEmail('dumpittrash@gmail.com')
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET',])
def get_extension_test_view(request):
    data={}

    poapClaim = PoapClaim.objects.get(id=146)

    logger.info(dir(poapClaim.address))
    logger.info(poapClaim.address.name)

    getFileExtension(poapClaim.address.name)
    
    return Response(data, status=status.HTTP_200_OK)







#########################################################################################################################
# utility 

def sendPoap(address, poapClaim):
    
    # get secret ref) https://stackoverflow.com/a/61437799
    wallet_address = config('WALLET_ADDRESS')
    pri_key = config('WALLET_PRI_KEY')
    alchemy_url = config('ALCHEMY_MUMBAI_HTTP_URL')
    mumbai_contract_address = config('MUMBAI_STELLAIAM_POAP_CONTRACT_ADDRESS')

    # alchemy_url = "https://polygon-mumbai.g.alchemy.com/v2/Uud_P7gk4UKBPIgcNN2nV3jsEbhn1R5Z"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))

    #get the nonce.  Prevents one from sending the transaction twice
    nonce = w3.eth.getTransactionCount(wallet_address)

    #build a transaction in a dictionary
    # old stable value is 2000000, 50
    options = {
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }

    abi = config('ABI')
    contract_instance = w3.eth.contract(address=mumbai_contract_address, abi=abi)

    tx = contract_instance.functions.mintByOwner(address, poapClaim.id, 1).buildTransaction(options)

    signed_tx = w3.eth.account.signTransaction(tx, private_key=pri_key)
    
    # ref) https://web3py.readthedocs.io/en/v5/web3.eth.html?highlight=sendRawTransaction#web3.eth.Eth.send_raw_transaction
    tx_address = w3.eth.send_raw_transaction(signed_tx.rawTransaction) 

    # ref) https://web3py.readthedocs.io/en/v5/web3.eth.html?highlight=receipt#web3.eth.Eth.wait_for_transaction_receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_address)

    logger.info("wait_for_transaction_receipt=> receipt : ")
    logger.info(receipt)

    return receipt   


def setUriPoap(poapClaim,metaCid):
    
    # get secret ref) https://stackoverflow.com/a/61437799
    wallet_address = config('WALLET_ADDRESS')
    pri_key = config('WALLET_PRI_KEY')
    alchemy_url = config('ALCHEMY_MUMBAI_HTTP_URL')
    mumbai_contract_address = config('MUMBAI_STELLAIAM_POAP_CONTRACT_ADDRESS')

    # alchemy_url = "https://polygon-mumbai.g.alchemy.com/v2/Uud_P7gk4UKBPIgcNN2nV3jsEbhn1R5Z"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))

    #get the nonce.  Prevents one from sending the transaction twice
    nonce = w3.eth.getTransactionCount(wallet_address)

    #build a transaction in a dictionary
    # old stable value is 2000000, 50
    options = {
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }

    abi = config('ABI')
    contract_instance = w3.eth.contract(address=mumbai_contract_address, abi=abi)

    tx = contract_instance.functions.setOneUri(poapClaim.id, "https://gateway.pinata.cloud/ipfs/"+metaCid).buildTransaction(options)

    signed_tx = w3.eth.account.signTransaction(tx, private_key=pri_key)
    
    # ref) https://web3py.readthedocs.io/en/v5/web3.eth.html?highlight=sendRawTransaction#web3.eth.Eth.send_raw_transaction
    tx_address = w3.eth.send_raw_transaction(signed_tx.rawTransaction) 

    # ref) https://web3py.readthedocs.io/en/v5/web3.eth.html?highlight=receipt#web3.eth.Eth.wait_for_transaction_receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_address)

    logger.info("wait_for_transaction_receipt=> receipt : ")
    logger.info(receipt)

    return receipt 
        



def pinImg(claim):
    
    # get secret ref) https://stackoverflow.com/a/61437799
    pinataJwtToken = config('PINATA_JWT_TOKEN')

    # access media file in view ref) https://stackoverflow.com/a/43630328
    media_root = settings.MEDIA_ROOT

    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    pinataMetadata = {}

    pinataMetadata['name'] = "poap_img_"+str(claim['id'])

    keyvalues = {}
    keyvalues['claim_id'] = claim['id']
    keyvalues['email'] = claim['email']
    keyvalues['title'] = claim['title']
    keyvalues['description'] = claim['description']
    keyvalues['howMany'] = claim['howMany']
    keyvalues['created'] = claim['created']
    keyvalues['created'] = claim['created']
    keyvalues['imgIpfsCreated'] = timezone.now().isoformat()

    pinataMetadata['keyvalues'] = keyvalues
    

    payload={
        'pinataOptions': '{"cidVersion": 1}',
        'pinataMetadata': json.dumps(pinataMetadata)
        }

    print("payload")
    print(payload)
    


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
    print("=====================")
    print(response.json)
    print("=====================")
    print("response.text")
    print(response.text)
    print("=====================")
    print("response.raw")
    print(response.raw)
    print("=====================")
    print("response.status_code")
    print(response.status_code)
    print("=====================")
    print("response.request")
    print(response.request)
    print("=====================")
    print("response.url")
    print(response.url)
    
    # print(dir(response))

    jsonObj = json.loads(response.text)

    print("jsonObj")
    print(jsonObj)
    print(dir(jsonObj))


    return jsonObj['IpfsHash']
    

def pinMetadata(poapClaim):
    # get secret ref) https://stackoverflow.com/a/61437799
    pinataJwtToken = config('PINATA_JWT_TOKEN')

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    payload = json.dumps({
    "pinataOptions": {
        "cidVersion": 1
    },
    "pinataMetadata": {
        "name":  poapClaim.title,
        "keyvalues": {
        "description":poapClaim.description,
        "publisher": "Stellaiam",
        }
    },
    "pinataContent": {
        "image": "https://gateway.pinata.cloud/ipfs/"+poapClaim.imgCid,
        "name": poapClaim.title,
        "description": poapClaim.description
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+pinataJwtToken
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    jsonObj = json.loads(response.text)


    print("jsonObj")
    print(jsonObj)
    print(dir(jsonObj))

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



# smtp google email send
# ref) https://leimao.github.io/blog/Python-Send-Gmail/
def sendEmail(poapClaim,sentCounter):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    email_address = config('EMAIL_ADDRESS')
    email_password = config('EMAIL_APP_PASSWORD')

    # logo_img = config('WEBSITE')+'static/for_django/images/logo-color.png'
    logo_img = 'http://jacob-yo.net/wp-content/uploads/2023/01/stellaiam-low-resolution-color-logo.png'
    facebook_logo = 'http://jacob-yo.net/wp-content/uploads/2023/01/facebook.png'
    twitter_logo = 'http://jacob-yo.net/wp-content/uploads/2023/01/twitter.png'
    instagram_logo ='http://jacob-yo.net/wp-content/uploads/2023/01/instagram.png' 
    poap_img = config('WEBSITE')+"media/"+poapClaim.image.name   
    howMany = sentCounter
    paidTxHash = poapClaim.paidTxHash
    whoPaid = poapClaim.whoPaid
    opensea_link = config('OPENSEA_URL')+config('MUMBAI_STELLAIAM_POAP_CONTRACT_ADDRESS')+"/"+str(poapClaim.id)
    star_img = 'http://jacob-yo.net/wp-content/uploads/2023/01/star.png'


    msg = EmailMessage()


   
    
    template= Template('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<!--[if gte mso 9]>
<xml>
  <o:OfficeDocumentSettings>
    <o:AllowPNG/>
    <o:PixelsPerInch>96</o:PixelsPerInch>
  </o:OfficeDocumentSettings>
</xml>
<![endif]-->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
  <title></title>
  
    <style type="text/css">
      @media only screen and (min-width: 620px) {
  .u-row {
    width: 600px !important;
  }
  .u-row .u-col {
    vertical-align: top;
  }

  .u-row .u-col-100 {
    width: 600px !important;
  }

}

@media (max-width: 620px) {
  .u-row-container {
    max-width: 100% !important;
    padding-left: 0px !important;
    padding-right: 0px !important;
  }
  .u-row .u-col {
    min-width: 320px !important;
    max-width: 100% !important;
    display: block !important;
  }
  .u-row {
    width: 100% !important;
  }
  .u-col {
    width: 100% !important;
  }
  .u-col > div {
    margin: 0 auto;
  }
}
body {
  margin: 0;
  padding: 0;
}

table,
tr,
td {
  vertical-align: top;
  border-collapse: collapse;
}

p {
  margin: 0;
}

.ie-container table,
.mso-container table {
  table-layout: fixed;
}

* {
  line-height: inherit;
}

a[x-apple-data-detectors='true'] {
  color: inherit !important;
  text-decoration: none !important;
}

@media (max-width: 480px) {
  .hide-mobile {
    max-height: 0px;
    overflow: hidden;
    display: none !important;
  }
}

table, td { color: #000000; } #u_body a { color: #0000ee; text-decoration: underline; } @media (max-width: 480px) { #u_content_image_3 .v-container-padding-padding { padding: 10px !important; } #u_content_image_3 .v-src-width { width: auto !important; } #u_content_image_3 .v-src-max-width { max-width: 31% !important; } #u_content_image_1 .v-src-width { width: auto !important; } #u_content_image_1 .v-src-max-width { max-width: 100% !important; } #u_content_heading_1 .v-container-padding-padding { padding: 30px 10px 10px !important; } #u_content_button_1 .v-size-width { width: 65% !important; } #u_content_text_2 .v-container-padding-padding { padding: 10px !important; } #u_content_image_2 .v-src-width { width: auto !important; } #u_content_image_2 .v-src-max-width { max-width: 10% !important; } #u_content_heading_2 .v-container-padding-padding { padding: 10px 10px 30px !important; } #u_content_text_3 .v-container-padding-padding { padding: 30px 10px 10px !important; } #u_content_menu_1 .v-padding { padding: 5px 10px !important; } #u_content_text_4 .v-container-padding-padding { padding: 10px 10px 30px !important; } }
    </style>
  
  

<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css2?family=Arvo&display=swap" rel="stylesheet" type="text/css"><!--<![endif]-->

</head>

<body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">
  <!--[if IE]><div class="ie-container"><![endif]-->
  <!--[if mso]><div class="mso-container"><![endif]-->
  <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0">
  <tbody>
  <tr style="vertical-align: top">
    <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #e7e7e7;"><![endif]-->
    

<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
  
<table id="u_content_image_3" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:'Raleway',sans-serif;" align="left">
        
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding-right: 0px;padding-left: 0px;" align="center">
      
      <img align="center" border="0" src="$logo_img" alt="image" title="image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 16%;max-width: 92.8px;" width="92.8" class="v-src-width v-src-max-width"/>
      
    </td>
  </tr>
</table>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>



<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="background-color: #ffffff;height: 100%;width: 100% !important;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->
  
<table id="u_content_image_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 0px 0px;font-family:'Raleway',sans-serif;" align="left">
        
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding-right: 0px;padding-left: 0px;" align="center">
      
      <img align="center" border="0" src="$poap_img" alt="image" title="image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 80%;max-width: 480px;" width="480" class="v-src-width v-src-max-width"/>
      
    </td>
  </tr>
</table>

      </td>
    </tr>
  </tbody>
</table>

<table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;" align="left">
        
  <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 3px solid #575757;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
    <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
          <span>&#160;</span>
        </td>
      </tr>
    </tbody>
  </table>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>



<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="background-color: #f6f6f6;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="background-color: #f6f6f6;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
  
<table id="u_content_heading_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 10px 10px;font-family:'Raleway',sans-serif;" align="left">
        
  <h1 style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: Arvo; font-size: 24px;"><strong>POAP를 성공적으로 보냈습니다</strong></h1>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_button_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;" align="left">
        
  <!--[if mso]><style>.v-button {background: transparent !important;}</style><![endif]-->
<div align="center">
  <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://www.unlayer.com" style="height:37px; v-text-anchor:middle; width:203px;" arcsize="67.5%"  stroke="f" fillcolor="#ffce00"><w:anchorlock/><center style="color:#000000;font-family:'Raleway',sans-serif;"><![endif]-->  
    <a href="$opensea_link" target="_blank" class="v-button v-size-width" style="box-sizing: border-box;display: inline-block;font-family:'Raleway',sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #000000; background-color: #ffce00; border-radius: 25px;-webkit-border-radius: 25px; -moz-border-radius: 25px; width:35%; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;">
      <span class="v-padding" style="display:block;padding:10px 20px;line-height:120%;"><strong><span style="font-size: 14px; line-height: 16.8px;">Opensea에서 확인하기</span></strong></span>
    </a>
  <!--[if mso]></center></v:roundrect><![endif]-->
</div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_text_2" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 50px;font-family:'Raleway',sans-serif;" align="left">
        
  <div style="line-height: 160%; text-align: center; word-wrap: break-word;">
    <p style="line-height: 160%; font-size: 14px;">$howMany 명에게 성공적으로 POAP을 보냈습니다.</p>
    <p style="line-height: 160%; font-size: 14px;">비용을 지불한 지갑주소는</p>
    <p style="line-height: 160%; font-size: 14px;">$whoPaid 입니다.</p>
    <p style="line-height: 160%; font-size: 14px;">비용지불 Smart contract 주소는</p>
    <p style="line-height: 160%; font-size: 14px;">$paidTxHash 입니다</p>
  </div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_image_2" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;" align="left">
        
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding-right: 0px;padding-left: 0px;" align="center">
      
      <img align="center" border="0" src="$star_img" alt="image" title="image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 7%;max-width: 42px;" width="42" class="v-src-width v-src-max-width"/>
      
    </td>
  </tr>
</table>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_heading_2" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 40px;font-family:'Raleway',sans-serif;" align="left">
        
  <h1 style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: Arvo; font-size: 20px;"><strong>Stellaiam</strong></h1>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>



<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
  
<table id="u_content_text_3" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 80px 10px;font-family:'Raleway',sans-serif;" align="left">
        
  <div style="line-height: 160%; text-align: center; word-wrap: break-word;">
    <p style="font-size: 14px; line-height: 160%;">문의 사항은 <a rel="noopener" href="mailto:18thcenturyprogrammer@gmail.com" target="_blank">18thcenturyprogrammer@gmail.com</a> 로 보내주시거나 http://127.0.0.1:8000 에서 확인하세요.</p>
  </div>

      </td>
    </tr>
  </tbody>
</table>

<table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 0px;font-family:'Raleway',sans-serif;" align="left">
        
  <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #BBBBBB;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
    <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
          <span>&#160;</span>
        </td>
      </tr>
    </tbody>
  </table>

      </td>
    </tr>
  </tbody>
</table>

<table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;" align="left">
        
<div align="center">
  <div style="display: table; max-width:187px;">
  <!--[if (mso)|(IE)]><table width="187" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-collapse:collapse;" align="center"><table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse; mso-table-lspace: 0pt;mso-table-rspace: 0pt; width:187px;"><tr><![endif]-->
  
    
    <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
    <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 15px">
      <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <a href="" title="Facebook" target="_blank">
          <img src="$facebook_logo" alt="Facebook" title="Facebook" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
        </a>
      </td></tr>
    </tbody></table>
    <!--[if (mso)|(IE)]></td><![endif]-->
    
    <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
    <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 15px">
      <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <a href="" title="Twitter" target="_blank">
          <img src="$twitter_logo" alt="Twitter" title="Twitter" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
        </a>
      </td></tr>
    </tbody></table>
    <!--[if (mso)|(IE)]></td><![endif]-->
    
    <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 0px;" valign="top"><![endif]-->
    <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 0px">
      <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <a href="" title="Instagram" target="_blank">
          <img src="$instagram_logo" alt="Instagram" title="Instagram" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
        </a>
      </td></tr>
    </tbody></table>
    <!--[if (mso)|(IE)]></td><![endif]-->
    
    
    <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
  </div>
</div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_menu_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;" align="left">
        
<div class="menu" style="text-align:center">
<!--[if (mso)|(IE)]><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center"><tr><![endif]-->

  <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
  
    <a href="http://127.0.0.1:8000" target="_self" style="padding:5px 15px;display:inline-block;color:#000000;font-size:14px;text-decoration:none"  class="v-padding">
      Home
    </a>
  
  <!--[if (mso)|(IE)]></td><![endif]-->
  
    <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
    <span style="padding:5px 15px;display:inline-block;color:#000000;font-size:14px" class="v-padding hide-mobile">
      |
    </span>
    <!--[if (mso)|(IE)]></td><![endif]-->
  

  <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
  
    <a href="https://www.unlayer.com" target="_self" style="padding:5px 15px;display:inline-block;color:#000000;font-size:14px;text-decoration:none"  class="v-padding">
      About Us
    </a>
  
  <!--[if (mso)|(IE)]></td><![endif]-->
  

<!--[if (mso)|(IE)]></tr></table><![endif]-->
</div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_text_4" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 40px;font-family:'Raleway',sans-serif;" align="left">
        
  <div style="line-height: 160%; text-align: center; word-wrap: break-word;">
    <p style="font-size: 14px; line-height: 160%;"> </p>
<p style="font-size: 14px; line-height: 160%;">Stellaiam All rights reserved</p>



  </div>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>


    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
    </td>
  </tr>
  </tbody>
  </table>
  <!--[if mso]></div><![endif]-->
  <!--[if IE]></div><![endif]-->
</body>

</html>''')
    

    content = template.substitute(
      logo_img= logo_img, 
      facebook_logo= facebook_logo, 
      twitter_logo= twitter_logo, 
      instagram_logo=instagram_logo,
      poap_img=poap_img,
      howMany=howMany,
      paidTxHash=paidTxHash,
      whoPaid=whoPaid,
      opensea_link=opensea_link,
      star_img=star_img
      )

    logger.info(content)
    
    msg.set_content(content, subtype='html')
    msg['Subject'] = "{howMany}개의 POAP이 전송되었습니다 - stellaiam".format(howMany=howMany)
    msg['From'] = email_address
    msg['To'] = poapClaim.email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg, from_addr=email_address, to_addrs=poapClaim.email)


def sendEmail_non_direct(poapClaim):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    email_address = config('EMAIL_ADDRESS')
    email_password = config('EMAIL_APP_PASSWORD')

    # logo_img = config('WEBSITE')+'static/for_django/images/logo-color.png'
    logo_img = 'http://jacob-yo.net/wp-content/uploads/2023/01/stellaiam-low-resolution-color-logo.png'
    facebook_logo = 'http://jacob-yo.net/wp-content/uploads/2023/01/facebook.png'
    twitter_logo = 'http://jacob-yo.net/wp-content/uploads/2023/01/twitter.png'
    instagram_logo ='http://jacob-yo.net/wp-content/uploads/2023/01/instagram.png' 
    poap_img = config('WEBSITE')+"media/"+poapClaim.image.name  
    howMany = poapClaim.howMany
    paidTxHash = poapClaim.paidTxHash
    whoPaid = poapClaim.whoPaid
    opensea_link = config('OPENSEA_URL')+config('MUMBAI_STELLAIAM_POAP_CONTRACT_ADDRESS')+"/"+str(poapClaim.id)
    star_img = 'http://jacob-yo.net/wp-content/uploads/2023/01/star.png'


    msg = EmailMessage()


   
    
    template= Template('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<!--[if gte mso 9]>
<xml>
  <o:OfficeDocumentSettings>
    <o:AllowPNG/>
    <o:PixelsPerInch>96</o:PixelsPerInch>
  </o:OfficeDocumentSettings>
</xml>
<![endif]-->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
  <title></title>
  
    <style type="text/css">
      @media only screen and (min-width: 620px) {
  .u-row {
    width: 600px !important;
  }
  .u-row .u-col {
    vertical-align: top;
  }

  .u-row .u-col-100 {
    width: 600px !important;
  }

}

@media (max-width: 620px) {
  .u-row-container {
    max-width: 100% !important;
    padding-left: 0px !important;
    padding-right: 0px !important;
  }
  .u-row .u-col {
    min-width: 320px !important;
    max-width: 100% !important;
    display: block !important;
  }
  .u-row {
    width: 100% !important;
  }
  .u-col {
    width: 100% !important;
  }
  .u-col > div {
    margin: 0 auto;
  }
}
body {
  margin: 0;
  padding: 0;
}

table,
tr,
td {
  vertical-align: top;
  border-collapse: collapse;
}

p {
  margin: 0;
}

.ie-container table,
.mso-container table {
  table-layout: fixed;
}

* {
  line-height: inherit;
}

a[x-apple-data-detectors='true'] {
  color: inherit !important;
  text-decoration: none !important;
}

@media (max-width: 480px) {
  .hide-mobile {
    max-height: 0px;
    overflow: hidden;
    display: none !important;
  }
}

table, td { color: #000000; } #u_body a { color: #0000ee; text-decoration: underline; } @media (max-width: 480px) { #u_content_image_3 .v-container-padding-padding { padding: 10px !important; } #u_content_image_3 .v-src-width { width: auto !important; } #u_content_image_3 .v-src-max-width { max-width: 31% !important; } #u_content_image_1 .v-src-width { width: auto !important; } #u_content_image_1 .v-src-max-width { max-width: 100% !important; } #u_content_heading_1 .v-container-padding-padding { padding: 30px 10px 10px !important; } #u_content_button_1 .v-size-width { width: 65% !important; } #u_content_text_2 .v-container-padding-padding { padding: 10px !important; } #u_content_image_2 .v-src-width { width: auto !important; } #u_content_image_2 .v-src-max-width { max-width: 10% !important; } #u_content_heading_2 .v-container-padding-padding { padding: 10px 10px 30px !important; } #u_content_text_3 .v-container-padding-padding { padding: 30px 10px 10px !important; } #u_content_menu_1 .v-padding { padding: 5px 10px !important; } #u_content_text_4 .v-container-padding-padding { padding: 10px 10px 30px !important; } }
    </style>
  
  

<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css2?family=Arvo&display=swap" rel="stylesheet" type="text/css"><!--<![endif]-->

</head>

<body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">
  <!--[if IE]><div class="ie-container"><![endif]-->
  <!--[if mso]><div class="mso-container"><![endif]-->
  <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0">
  <tbody>
  <tr style="vertical-align: top">
    <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #e7e7e7;"><![endif]-->
    

<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
  
<table id="u_content_image_3" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:'Raleway',sans-serif;" align="left">
        
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding-right: 0px;padding-left: 0px;" align="center">
      
      <img align="center" border="0" src="$logo_img" alt="image" title="image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 16%;max-width: 92.8px;" width="92.8" class="v-src-width v-src-max-width"/>
      
    </td>
  </tr>
</table>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>



<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="background-color: #ffffff;height: 100%;width: 100% !important;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->
  
<table id="u_content_image_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 0px 0px;font-family:'Raleway',sans-serif;" align="left">
        
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding-right: 0px;padding-left: 0px;" align="center">
      
      <img align="center" border="0" src="$poap_img" alt="image" title="image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 80%;max-width: 480px;" width="480" class="v-src-width v-src-max-width"/>
      
    </td>
  </tr>
</table>

      </td>
    </tr>
  </tbody>
</table>

<table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;" align="left">
        
  <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 3px solid #575757;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
    <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
          <span>&#160;</span>
        </td>
      </tr>
    </tbody>
  </table>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>



<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="background-color: #f6f6f6;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="background-color: #f6f6f6;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
  
<table id="u_content_heading_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 10px 10px;font-family:'Raleway',sans-serif;" align="left">
        
  <h1 style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: Arvo; font-size: 24px;"><strong>POAP를 성공적으로 보냈습니다</strong></h1>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_button_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;" align="left">
        
  <!--[if mso]><style>.v-button {background: transparent !important;}</style><![endif]-->
<div align="center">
  <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://www.unlayer.com" style="height:37px; v-text-anchor:middle; width:203px;" arcsize="67.5%"  stroke="f" fillcolor="#ffce00"><w:anchorlock/><center style="color:#000000;font-family:'Raleway',sans-serif;"><![endif]-->  
    <a href="$opensea_link" target="_blank" class="v-button v-size-width" style="box-sizing: border-box;display: inline-block;font-family:'Raleway',sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #000000; background-color: #ffce00; border-radius: 25px;-webkit-border-radius: 25px; -moz-border-radius: 25px; width:35%; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;">
      <span class="v-padding" style="display:block;padding:10px 20px;line-height:120%;"><strong><span style="font-size: 14px; line-height: 16.8px;">Opensea에서 확인하기</span></strong></span>
    </a>
  <!--[if mso]></center></v:roundrect><![endif]-->
</div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_text_2" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 50px;font-family:'Raleway',sans-serif;" align="left">
        
  <div style="line-height: 160%; text-align: center; word-wrap: break-word;">
    <p style="line-height: 160%; font-size: 14px;">$howMany 개의 POAP가 준비되었습니다</p>
    <p style="line-height: 160%; font-size: 14px;">비용을 지불한 지갑주소는</p>
    <p style="line-height: 160%; font-size: 14px;">$whoPaid 입니다.</p>
    <p style="line-height: 160%; font-size: 14px;">비용지불 Smart contract 주소는</p>
    <p style="line-height: 160%; font-size: 14px;">$paidTxHash 입니다</p>
  </div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_image_2" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;" align="left">
        
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding-right: 0px;padding-left: 0px;" align="center">
      
      <img align="center" border="0" src="$star_img" alt="image" title="image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 7%;max-width: 42px;" width="42" class="v-src-width v-src-max-width"/>
      
    </td>
  </tr>
</table>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_heading_2" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 40px;font-family:'Raleway',sans-serif;" align="left">
        
  <h1 style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: Arvo; font-size: 20px;"><strong>Stellaiam</strong></h1>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>



<div class="u-row-container" style="padding: 0px;background-color: transparent">
  <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
      
<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
  <div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
  <!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
  
<table id="u_content_text_3" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 80px 10px;font-family:'Raleway',sans-serif;" align="left">
        
  <div style="line-height: 160%; text-align: center; word-wrap: break-word;">
    <p style="font-size: 14px; line-height: 160%;">문의 사항은 <a rel="noopener" href="mailto:18thcenturyprogrammer@gmail.com" target="_blank">18thcenturyprogrammer@gmail.com</a> 로 보내주시거나 http://127.0.0.1:8000 에서 확인하세요.</p>
  </div>

      </td>
    </tr>
  </tbody>
</table>

<table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 0px;font-family:'Raleway',sans-serif;" align="left">
        
  <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #BBBBBB;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
    <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
          <span>&#160;</span>
        </td>
      </tr>
    </tbody>
  </table>

      </td>
    </tr>
  </tbody>
</table>

<table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;" align="left">
        
<div align="center">
  <div style="display: table; max-width:187px;">
  <!--[if (mso)|(IE)]><table width="187" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-collapse:collapse;" align="center"><table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse; mso-table-lspace: 0pt;mso-table-rspace: 0pt; width:187px;"><tr><![endif]-->
  
    
    <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
    <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 15px">
      <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <a href="" title="Facebook" target="_blank">
          <img src="$facebook_logo" alt="Facebook" title="Facebook" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
        </a>
      </td></tr>
    </tbody></table>
    <!--[if (mso)|(IE)]></td><![endif]-->
    
    <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
    <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 15px">
      <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <a href="" title="Twitter" target="_blank">
          <img src="$twitter_logo" alt="Twitter" title="Twitter" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
        </a>
      </td></tr>
    </tbody></table>
    <!--[if (mso)|(IE)]></td><![endif]-->
    
    <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 0px;" valign="top"><![endif]-->
    <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32" style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 0px">
      <tbody><tr style="vertical-align: top"><td align="left" valign="middle" style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <a href="" title="Instagram" target="_blank">
          <img src="$instagram_logo" alt="Instagram" title="Instagram" width="32" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
        </a>
      </td></tr>
    </tbody></table>
    <!--[if (mso)|(IE)]></td><![endif]-->
    
    
    <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
  </div>
</div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_menu_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;" align="left">
        
<div class="menu" style="text-align:center">
<!--[if (mso)|(IE)]><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center"><tr><![endif]-->

  <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
  
    <a href="http://127.0.0.1:8000" target="_self" style="padding:5px 15px;display:inline-block;color:#000000;font-size:14px;text-decoration:none"  class="v-padding">
      Home
    </a>
  
  <!--[if (mso)|(IE)]></td><![endif]-->
  
    <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
    <span style="padding:5px 15px;display:inline-block;color:#000000;font-size:14px" class="v-padding hide-mobile">
      |
    </span>
    <!--[if (mso)|(IE)]></td><![endif]-->
  

  <!--[if (mso)|(IE)]><td style="padding:5px 15px"><![endif]-->
  
    <a href="https://www.unlayer.com" target="_self" style="padding:5px 15px;display:inline-block;color:#000000;font-size:14px;text-decoration:none"  class="v-padding">
      About Us
    </a>
  
  <!--[if (mso)|(IE)]></td><![endif]-->
  

<!--[if (mso)|(IE)]></tr></table><![endif]-->
</div>

      </td>
    </tr>
  </tbody>
</table>

<table id="u_content_text_4" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
  <tbody>
    <tr>
      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 40px;font-family:'Raleway',sans-serif;" align="left">
        
  <div style="line-height: 160%; text-align: center; word-wrap: break-word;">
    <p style="font-size: 14px; line-height: 160%;"> </p>
<p style="font-size: 14px; line-height: 160%;">Stellaiam All rights reserved</p>



  </div>

      </td>
    </tr>
  </tbody>
</table>

  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
  </div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
    </div>
  </div>
</div>


    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
    </td>
  </tr>
  </tbody>
  </table>
  <!--[if mso]></div><![endif]-->
  <!--[if IE]></div><![endif]-->
</body>

</html>''')
    

    content = template.substitute(
      logo_img= logo_img, 
      facebook_logo= facebook_logo, 
      twitter_logo= twitter_logo, 
      instagram_logo=instagram_logo,
      poap_img=poap_img,
      howMany=howMany,
      paidTxHash=paidTxHash,
      whoPaid=whoPaid,
      opensea_link=opensea_link,
      star_img=star_img
      )

    logger.info(content)


    # Data to be encoded
    data = "{website}receive_poap/{id}".format(website=config('WEBSITE'), id = poapClaim.id)
    
    # Encoding data using make() function
    img = qrcode.make(data)
      
    # Saving as an image file
    img.save('./media/qr_imgs/{id}_poap_qrcode.png'.format(id=poapClaim.id))

    logger.info(img)
    logger.info("img img img img img img img")
    logger.info(dir(img))

    
    # msg.set_content(content, subtype='html')
    # msg['Subject'] = "{howMany}개의 POAP이 전송되었습니다 - stellaiam".format(howMany=howMany)
    # msg['From'] = email_address
    # msg['To'] = poapClaim.email
    







    msg = MIMEMultipart("alternative")
    msg["Subject"] = "{howMany}개의 POAP이 전송되었습니다 - stellaiam".format(howMany=howMany)
    msg["From"] = email_address
    msg["To"] = poapClaim.email
    filename = "poap_qrcode.png"

    part = MIMEText(content, "html")
    msg.attach(part)

    # Add Attachment
    with open('./media/qr_imgs/{id}_poap_qrcode.png'.format(id=poapClaim.id), "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
      
    encoders.encode_base64(part)

    # Set mail headers
    part.add_header(
        "Content-Disposition",
        "attachment", filename= filename
    )
    msg.attach(part)

    









    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg, from_addr=email_address, to_addrs=poapClaim.email)



def getFileExtension(filePathName):
  # this will return a tuple of root and extension
  split_tup = os.path.splitext(filePathName)
  print(split_tup)
    
  # extract the file name and extension
  file_name = split_tup[0]
  file_extension = split_tup[1]
    
  print("File Name: ", file_name)
  print("File Extension: ", file_extension)
  return file_extension
