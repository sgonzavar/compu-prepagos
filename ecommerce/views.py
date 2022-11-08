from django.shortcuts import render
from .models import Category, Product
from django.contrib import messages

def index(request):
  template_name = 'templates/index.html'
  categories = Category.objects.filter(active=True)
  products = Product.objects.filter(active=True)
  context = {'products': products, 'categories': categories}
  return render(request, "index.html", context)

def search_category(request, slug):
  template_name = 'list.html'
  cat = Category.objects.get(slug=slug)
  categories = Category.objects.filter(active=True)
  products = Product.objects.filter(active=True, category=cat)
  context = {'products': products, 'categories': categories}
  return render(request, template_name, context)

def search(request):
  template_name = 'list.html'
  input = request.GET.get['input']
  products = Product.objects.filter(active=True, name__icontains=input)
  categories = Category.objects.filter(active=True)
  context = {'products': products, 'categories': categories}
  return render(request, template_name, context)

def detail(request, slug):
  if Product.objects.filter(active=True, slug=slug).exists():
    template_name = 'datail.html'
    products = Product.objects.filter(active=True, slug=slug)
    categories = Category.objects.filter(active=True)
    context = {'products': products, 'categories': categories}
    return render(request, template_name, context)

  
def cart(request, slug):
  product = Product.objects.get(slug=slug)
  initial = {'items':[], 'price': 0.0, 'count':0}
  session = request.session.get('data', initial)
  if slug in session['items']:
    messages.error(request, 'Producto ya existe en el carro de compras')
  else:
    session['items'].append(slug)
    session['price'] += float(product.price)
    session['count'] += 1
    request.session['data'] = session
    messages.succes(request, 'Agregado con exito')
  return redirect('ecommmerce:detail', slug=slug)

def mycart(request):
  template_name = 'list.html'
  session = request.session.get('data', {'items':[]})
  products = Product.objects.filter(active=True, slug__in=session['items'])
  categories = Category.objects.filter(active=True)
  context = {'products': products, 'categories': categories}
  return render(request, template_name, context)

