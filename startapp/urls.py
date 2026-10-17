from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register("products", ProductViewSet,basename="products")
router.register("orders", OrderViewSet,basename="orders")


urlpatterns = router.urls
