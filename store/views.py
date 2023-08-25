
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    products = Product.objects.filter(offeres=1)
    context = ({'products':products})
    return render(request, "store/index.html", context)

def collections(request):
    category=Category.objects.filter()
    context=({'category':category})
    return render(request, "store/collections.html", context)


def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug)):
        products=Product.objects.filter(category__slug=slug)
        category= Category.objects.filter(slug=slug).first()
        context={'products': products , 'category':category}
        return render(request, "store/products/index.html", context)
    else:
        messages.warning(request, "No such cetgory found")
        return redirect('index')
    
def productview(request,cate_slug, prod_slug):
    if (Category.objects.filter(slug=cate_slug)):
        if (Product.objects.filter(slug=prod_slug)):
            products= Product.objects.filter(slug=prod_slug).first
            context ={'products': products}
        else:
            messages.error(request, "No such product found")
            return redirect('collections')


    else:
        messages.error(request, "No such category found")
        return redirect('collections')
    
    return render(request, "store/products/view.html", context)


def productlistajax(request):
    products =Product.objects.filter().values_list('name', flat=True)
    productlist = list(products)

    return JsonResponse(productlist, safe=False)
def categorylistajax(request):
    category =Product.objects.filter().values_list('name',flat=True)

    categorylist =list(category)

    return JsonResponse(categorylist, safe=False)
@login_required(login_url='loginpage')
def searchproducts(request):
    if request.method == "POST":
        search = request.POST.get('searchproduct')
        if search =="":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product =Product.objects.filter(name__icontains=search).first()
            category =Category.objects.filter(name__icontains=search).first()
            if product:
                return redirect("collections/"+product.category.slug+'/'+product.slug)
            elif category:
                return redirect("collections/"+category.slug)
            else:
                messages.info(request,"No product match your search")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))