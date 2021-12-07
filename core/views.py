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
            'sender': request.data.get('sender'),
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
            'sender': request.data.get('sender'),
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

# TODO Create OrderView Class

# TODO Create OrderDetail Class

# TODO Create ShareView Class

# TODO Create ShareDetail Class

# TODO API for cash Deposit

# TODO API for Profile

