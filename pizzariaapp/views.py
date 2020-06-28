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
	userName = request.POST['username']
	userPassword = request.POST['userpassword']

	if User.objects.filter(username = userName).exists():
		return redirect('userwelcomepage')
	else:
		messages.add_message(request,messages.ERROR,"Invalid Credentials")
		return redirect('userloginview')

def customerWelcomePage(request):
	return render(request,'pizzariaapp/welcomeuser.html')

def logoutUser(request):
	logout(request)
	return redirect('homepageview')