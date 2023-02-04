from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.utils.encoding import escape_uri_path
from .models import Account
from .models import Mail

#Fix to flaw 1:
#def tranferView(request):
#	if request.method == "POST":
#   	sender = request.user
#		to = User.objects.get(username=request.POST.get('to'))
#		amount = int(request.POST.get('amount'))
#		transfer(sender,to,amount)
#	return redirect('/')

#Fix to flaw 2:
#replace content in mailview with:
#content = escape_uri_path(request.POST.get('content'))
#escape_uri_path is builtin function that django provides for sanitizing user input

#Fix to flaw 3:
#By adding validation and verification to the transferview function so only logged in users can transfer money from their account
#replace row 59 with 
#if sender.id != request.user.id:
#	 return redirect('/')


def transfer(sender, receiver, amount):
	with transaction.atomic():
		
			if sender == receiver:
				pass

			acc1 = Account.objects.get(user=sender)
			acc2 = Account.objects.get(user=receiver)
			one = (f"{acc1.balance} - {amount}")
			two = (f"{acc2.balance} + {amount}")

			acc1.balance = eval(one)
			acc2.balance = eval(two)
		
	acc1.save()
	acc2.save()
	


@login_required
def transferView(request):
	if request.method == 'GET':
		try:
			sender = User.objects.get(username=request.GET.get('from'))
			to = User.objects.get(username=request.GET.get('to'))
			amount = request.GET.get('amount')
			
			transfer(sender,to,amount)
		except (ValueError,NameError,SyntaxError):
			print("ERROR")
			return redirect('/error/')
	return redirect('/')

@login_required
def mailView(request):
	target = User.objects.get(username=request.POST.get('to'))
	content = request.POST.get('content')
	Mail.objects.create(source=request.user, target=target, content=content)
	return redirect('/')

def errorView(request):
	return render(request, 'pages/error.html')

@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	mails = Mail.objects.filter(Q(source=request.user) |Q(target=request.user))
	return render(request, 'pages/index.html', {'mails': mails, 'accounts': accounts})
