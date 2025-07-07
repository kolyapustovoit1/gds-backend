from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders.views import OrderListAPIView, OrderDetailAPIView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail-api'),
    path('api/orders/', OrderListAPIView.as_view(), name='order-list-api'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

