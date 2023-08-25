from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart, Order, OrderItem, Profile
import random
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
# from store.views import productview



@login_required(login_url='loginpage')
def index(request):
    rowcart = Cart.objects.filter(user=request.user)
    for item in rowcart:
        if item.product_qty > item.product.quantity :
            Cart.objects.delete(id=item.id)
    
    cartitems = Cart.objects.filter(user=request.user)
    total_price =  0

    for item in cartitems:
        if item.product.selling_price:
            total_price = total_price + item.product.selling_price * item.product_qty
        if item.product.dozon_price:
            total_price = total_price + item.product.dozon_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()


    context = {'cartitems':cartitems, 'total_price':total_price, 'userprofile':userprofile}
    return render(request, "store/checkout.html",  context)

@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == "POST":

        currentuser = User.objects.filter(id=request.user.id).first()
        

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()


        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()


        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        
        neworder.payment_mode = request.POST.get('payment_mode')
        
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        
        for item in cart:
            if item.product.selling_price:
                cart_total_price = cart_total_price + item.product.selling_price * item.product_qty
            if item.product.dozon_price:
                cart_total_price = cart_total_price + item.product.dozon_price * item.product_qty

        neworder.total_price = cart_total_price
        trackno ='Order_No'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'Order_No'+str(random.randint(1111111,9999999))
        
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.selling_price + item.product.dozon_price,
                quantity = item.product_qty,

            )
        #To Decrease the product quantity from available stock 
        orderproduct = Product.objects.filter(id=item.product_id).first()
        orderproduct.quantity = orderproduct.quantity - item.product_qty
        orderproduct.save()

            #To clear users cart
        Cart.objects.filter(user=request.user).delete()


        payMode= request.POST.get('payment_mode')
        if (payMode == "Paid by Online"):
            return JsonResponse({'status': "Your Order has been palced successfully!"})
        else:
            messages.success(request, "Your order has been placed succefully!")
    return redirect("/my-orders")

@login_required(login_url='loginpage')
def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        if item.product.selling_price:
            total_price = total_price + item.product.selling_price * item.product_qty
        if item.product.dozon_price:
            total_price = total_price + item.product.dozon_price * item.product_qty

    return JsonResponse({
        "total_price": total_price
    })

def orders(request):
    return HttpResponse('my ordder page')
