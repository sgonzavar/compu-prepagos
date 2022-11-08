from django.db import models
from autoslug import AutoSlugField

class Category(models.Model):
  name = models.CharField(max_length=225)
  slug = AutoSlugField(populate_from='name')
  active=models.BooleanField(default=True)

  def __str__(self) -> str:
      return self.name
  
  class Meta:
    verbose_name_plural='Category'

class Product(models.Model):
  # code=models.CharField(max_length=10, primary_key=True, db_index=True)
  name = models.CharField(max_length=225)
  image = models.CharField(max_length=500)
  slug = AutoSlugField(populate_from='name')
  mark = models.CharField(max_length=225)
  description = models.TextField(blank=True, null=True)
  price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  leading = models.BooleanField(default=True)
  active = models.BooleanField(default=True)

  def __str__(self) -> str:
    return self.name

  class Meta:
    verbose_name_plural= 'Product'