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
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage

from AXEL.settings import EMAIL_HOST_USER , ROOT_DOMAIN, MEDIA_ROOT

from.serializer import productSerializer, cartSerializer
from .form import productCreationForm
from .models import Product , Cart

from django.db.models import Q

from Shop.models import User

import os
import json
from PIL import Image

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.method == "POST":
        form = productCreationForm(request.data)

        if(form.is_valid()):
            form.save()
            ps = productSerializer(form.instance)
            return Response(ps.data)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST' , 'PATCH'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def product_image(request,id:int):
    try:
        prod = Product.objects.get(id__exact=id)
        if str(request.user.username) == str(prod.owner):
            imgs = request.FILES
            images = [] if len(prod.images) <= 3 else json.loads(prod.images)
            fs = FileSystemStorage()
            for img in imgs.values():
                name = fs.save(img.name,img)
                img = Image.open(os.path.join(MEDIA_ROOT , name))
                # limit the resolution of images in our local storage
                if(img.height > 500 or img.width > 500):
                    output_size = (500,500)
                    img.thumbnail(output_size)
                    img.save(os.path.join(MEDIA_ROOT , name))
                # update the name of the file in images  because django migth rename it
                images.append(name)
            prod.images = json.dumps(images)
            prod.save()
            pt = productSerializer(prod)
            return Response(pt.data)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def product(request,id:int):
    try:
        product = Product.objects.get(id__exact=id)
        if request.method == 'GET':
            s_prod = productSerializer(product)
            return Response(s_prod.data)

        if str(request.user.username) == str(product.owner):
            data = request.data
            if request.method == 'PATCH':
                if data.get('price') != None:
                    product.price = data['price']
                if data.get('name') != None:
                    product.name = data['name']
                if data.get('description') != None:
                    product.description = data['description']
                if data.get('brand') != None:
                    product.brand = data['brand']
                if data.get('genre') != None:
                    product.genre = data['genre']
                if data.get('quantity') != None:
                    product.quantity = data['quantity']
                product.save()

            elif request.method == 'DELETE':
                ls = list(json.loads(product.images))
                for file in ls:
                    if os.path.exists(os.path.join(MEDIA_ROOT, file)):
                        os.remove(os.path.join(MEDIA_ROOT, file))
                        
                product.delete(keep_parents=True)
            sd = productSerializer()
            return Response(sd.data)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        if(e == ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request):
    try:
        data_per_page:int = 20
        page:int = 1

        try:
            data_per_page = data_per_page if (request.query_params.get('object_per_page') == None) else int(request.query_params.get('data_per_page'))
            page = page if (request.query_params.get('page_number') == None) else int(request.query_params.get('page_number'))
        except:
            data_per_page = 20
            page = 1 
        finally:
            start = (page-1) * data_per_page if (page > 1) else 0
            end = start + data_per_page
            
            Q_obj = Q()
            if request.data.get("brand") != None:
                Q_obj &= Q(**{f'brand__in': request.data.get("brand")}) 
            if request.data.get("name") != None:
                Q_obj &= Q(**{f'name__icontains': request.data.get("name")})
            if request.data.get("owner") != None:
                Q_obj &= Q(**{f'owner__iexact': request.data.get("owner")})
            if request.data.get("date_created") != None:
                Q_obj &= Q(**{f'date_created__range': request.data.get("date_created")})
            if request.data.get("genre") != None:
                Q_obj &= Q(**{f'genre__in': request.data.get("genre")})
            if request.data.get("price") != None:
                Q_obj &= Q(**{f'price__range': request.data.get("price")})
            prods = Product.objects.filter(Q_obj).order_by('-date_created')[start : end]
            return Response(productSerializer(prods, many=True).data)

    except Exception as e:  
        if(e == ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)  
        elif(e == FieldError):
            print("Field Error")
    return Response(status=status.HTTP_400_BAD_REQUEST)






# Create your views here.
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_to_cart(request,id:int):
    try:
        obj = Cart.objects.filter(id__exact=id)
        cart = None
        if len(obj) > 0:
            cart = Cart.objects.get(id__exact=id)
        else:
            cart = Cart(customer=request.user)
            cart.save()
        
        if str(request.user.username) == str(cart.customer):
            prod = Product.objects.get(id__exact=request.data['id'])
            ls = []
            if len(cart.products) == 0 or cart.products == None:
                ls.append({"id": request.data["id"], "quantity": request.data["quantity"]})
                cart.products = json.dumps(ls)
            else:
                ls = list(json.loads(cart.products))
                ls.append({"id": request.data["id"],  "quantity": request.data["quantity"]})
                cart.products = json.dumps(ls)
            cost = 0
            for p in ls:
                prod = Product.objects.get(id__exact=p['id'])
                cost += prod.price * p["quantity"]
            cart.cost = cost
            cart.save()
            return Response(cartSerializer(cart).data)

        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        if(e == ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    




# Create your views here.
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request,id:int):
    try:
        cart = Cart.objects.get(id__exact=id)
        if str(request.user.username) == str(cart.customer):
            prod = Product.objects.get(id__exact=request.data['id'])
            ls = []
            if len(cart.products) > 0:
                ls = list(json.loads(cart.products))
                to_remove = None
                for p in ls:
                    if(p["id"] == request.data["id"]):
                        if p["quantity"] <= request.data["quantity"]:
                            to_remove = p
                            break
                        else:
                            p["quantity"] -= request.data["quantity"]
                            break

                if to_remove != None:
                    ls.remove(to_remove)
                cart.products = json.dumps(ls)

            cost = 0
            for p in ls:
                prod = Product.objects.get(id__exact=p['id'])
                cost += prod.price * p["quantity"]
            cart.cost = cost
            cart.save()
            return Response(cartSerializer(cart).data)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        if(e == ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)



    
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request,id:int):
    try:
        cart = Cart.objects.get(id__exact=id)
        if request.method == 'GET':
            return Response(cartSerializer(cart).data)
        
        if str(request.user.username) == str(cart.customer):
        
            if request.method == 'DELETE':
                cart.delete(keep_parents=True)
            return Response()
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        if(e == ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_carts(request):
    try:
        data_per_page:int = 20
        page:int = 1

        try:
            data_per_page = data_per_page if (request.query_params.get('object_per_page') == None) else int(request.query_params.get('data_per_page'))
            page = page if (request.query_params.get('page_number') == None) else int(request.query_params.get('page_number'))
        except:
            data_per_page = 20
            page = 1 
        finally:
            start = (page-1) * data_per_page if (page > 1) else 0
            end = start + data_per_page
            
            Q_obj = Q()
            if request.data.get("date_created") != None:
                Q_obj &= Q(**{f'date_created__range': request.data.get("date_created")})
            if request.data.get("is_paid_for") != None:
                Q_obj &= Q(**{f'is_paid_for': request.data.get("is_paid_for")})
            if request.data.get("customer") != None:
                Q_obj &= Q(**{f'customer__exact': request.data.get("customer")})

            carts = Cart.objects.filter(Q_obj).order_by('-date_created')[start : end]
            return Response(cartSerializer(carts, many=True).data)
    except Exception as e:
        if(e == ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)