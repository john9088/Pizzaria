from django.db import models

# Create your models here.
class PizzaModel(models.Model):
	name = models.CharField(max_length = 10)
	price = models.CharField(max_length = 10)

class CustomerModel(models.Model):
	userid = models.CharField(max_length = 10)
	userphoneno = models.CharField(max_length = 10)

class CustomerOrder(models.Model):
	username = models.CharField(max_length = 10)
	phoneno = models.CharField(max_length = 10)
	address = models.CharField(max_length = 25)
	order =  models.CharField(max_length = 30)
	totalcost =  models.CharField(max_length = 10)
	status = models.CharField(max_length = 10)