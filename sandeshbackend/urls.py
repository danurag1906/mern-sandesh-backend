"""sandeshbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# urls.py

from django.urls import path
from myapp.views import signup, signin, create_bill, get_all_bills, get_bill_by_id, update_bill, delete_bill,test

urlpatterns = [
    path('api/signup', signup),
    path('api/signin', signin),
    path('api/createBill', create_bill),
    path('api/getAllBills', get_all_bills),
    path('api/getBillById/<str:id>', get_bill_by_id),
    path('api/updateBill/<str:id>', update_bill),
    path('api/deleteBill/<str:id>', delete_bill),
    path('api/test/', test),

]

