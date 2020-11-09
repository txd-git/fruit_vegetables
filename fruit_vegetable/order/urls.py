from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.OrderInfoView.as_view()),
    #http://127.0.0.1:8000/v1/orders/<username>/advance
    path('<str:username>/advance', views.AdvanceOrderView.as_view()),
    # url('(?P<username>\w+)/advance$', views.AdvanceOrderView.as_view())
]
