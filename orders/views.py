from django.shortcuts import render,redirect
from django.http import HttpResponse
from products.models import Product
from django .contrib import messages
from . models import Order,OrderedItem
from customers.models import Customer,User
from django.contrib.auth.decorators import login_required



# Create your views here.
def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj,created=Order.objects.get_or_create(
        Owner=customer,
        order_status=Order.CART_STAGE
    )
    context={'cart':cart_obj}


    return render(request,'cart.html',context,)


def remove_item_from_cart(request,pk):


    item=OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart') 

def checkout_cart(request):
    if request.method == 'POST':
        user = request.user
        customer, created = Customer.objects.get_or_create(user=user)

        total = float(request.POST.get('total', 0))
        order_obj = Order.objects.filter(
            Owner=customer,
            order_status=Order.CART_STAGE
        ).first()

        if order_obj:
            order_obj.order_status = Order.ORDER_CONFIRMED
            order_obj.total_price = total
            order_obj.save()
            status_message = "Your order is processed. Your item will be delivered within 2 days."
            messages.success(request, status_message)
        else:
            status_message = "Unable to process order. No items in cart."
            messages.error(request, status_message)

    return redirect('cart')

@login_required(login_url='account')
def Show_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders=Order.objects.filter(Owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}

   

    return render(request,'orders.html',context,)

@login_required(login_url='account')
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user

        customer, created = Customer.objects.get_or_create(user=user)
        quantity = int(request.POST.get('quantity', 1))
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return redirect('cart')  

        cart_obj, created = Order.objects.get_or_create(
            Owner=customer,
            order_status=Order.CART_STAGE
        )
        ordered_item, created = OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj
        )
        if created:
            ordered_item.quantity = quantity
        else:
            ordered_item.quantity += quantity
        ordered_item.save()

    return redirect('cart')          




            












