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

class ProductsListGuest(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# DONE Signed in user browsable products
class ProductsList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        products = Product.objects.exclude(owner = request.user.id)
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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
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
            {"response": "Product deleted successfully!"},
            status=status.HTTP_200_OK
        )
        
class CategoriesListGuest(APIView):
    def get(self, request, format=None):
        products = Category.objects.all()
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
            {"response": "Category deleted successfully!"},
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
        if type == "received":
            transaction = request.user.received_money
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
        receiver = User.objects.get(email= request.data.get('receiver'))

        data = {
            'sender': request.user.id,
            'receiver': receiver.id,
            'transaction_size': request.data.get('transaction_size'),
        }            

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            transaction_size = int(request.data.get('transaction_size'))
            if transaction_size > request.user.profile.cash:
                return Response(
                    {"response": "The amount is larger than available cash"}
                    , status=status.HTTP_400_BAD_REQUEST)
            request.user.profile.cash = request.user.profile.cash - transaction_size
            request.user.save()
            receiver.profile.cash = receiver.profile.cash + transaction_size
            receiver.save()
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
        receiver = User.objects.get(email=request.data.get('receiver'))
        data = {
            'sender': request.user.id,
            'receiver': receiver.id,
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
            {"response": "Transaction deleted successfully!"},
            status=status.HTTP_200_OK
        )

# DONE Create GiftView Class
class GiftView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        type = request.GET.get('type')
        gift_req=[]
        if type == "received":
            gift_req = request.user.gifts
        elif type == "sent":
            order_ids = (Order.objects.filter(maker= request.user.id)).values_list('id', flat=True)
            gift_req = Gift.objects.filter(order__in= order_ids)
        if not gift_req:
            return Response({"Gifts": []}) ## TODO

        serializer = GiftSerializerNested(gift_req, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):

        receiver = User.objects.get(email= request.data.get('receiver'))
        order_data = {
            'maker': request.user.id,
            'product': request.data.get('product'),
            'location': receiver.profile.location,
            'amount': request.data.get('amount'),
            'date_added': datetime.datetime.now()
        }
        order_serializer = OrderSerializerFlat(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            product = Product.objects.get(pk=request.data.get('product'))
            if product.no_of_pieces < int(request.data.get('amount')):
                return Response(
                    {"response": "The amount is larger than available number of pieces"}, 
                    status=status.HTTP_400_BAD_REQUEST   
                )
            new_no_of_pieces = product.no_of_pieces - int(request.data.get('amount'))
            product = Product.objects.filter(pk=request.data.get('product')).update(no_of_pieces = new_no_of_pieces)

        data = {
            'order':  order.id,
            'receiver': receiver.id,
        }

        serializer = GiftSerializerFlat(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DONE Create GiftDetail Class
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
        serializer = GiftSerializerNested(gift)
        return Response(serializer.data)
    
    def put(self, request, gift_id, format=None):
        gift = self.get_object(gift_id)
        data = {
            'order': request.data.get('order'),
            'receiver': (User.objects.get(email = request.data.get('receiver'))).id,
        }
        serializer = GiftSerializerFlat(instance = gift, data = data, partial = True)
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
            {"response": "Gift deleted successfully!"},
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

        serializer = OrderSerializerNested(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = {
            'maker': request.user.id,
            'product': request.data.get('product'),
            'location': request.data.get('location'),
            'amount': request.data.get('amount'),
            'date_added': datetime.datetime.now()
        }
        
        serializer = OrderSerializerFlat(data=data)
        if serializer.is_valid():
            serializer.save()
            product = Product.objects.get(pk=request.data.get('product'))
            if product.no_of_pieces < int(request.data.get('amount')):
                return Response(
                    {"response": "The amount is larger than available number of pieces"}, 
                    status=status.HTTP_400_BAD_REQUEST   
                )
            new_no_of_pieces = product.no_of_pieces - int(request.data.get('amount'))
            if request.user.profile.cash < int(product.price):
                return Response(
                    {"response": "The price is higher than available cash"}, 
                    status=status.HTTP_400_BAD_REQUEST   
                )
            request.user.profile.cash = request.user.profile.cash - int(product.price)
            request.user.save()
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
        serializer = OrderSerializerNested(order)
        return Response(serializer.data)
    
    def put(self, request, order_id, format=None):
        order = self.get_object(order_id)
        serializer = OrderSerializerFlat(order)
        data = {
            'maker': request.user.id,
            'product': request.data.get('product'),
            'location': request.data.get('location'),
            'amount': request.data.get('amount'),
            'date_added': request.data.get('date_added')
        }
        serializer = OrderSerializerFlat(instance = order, data = data, partial = True)
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
            {"response": "Order deleted successfully!"},
            status=status.HTTP_200_OK
        )

# Done Get Sold Products
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def getSoldProducts(request):
    orders = Order.objects.filter(product__owner = request.user.id)
    if not orders:
        return Response(
            {"response": "Orders not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = OrderSerializerNested(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# DONE Create ShareView Class
class ShareView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        share = Share.objects.filter(share_holder = request.user.id)
        serializer = ShareSerializerNested(share, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = {
            'product': request.data.get('product'),
            'share_holder': request.user.id,
        }

        serializer = ShareSerializerFlat(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DONE Create ShareDetail Class
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
                {"response": "Shared offer does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        serializer = ShareSerializerNested(share)
        return Response(serializer.data)

    def delete(self, request, share_id):
        share = self.get_object(share_id)
        if not share:
            return Response(
                {"response": "Shared offer does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        share.delete()
        return Response(
            {"response": "Shared offer deleted successfully!"},
            status=status.HTTP_200_OK
        )

# DONE API for Profile
class ProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,format=None):
        profile = Profile.objects.get(pk=request.user.id)
        serializer = ProfileSerializerNested(profile)
        return Response(serializer.data)

# DONE API for cash Deposit
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deposit(request):
    value = request.data.get('value', '')

    if value:
        profile = Profile.objects.get(user = request.user.id)
        data = {
            'user': request.user.id,
            'cash': profile.cash + int(value),
            'location': profile.location,
            'birth_date': profile.birth_date,
            'sex': profile.sex,
        }
        serializer = ProfileSerializerFlat(instance = profile, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"response": "Please try again later"},
            status=status.HTTP_400_BAD_REQUEST
        )

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
        serializer = ProfileSerializerNested(profile)
        return Response(serializer.data)
    
    def put(self, request, profile_id, format=None):
        profile = self.get_object(profile_id)
        data = {
            'user':request.user.id,
            'cash': request.data.get('cash'),
            'location': request.data.get('location'),
            'birth_date':request.data.get('birth_date'),
            'phone': request.data.get('phone'),
            'sex':request.data.get('sex'),
        }
        serializer = ProfileSerializerFlat(instance = profile, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        profile = self.get_object(profile_id)
        if not profile:
            return Response(
                {"response": "Profile does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST   
            )
        profile.delete()
        return Response(
            {"response": "Profile deleted successfully!"},
            status=status.HTTP_200_OK
        )
