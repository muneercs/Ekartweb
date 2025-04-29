from django.shortcuts import render
from . models import Product
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    featured_products=Product.objects.order_by('priority')[:4]
    latest_products=Product.objects.order_by('-id')[:4]
    context={
        'featured_products':featured_products,
        'latest_products':latest_products
    }
    
    return render(request,'index.html',context)

def list_products(request):
    """_summary_
    returns product list page

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """    
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    Product_list=Product.objects.order_by('-priority')
    product_paginator=Paginator(Product_list,2)
    Product_list=product_paginator.get_page(page)
    context = {'Products': Product_list}
    return render(request,'products.html',context)



def detail_product(request,pk):
    products=Product.objects.get(pk=pk)
    context={'Product':products}
    
    return render(request,'product_detail.html',context)