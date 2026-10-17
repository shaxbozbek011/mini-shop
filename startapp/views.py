from rest_framework import viewsets, permissions

from startapp.models import Product, Order
from startapp.serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]




class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        qs = Order.objects.prefetch_related('items').order_by('-created_at')
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)






