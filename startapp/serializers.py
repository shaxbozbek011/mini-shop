from django.db import transaction
from rest_framework import serializers

from .models import Product, Order,OrderItem



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'




class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
        ]


    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Miqdor kamida 1 bo'lishi kerak.")
        return value



    def validate_product(self, product):
        if not product.is_active:
            raise serializers.ValidationError("Bu mahsulot sotuvda yo'q")

        return product



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'created_at',
            'updated_at',
            'total_price',
            'items',


        ]


    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

    def validate_items(self, value):

      if not value:
          raise serializers.ValidationError("Buyurtmada kamida 1 ta mahsulot bo'lishi kerak.")
      return value



    @transaction.atomic
    def create(self, validated_data):
      items_data = validated_data.pop('items')
      order = Order.objects.create(**validated_data)

      OrderItem.objects.bulk_create([
          OrderItem(
              order=order,
              product=item['product'],
              quantity=item['quantity'],
              price=item['product'].price,
          )
          for item in items_data
      ])
      return order



