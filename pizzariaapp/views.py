from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
# Create your views here.


def homePageView(request):
	return render(request,"pizzariaapp/homePageView.html")


def adminLoginView(request):
	return render(request,"pizzariaapp/adminLogin.html")

def authenticateAdmin(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username, password = password)
	if (user is not None) and (username == 'johnj'):
		login(request,user)
		return redirect('adminhomepage')

	else:
		messages.add_message(request,messages.ERROR,"Invalid Credential")
		return redirect('adminloginpage')

def adminHomePageView(request):
	pizzas = PizzaModel.objects.all()
	context = {'pizzas':pizzas}
	return render(request,"pizzariaapp/adminHomePage.html",context)

def logoutAdmin(request):
	logout(request)
	return redirect('adminloginpage')

def addAdminPizza(request):
	pizzaName = request.POST['pizza']
	pizzaPrice = request.POST['price']
	PizzaModel(name = pizzaName, price = pizzaPrice).save()
	return redirect('adminhomepage')

def deleteAdminPizza(request,pizzaid):
	PizzaModel.objects.filter(id = pizzaid).delete()
	return redirect('adminhomepage')

def signupUser(request):
	userName = request.POST['username']
	userPassword = request.POST['userpassword']
	userPhno = request.POST['phoneno']
	useremail = request.POST['useremail']

	if User.objects.filter(username = userName).exists():
		messages.add_message(request,messages.ERROR,"User Already Exist")
		return redirect('homepageview')
	else:
		User.objects.create_user(username = userName, password = userPassword, email = useremail).save()
		userlen = len(User.objects.all()) - 1
		CustomerModel(userid = User.objects.all()[int(userlen)].id,userphoneno = userPhno).save()
		messages.add_message(request,messages.ERROR,"User Created Successfully")

		return redirect('homepageview')

def userLoginView(request):
	return render(request,'pizzariaapp/userloginview.html')

def authenticateUser(request):
	username = request.POST['username']
	password = request.POST['userpassword']
	user = authenticate(username = username, password = password)
	if (user is not None):
		login(request,user)
		return redirect('userwelcomepage')

	else:
		messages.add_message(request,messages.ERROR,"Invalid Credential")
		return redirect('userloginview')

def customerWelcomePage(request):
	if not request.user.is_authenticated:
		return redirect('userloginview')

	username = request.user.username
	pizzas = PizzaModel.objects.all()
	context = {'username':username,'pizzas':pizzas}
	return render(request,'pizzariaapp/welcomeuser.html',context)

def placeOrder(request):
	if not request.user.is_authenticated:
		return redirect('userloginview')

	username = request.user.username
	phoneno = CustomerModel.objects.filter(userid = request.user.id)[0].userphoneno
	address = request.POST['address']
	ordereditems = ''
	totalcost = '0'
	
	
	for pizza in PizzaModel.objects.all():
		pizzaid = pizza.id
		pizzaname = pizza.name
		pizzaprice = pizza.price
		pizzaqty = request.POST.get(str(pizzaid),'')

		if((pizzaqty is not None) and (pizzaqty != '') and (pizzaqty != '0')):
			totalcost = str(int(totalcost) + int(pizzaprice)* int(pizzaqty))
			ordereditems = ordereditems + 'Name: '+str(pizzaname)+ '| Pizza Price: '+str(pizzaprice)+'| Pizza Quantity:'+str(pizzaqty)+','+'\n'

	if((totalcost is not None) and (totalcost != '0')):
		CustomerOrder(username = username,phoneno = str(phoneno),address=  str(address),order = ordereditems,totalcost = totalcost,status = 'Pending').save()
		messages.add_message(request,messages.ERROR,"Order Placed")
	return redirect('userwelcomepage')

def showOrders(request):
	username = request.user.username
	orders = CustomerOrder.objects.filter(username = request.user.username)
	context = {'orders':orders,'username':username}
	return render(request,"pizzariaapp/showorders.html",context)

def logoutUser(request):
	print(request.user)
	logout(request)
	#return redirect('userwelcomepage')
	return redirect('homepageview')

def showOrdersAdmin(request):
	orders = CustomerOrder.objects.all()
	context = {'orders':orders}
	return render(request,'pizzariaapp/showadminorders.html',context)

def acceptOrder(request,orderid):
	order = CustomerOrder.objects.filter(id = orderid)[0]
	order.status = 'Accepted'
	order.save()
	return redirect(request.META['HTTP_REFERER'])

def rejectOrder(request,orderid):
	order = CustomerOrder.objects.filter(id = orderid)[0]
	order.status = 'Rejected'
	order.save()
	return redirect(request.META['HTTP_REFERER'])
