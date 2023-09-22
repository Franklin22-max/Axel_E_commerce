from rest_framework.response import Response
from rest_framework.decorators import api_view , parser_classes
from rest_framework.parsers import MultiPartParser
from .serializer import userSerializer
from .form import passResetForm, signinForm
from .models import User
#from django.contrib.auth.password_validation import validate_password
#from django.core.exceptions import ValidationError
#from django.contrib.auth.hashers import make_password , check_password
from rest_framework.decorators import permission_classes , authentication_classes
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from AXEL.settings import EMAIL_HOST_USER , ROOT_DOMAIN
import os

@api_view(['POST'])
@authentication_classes([])
def register(request):
    if request.method == "POST":

        jsondata = request.data
        form = signinForm(jsondata)

        if form.is_valid():
            form.save()
            serialized = userSerializer(form.instance)

            return Response(serialized.data)
        else:
            errors = []
            for err in form.errors.items():
                errors.append(err)

            return Response( errors, status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        Rtoken = RefreshToken(request.data['refresh_token'])
        Rtoken.blacklist()
        return Response()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        data = request.data
        
        try:
            user = User.objects.get(email__exact=data['email'])

            """ validate_password(data['password'])
            check_password(data['password'],user.password) """
            serialized = userSerializer(user)
            return Response(serialized.data)
            
        except Exception as e:
            print(e)
            if(e == ObjectDoesNotExist):
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                 return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def resetPassword(request):
    try:
        user = User.objects.get(email__exact=request.data['email'])

        send_mail("Axel PassWord Reset","", from_email=EMAIL_HOST_USER, recipient_list=[request.data['email']],
        html_message=f"""
        <div>
            <h1>AXEL PASSWORD RESET MAIL</h1>
            <h2> A password reset request was made on your account, if this was not you ignore it otherwise click <a href="{ROOT_DOMAIN}/password-complete">here</a> <h2>
        </div>
         """,
        fail_silently=False)

        res = dict()
        res.setdefault("message","A message has been set to your email follow it to reset your password")
        return Response(res)
    except Exception as e:
        print(e)
        if(e == ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_417_EXPECTATION_FAILED)
    

        