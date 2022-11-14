from django.urls import path
from .views import *

app_name = 'ecommerce'

urlpatterns = [
  path('', index, name='index'),
  path('categories/<slug>', search_category, name='categories'),
  path('search', search, name='search'),
  path('detail/<slug>', detail, name='detail'),
  path('<slug>/cart', cart, name='cart'),
  path('mycar/', mycar, name='mycar'),
  # path('checkout/', checkout, name='checkout'),
  path('success/', success, name='success'),
  path('complete/', paymentComplete, name='complete'),

]