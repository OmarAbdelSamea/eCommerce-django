from django.db.models import Q
from django.shortcuts import render
from django.http import Http404

from rest_framework import status, authentication, permissions
from rest_framework.fields import EmailField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Product, Category
from .serializers import *
from core import serializers
import datetime

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        products = Product.objects.filter(owner = request.user.id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = {
            'category': request.data.get('category'),
            'owner': request.user.id,
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'no_of_pieces': request.data.get('no_of_pieces'),
            'on_sale': request.data.get('on_sale'),
            'image_main': request.data.get('image_main'),
            'image_thumbnail': request.data.get('image_thumbnail'),
        }

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    def get_object(self, product_id):
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, product_id, format=None):
        product = self.get_object(product_id)
        if not product:
            return Response(
                {"response": "Product does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response(
                {"response": "Product does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        data = {
            'category': request.data.get('category'),
            'owner': request.user.id,
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'no_of_pieces': request.data.get('no_of_pieces'),
            'on_sale': request.data.get('on_sale'),
            'image_main': request.data.get('image_main'),
            'image_thumbnail': request.data.get('image_thumbnail'),
        }
        serializer = ProductSerializer(instance = product, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response(
                {"response": "Product does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        product.delete()
        return Response(
            {"response": "Product deleted succesfully!"},
            status=status.HTTP_200_OK
        )
        
class LatestCategoriesList(APIView):
    def get(self, request, format=None):
        products = Category.objects.all()[0:4]
        serializer = CategorySerializer(products, many=True)
        return Response(serializer.data)

class CategoryView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
        }

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, category_id):
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_id, format=None):
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, category_id, format=None):
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
        }
        serializer = CategorySerializer(instance = category, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        category = self.get_object(category_id)
        if not category:
            return Response(
                {"response": "Category does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        category.delete()
        return Response(
            {"response": "Category deleted succesfully!"},
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})


class TransactionView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        type = request.GET.get('type')
        if type == "recevied":
            transaction = request.user.recieved_money
        elif type == "sent":
            transaction = request.user.sent_money
        else:
            return Response(
                {"response": "Wrong transaction type"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )

        if not transaction:
            return Response({"transactions": []}) ## TODO

        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = {
            'sender': request.user.id,
            'reciever': request.data.get('reciever'),
            'transaction_size': request.data.get('transaction_size'),
        }

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, transaction_id):
        try:
            return Transaction.objects.get(pk=transaction_id)
        except Transaction.DoesNotExist:
            raise Http404
    
    def get(self, request, transaction_id, format=None):
        category = self.get_object(transaction_id)
        serializer = TransactionSerializer(category)
        return Response(serializer.data)
    
    def put(self, request, transaction_id, format=None):
        category = self.get_object(transaction_id)
        serializer = TransactionSerializer(category)
        data = {
            'sender': request.user.id,
            'reciever': request.data.get('reciever'),
            'transaction_size': request.data.get('transaction_size'),
        }
        serializer = TransactionSerializer(instance = category, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, transaction_id):
        category = self.get_object(transaction_id)
        if not category:
            return Response(
                {"response": "Transaction does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        category.delete()
        return Response(
            {"response": "Transaction deleted succesfully!"},
            status=status.HTTP_200_OK
        )

# TODO Create GiftView Class
class GiftView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        type = request.GET.get('type')
        gift_req=[]
        if type == "recevied":
            gift_req = request.user.gifts
        elif type == "sent":
            order_ids = (Order.objects.filter(maker= request.user.id)).values_list('id', flat=True)
            gift_req = Gift.objects.filter(order__in= order_ids)
        if not gift_req:
            return Response({"Gifts": []}) ## TODO

        serializer = GiftSerializer(gift_req, many=True)
        return Response(serializer.data)
    #shdedaaaaaaaaaaaaaaaaaaaaaaaa
    def post(self, request, format=None):

        data = {
            'order':  request.data.get('order'),
            'reciever': (User.objects.get(email= request.data.get('reciever'))).id,
        }

        serializer = GiftSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO Create GiftDetail Class
class GiftDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, gift_id):
        try:
            return Gift.objects.get(pk=gift_id)
        except Gift.DoesNotExist:
            raise Http404
    
    def get(self, request, gift_id, format=None):
        gift = self.get_object(gift_id)
        serializer = GiftSerializer(gift)
        return Response(serializer.data)
    
    def put(self, request, gift_id, format=None):
        gift = self.get_object(gift_id)
        serializer = GiftSerializer(gift)
        data = {
            'order': request.data.get('order'),
            'reciever': (User.objects.get(email = request.data.get('reciever'))).id,
        }
        serializer = GiftSerializer(instance = gift, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, gift_id):
        gift = self.get_object(gift_id)
        if not gift:
            return Response(
                {"response": "Gift does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        gift.delete()
        return Response(
            {"response": "Gift deleted succesfully!"},
            status=status.HTTP_200_OK
        )




# DONE Create OrderView Class
class OrderView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        orders = request.user.orders

        if not orders:
            return Response({"orders": []}) ## TODO

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = {
            'maker': request.user.id,
            'product': request.data.get('product'),
            'location': request.data.get('location'),
            'amount': request.data.get('amount'),
            'date_added': datetime.datetime.now()
        }
        
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            product = Product.objects.get(pk=request.data.get('product'))
            if product.no_of_pieces < int(request.data.get('amount')):
                return Response(
                    {"response": "The amount is larger than availble number of pieces"}, 
                    status=status.HTTP_400_BAD_REQUEST   
                )
            new_no_of_pieces = product.no_of_pieces - int(request.data.get('amount'))
            product = Product.objects.filter(pk=request.data.get('product')).update(no_of_pieces = new_no_of_pieces)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DONE Create OrderDetail Class
class OrderDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, order_id):
        try:
            return Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise Http404
    
    def get(self, request, order_id, format=None):
        order = self.get_object(order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def put(self, request, order_id, format=None):
        order = self.get_object(order_id)
        serializer = OrderSerializer(order)
        data = {
            'maker': request.user.id,
            'product': request.data.get('product'),
            'location': request.data.get('location'),
            'amount': request.data.get('amount'),
            'date_added': request.data.get('date_added')
        }
        serializer = OrderSerializer(instance = order, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = self.get_object(order_id)
        if not order:
            return Response(
                {"response": "Order does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        order.delete()
        return Response(
            {"response": "Order deleted succesfully!"},
            status=status.HTTP_200_OK
        )
# TODO Create ShareView Class
class ShareView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        share = Share.objects.filter(share_holder = request.user.id)
        serializer = ShareSerializer(share, many=True)
        return Response(serializer.data)

    #shdedaaaaaaaaaaaaaaaaaaaaaaaa
    def post(self, request, format=None):
        data = {
            'product': request.data.get('product'),
            'share_holder': request.user.id,
        }

        serializer = ShareSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO Create ShareDetail Class
class ShareDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, share_id):
        try:
            return Share.objects.get(pk=share_id)
        except Share.DoesNotExist:
            raise Http404
    
    def get(self, request, share_id, format=None):
        share = self.get_object(share_id)
        if not share:
            return Response(
                {"response": "shared offer does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        serializer = ShareSerializer(share)
        return Response(serializer.data)

    def delete(self, request, share_id):
        share = self.get_object(share_id)
        if not share:
            return Response(
                {"response": "shared offer does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        share.delete()
        return Response(
            {"response": "shared offer deleted succesfully!"},
            status=status.HTTP_200_OK
        )



# TODO API for cash Deposit

# TODO API for Profile
class ProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        profile = request.user.id
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    
# Done ProfileDetail
class ProfileDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, profile_id):
        try:
            return Profile.objects.get(pk=profile_id)
        except Profile.DoesNotExist:
            raise Http404
    
    def get(self, request, profile_id, format=None):
        profile = self.get_object(profile_id)
        serializer = OrderSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, profile_id, format=None):
        profile = self.get_object(profile_id)
        serializer = ProfileSerializer(profile)
        data = {
            'user':request.user.id,
            'cash': request.data.get('cash'),
            'location': request.data.get('location'),
            'birth_date':request.data.get('birth_date'),
            'sex':request.data.get('sex'),
        }
        serializer = ProfileSerializer(instance = profile, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        profile = self.get_object(profile_id)
        if not profile:
            return Response(
                {"response": "Order does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        profile.delete()
        return Response(
            {"response": "Order deleted succesfully!"},
            status=status.HTTP_200_OK
        )
 

# TODO Import Decimal and use it for all Decimal values
