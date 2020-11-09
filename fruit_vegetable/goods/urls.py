from django.urls import path
from . import views
urlpatterns=[
    path('detail/<int:goodsid>',views.GoodsDetailView.as_view()),
    path('catalogs/<int:type>',views.GoodsListView.as_view()),
]