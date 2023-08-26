from django.contrib import messages
from django.shortcuts import redirect, render
from store.models import Product,Cart,Order,OrderItem
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required


def index(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request, "store/orders/index.html", context)

def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderitems}
    return render(request, "store/orders/view.html", context)
