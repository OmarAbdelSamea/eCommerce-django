from django.db.models import Q
from django.shortcuts import render
from django.http import Http404

from rest_framework import status, authentication, permissions
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
            'no_of_pieces': request.data.get('no_of_pieces')
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
        serializer = ProductSerializer(product, many=True)
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
            'no_of_pieces': request.data.get('no_of_pieces')
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

# TODO Create GiftDetail Class

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
            # Sold should be on_sale to differ owned items from 
            # one are being saled
            'sold': True,
            'amount': request.data.get('amount'),
            'date_added': datetime.datetime.now()
        }

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            product = Product.objects.filter(pk=request.data.get('product')).update(owner=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            'sold': request.data.get('sold'),
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

# TODO Create ShareDetail Class

# TODO API for cash Deposit

# TODO API for Profile

# TODO Import Decimal and use it for all Decimal values
