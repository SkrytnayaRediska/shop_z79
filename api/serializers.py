from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Discount, ProductItem, Producer, Promocode, \
    RegistredUser, Order

from django.contrib.auth import authenticate
import datetime


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


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    password = serializers.CharField(max_length=100, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone = data.get('phone', None)
        password = data.get('password', None)

        if phone is None:
            raise serializers.ValidationError("Phone number is required to log in")
        if password is None:
            raise serializers.ValidationError("Password is required to log in")

        user = authenticate(username=phone, password=password)

        if user is None:
            raise serializers.ValidationError("A user with this phone and password was not found")

        if not user.is_active:
            raise serializers.ValidationError("This account was not verified")

        return {
            'phone': user.phone,
            'token': user.token
        }


class ProductInBasketSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    number_of_items = serializers.IntegerField()


class BasketSerializer(serializers.Serializer):
    products = ProductInBasketSerializer(many=True)
    result_price = serializers.SerializerMethodField()

    def get_result_price(self, data):
        result_price = 0

        for item in data.get('products'):
            if item.get("discount"):
                percent = item.get("discount_percent")
                expire_date = item.get("discount_expire_date")
                delta = expire_date - datetime.datetime.now(datetime.timezone.utc)
                if delta.days >= 0 and delta.seconds >= 0:
                    result_price += (item.get("price") * (100 - percent) / 100) * item.get("number_of_items")
                else:
                    result_price += item.get("price") * item.get("number_of_items")
            else:
                result_price += item.get("price") * item.get("number_of_items")

        return result_price


class AddProductsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    number_of_items = serializers.IntegerField()


class DeleteProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):

    def run_validation(self, data=None):
        return data

    class Meta:
        model = Order
        fields = '__all__'

    def calculate_result_price(self, data):
        product_items_dict = data.get('product_items')
        product_items_ids = product_items_dict.keys()
        product_items = ProductItem.objects.filter(id__in=product_items_ids).values('id', 'price',
                                                                                    'discount__percent',
                                                                                    'discount__expire_date')
        promocode_name = data.get('promocode')
        promocode = Promocode.objects.filter(name=promocode_name).first()

        result_price = 0

        for item in product_items:
            number_of_items = product_items_dict.get(str(item.get('id')))
            discount_percent = item.get('discount__percent')
            price = item.get('price')

            if not promocode or promocode.is_allowed_to_sum_with_discounts:
                if discount_percent:

                    discount_expire = item.get('discount__expire_date')
                    delta = discount_expire - datetime.datetime.now(datetime.timezone.utc)
                    if delta.days >= 0 and delta.seconds >= 0:
                        result_price += price * (100 - discount_percent) / 100 * number_of_items
                    else:
                        result_price += price * number_of_items
                else:
                    result_price += price * number_of_items
            else:
                result_price += price * number_of_items

        if promocode:
            result_price = result_price * (100 - promocode.percent) / 100

        return result_price

    def calculate_result_number_of_items(self, data):
        return sum(data.get('product_items').values())

    def get_user(self):
        request = self.context.get('request')
        return request.user

    def create(self, validated_data):
        validated_data['result_price'] = self.calculate_result_price(validated_data)
        validated_data['result_number_of_items'] = self.calculate_result_number_of_items(validated_data)
        validated_data['user'] = self.get_user()

        if validated_data.get('promocode'):
            validated_data.pop('promocode')

        validated_data.pop('use_cashback')

        return Order.objects.create(**validated_data)






