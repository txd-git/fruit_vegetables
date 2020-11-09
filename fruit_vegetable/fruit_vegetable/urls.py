"""fruit_vegetable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from btoken import views as btoken_views
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('v1/users/',include('user.urls')),
    path('v1/tokens',btoken_views.TokenViews.as_view()),
    #详情页
    path('v1/goods/',include('goods.urls')),
    path('v1/orders/',include('order.urls')),


    #*****************************
    path('v1/users/password/verification', views.pwfind),
    path('v1/carts/', include("carts.urls")),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
