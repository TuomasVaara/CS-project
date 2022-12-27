from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from .models import Account
from .models import Mail

def transfer(sender, receiver, amount):
	with transaction.atomic():
		if sender == receiver:
			pass

		acc1 = Account.objects.get(user=sender)
		acc2 = Account.objects.get(user=receiver)

		if acc1.balance >= amount and amount > 0:
			acc1.balance -= amount
			acc2.balance += amount

	acc1.save()
	acc2.save()



@login_required
#Tänne muutettiin POST -> GET 
# JES NYT KAVERIT VOIDAAN RYÖSTÄÄ!!!
def transferView(request):
	if request.method == 'GET':
		sender = request.user
		to = User.objects.get(username=request.GET.get('to'))
		amount = int(request.GET.get('amount'))
		transfer(sender,to,amount)
		
	return redirect('/')

@login_required
def mailView(request):
	target = User.objects.get(username=request.POST.get('to'))
	Mail.objects.create(source=request.user, target=target, content=request.POST.get('content'))
	return redirect('/')

@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	mails = Mail.objects.filter(Q(source=request.user) |Q(target=request.user))
	return render(request, 'pages/index.html', {'mails': mails, 'accounts': accounts})
