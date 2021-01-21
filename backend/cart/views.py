from django.contrib.auth.models import User
from cart.models import Product, Order
from cart.serializers import ProductSerializer, OrderSerializer
from cart.serializers import UserSerializer
from cart.permissions import IsOwnerOrReadOnly
from cart.permissions import IsStaffOrTargetUser
from django.contrib.auth.hashers import make_password

from rest_framework import viewsets, permissions
from rest_framework import generics


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-name')
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    )

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()),

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)
