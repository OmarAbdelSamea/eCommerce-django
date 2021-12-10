
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
            'on_sale',
            'shared_by',
        )
        read_only_fields = ('shared_by',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = Transaction
        fields = (
            'id',
            'sender',
            'sender_name',
            'receiver',
            'receiver_name',
            'transaction_size',
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
            'id',
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
    share_holder_name = serializers.ReadOnlyField(source='share_holder.username')
    class Meta:
        model = Share
        fields = (
            'id',
            'product',
            'share_holder',
            'share_holder_name'
        )

class ShareSerializerFlat(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'

class GiftSerializerNested(serializers.ModelSerializer):
    order = OrderSerializerFlat('order')
    receiver = UserSerializer('receiver')

    class Meta:
        model = Gift
        fields = '__all__'

class GiftSerializerFlat(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'