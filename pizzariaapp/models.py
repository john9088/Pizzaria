from django.db import models

# Create your models here.
class PizzaModel(models.Model):
	name = models.CharField(max_length = 10)
	price = models.CharField(max_length = 10)

class CustomerModel(models.Model):
	userid = models.CharField(max_length = 10)
	userphoneno = models.CharField(max_length = 10)