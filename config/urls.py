"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config.views import home

urlpatterns = [
    path("", home),

    path('admin/', admin.site.urls),
    path('auth/', include("userAPI.urls")),

    path('api/categories/', include("categoryAPI.urls")),
    path('api/products/', include("productAPI.urls")),
    path('api/inventory/', include("inventoryAPI.urls")),
    path('api/chats/', include("chatsAPI.urls")),
    path('api/notifications/', include("notificationAPI.urls")),
    path('api/cart/', include("cartAPI.urls")),
    path('api/wishlist/', include("wishlistAPI.urls")),
    path('api/orders/', include("orderAPI.urls")),
    path('api/orderlines/', include("orderlineAPI.urls")),
    path('api/payments/', include("paymentAPI.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# localhost:8000
# localhost:8000/admin
# localhost:8000/api/v1.0/user/

# localhost:8000/api