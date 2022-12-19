from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Discount, ProductItem, Producer, Promocode, \
    RegistredUser


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class ProducerSerializer(ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'


class PromocodeSerializer(ModelSerializer):
    class Meta:
        model = Promocode
        fields = '__all__'


class ProductItemSerializer(ModelSerializer):
    producer = ProducerSerializer()
    category = CategorySerializer()
    discount = DiscountSerializer()

    class Meta:
        model = ProductItem
        fields = ['id', 'name', 'description', 'producer', 'category', 'discount',
                  'price', 'articul', 'count_on_stock']


class RegistrationSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=100,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(
        max_length=255,
        read_only=True
    )

    class Meta:
        model = RegistredUser
        fields = ['phone', 'email', 'password', 'login', 'token', 'age']

    def create(self, validated_data):
        return RegistredUser.objects.create_user(**validated_data)



