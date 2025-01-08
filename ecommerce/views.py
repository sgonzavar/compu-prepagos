from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import json, random, requests


def index(request):
    template_name = 'index.html'
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True)
    context = {'products': products, 'categories': categories}
    return render(request, template_name, context)


def search_category(request, slug):
    request.session['paypal'] = True
    template_name = 'list.html'
    cat = Category.objects.get(slug=slug)
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True, category=cat)
    context = {'products': products, 'categories': categories}
    return render(request, template_name, context)


def search(request):
    request.session['paypal'] = True
    template_name = 'list.html'
    input = request.GET['input']
    products = Product.objects.filter(active=True, name__icontains=input)
    categories = Category.objects.filter(active=True)
    context = {'products': products, 'categories': categories}
    return render(request, template_name, context)


def detail(request, slug):
    if Product.objects.filter(active=True, slug=slug).exists():
        template_name = 'detail.html'
        products = Product.objects.filter(active=True, slug=slug)
        categories = Category.objects.filter(active=True)
        context = {'products': products, 'categories': categories}
        return render(request, template_name, context)


def cart(request, slug):

    product = Product.objects.get(slug=slug)
    initial = {'items': [], 'price': 0.0, 'count': 0}
    session = request.session.get('data', initial)
    if slug in session['items']:
        messages.error(request, 'Producto ya existe en el carro de compras')
    else:
        session['items'].append(slug)
        session['price'] += float(product.price)
        session['count'] += 1
        request.session['data'] = session
        messages.success(request, 'Agregado con exito')
    return redirect('ecommerce:detail', slug)


def mycar(request):
    template_name = 'list.html'
    request.session['paypal'] = False
    session = request.session.get('data', {'items': []})
    products = Product.objects.filter(active=True, slug__in=session['items'])
    categories = Category.objects.filter(active=True)
    total = session['price']
    context = {'products': products, 'categories': categories, 'total': total}
    return render(request, template_name, context)


def checkout(request):
    template_name = 'checkout.html'
    return render(request, template_name)


def paymentComplete(request):
    body = json.loads(request.body)
    session = request.session.get('data',{'items':[]})
    car_product = session['items']
    order_pay = Order()
    order_pay.customer = body['customer']
    order_pay.orderNum = random.randint(10000,99999)
    order_pay.save()

    for item in car_product:
        product = Product.objects.get(slug=item)
        order_det = Order_Details()
        order_det.product = product
        order_det.amount = 1
        order_det.order = order_pay
        order_det.save()
    del request.session['data']
    return redirect('ecommerce:success')


def success(request):
    template_name = 'success.html'
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True)
    context = {'products': products, 'categories': categories}
    return render(request, template_name, context)
