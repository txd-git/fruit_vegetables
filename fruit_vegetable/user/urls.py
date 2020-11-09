from django.urls import path
from . import views
urlpatterns=[
    path('add',views.AddUser.as_view()),
    path('sms/code',views.sms_send),
    path('<str:username>/address',views.AddressView.as_view()),
    path('<str:username>/address/<int:address_id>',views.AddressView.as_view()),
    path('<str:username>/address/default',views.AddressDefaultView.as_view()),
    path('password/sms', views.sms_send),
    path('password/verification', views.verification),
    path('password/new', views.findpass),
    path('<str:username>/password', views.ChangePwd.as_view()),
]