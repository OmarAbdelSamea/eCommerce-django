
from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    owner_name = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Product
        fields = (
            'id',
            'category_name',
            'owner_name',
            'category',
            'owner',
            'name',
            'description',
            'price',
            'no_of_pieces',
            'image_main',
            'image_thumbnail',
            'date_added',
            'on_sale'
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    maker_name = serializers.ReadOnlyField(source='maker.username')
    class Meta:
        model = Transaction
        fields = (
            'maker_name',
            'product',
            'amount'
        )

class OrderSerializerNested(serializers.ModelSerializer):
    product = ProductSerializer('product')
    maker_name = serializers.ReadOnlyField(source='maker.username')
    class Meta:
        model = Order
        fields = (
            'id',
            'maker',
            'maker_name',
            'product',
            'location',
            'amount',
            'date_added'
        )

class OrderSerializerFlat(serializers.ModelSerializer):
    maker_name = serializers.ReadOnlyField(source='maker.username')
    class Meta:
        model = Order
        fields = (
            'maker',
            'maker_name',
            'product',
            'location',
            'amount',
            'date_added'
        )
class ProfileSerializerNested(serializers.ModelSerializer):
    user = UserSerializer('user')
    class Meta:
        model = Profile
        fields = '__all__'
      
class ProfileSerializerFlat(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 

class ShareSerializerNested(serializers.ModelSerializer):
    product = ProductSerializer('product')
    class Meta:
        model = Share
        fields = '__all__'

class ShareSerializerFlat(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'
class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'