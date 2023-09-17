from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view , parser_classes
from rest_framework.parsers import MultiPartParser

#from django.contrib.auth.password_validation import validate_password
#from django.core.exceptions import ValidationError
#from django.contrib.auth.hashers import make_password , check_password
from rest_framework.decorators import permission_classes , authentication_classes
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage

from AXEL.settings import EMAIL_HOST_USER , ROOT_DOMAIN
from.serializer import productSerializer, cartSerializer

import os

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.method == "POST":
        ps = productSerializer((request.data))

        if(ps.is_valid()):
            ps.save()
            return Response((ps.data))
        else:
            return Response(ps.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Create your views here.
@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def product_image(request):
    if(request.method == 'PUT'):
        try:

            imgs = request.FILES
            prod = Product.objects.get(id__exact=id)
            images = json.loads(prod.images)

            fs = FileSystemStorage()
            
            for img in imgs.values():
                name = fs.save(img.name,img)
                # update the name of the file in images  because django migth rename it
                for _img in images.value():
                    if _img.name == img.name:
                        _img.name = name
                        break

            prod.images = json.dumps(images)
            prod.save()

            pt = productSerializer(prod)
            return Response(pt.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Create your views here.
@api_view(['PUT', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def product(request,int:id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id__exact=id)
            s_prod = productSerializer(s_prod)
            return Response(sp)
        except Exception as e:
            if(e == ObjectDoesNotExist):
                return Response(status=status.HTTP_404_NOT_FOUND) 
    elif request.method == 'PUT':
        pass

