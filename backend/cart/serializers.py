from django.contrib.auth.models import User

from rest_framework import serializers
from cart.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'quantity', 'rating', 'description', 'image_url', 'owner']


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Order
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'products']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
