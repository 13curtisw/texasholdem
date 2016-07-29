

# def index(request):
# 	return render(request,'pokerapp/index.html')
# def table(request):
# 	return render(request, 'pokerapp/table.html')
from django.shortcuts import render, redirect
from .models import User,Table
from django.core.urlresolvers import reverse
import re
import bcrypt
# Create your views here.

def index(request):
    context = {
     "users" : User.objects.all()
    }
    request.session['loggedin']=False
    return render(request, 'pokerapp/index.html', context)


# def hashit(password):
#     hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     return hashed
def create(request):
    # if validate(request):
    User.objects.create(name=request.POST['name'],username=request.POST['username'],password=request.POST['password'], balance=100, picture="poker/img/superheroes" + request.POST['picture'] + ".png")
    #     return redirect('/')
    # else:
    #     print "invalid"
    return redirect('/')

def login(request):


    if request.session['loggedin'] == True:
        user = User.objects.get(id=request.session['user'])
        context={
            'users' : user,
            'tables' : Table.objects.all()


        }

        return render(request, 'pokerapp/mainpage.html', context)
    else:
        if len(User.objects.filter(username=request.POST['username']))==0:
            return render(request,'pokerapp/index.html')
        else:
            user = User.objects.get(username=request.POST['username'])
            password = request.POST['password']
            ##make Session for user

            ##Hash
            # hashed = user.password
            # if bcrypt.hashpw(password.encode("utf-8"), hashed.encode()) == hashed.encode():
            if user.password == password:
                request.session['user']=user.id
                context={
                    'users' : user,
                    'tables' : Table.objects.all(),

                }
                request.session['loggedin']=True
                return render(request, 'pokerapp/mainpage.html', context)


def addtable (request):
    table = Table.objects.create()
    table.currentplayer=0
    table.save()
    user = User.objects.get(id=request.session['user'])
    return redirect(reverse('my_join', args=[table.id]))
    # user = User.objects.get(id=request.session['user'])
    # user.table=table
    # user.save()

    # context={
    # 'user' : user
    # }
    # return render(request,'pokerapp/ingame.html',context)
# def submittravel(request):
#     user=User.objects.get(id=request.session['user'])
#     Trip.objects.create(destination=request.POST['destination'],description=request.POST['description'],travel_from=request.POST['travel_from'],travel_to=request.POST['travel_to'],user=user)
#
#     return redirect(reverse("my_home"))
def profile (request,id):

    user=User.objects.get(id=id)
    ##person going to

    context = {
        "user":user
    }
    return render(request, 'pokerapp/viewprofile.html', context)

def join (request):
    user=User.objects.get(id=request.session['user'])
    # table=Table.objects.get(id=id)
    # if not user.table == table:
	   #  user.table=table
	   #  user.save()
	   #  table.currentplayer += 1
	   #  table.save()
    context={
    "user":user
    }
    return render(request,'pokerapp/ingame.html',context)

def logout (request):
    request.session.pop('user')
    request.session['loggedin'] = False
    return redirect('/')
def leave(request):
    # user=User.objects.get(id=request.session['user'])
    # user.table.currentplayer -= 1
    # user.table.save()
    # if(user.table.currentplayer ==0):
    #     print "hello"
    #     table=Table.objects.get(id=user.table.id)
    #     print table
    #     table.delete()
    #     user.table.delete()
    # user.table= None

    # user.save()

    return redirect('/main')

def addplayer(request):
	print request

def edit(request):
	context={
	'user' : User.objects.get(id = request.session['user'])
	}
	return render(request,'pokerapp/edit.html',context)
def update(request):
	user = User.objects.get(id=request.session['user'])
	user.name = request.POST['name']
	user.username = request.POST['username']
	user.picture = "poker/img/superheroes" + request.POST['picture'] + ".png"
	user.save()
	return redirect(reverse('my_profile', args=[user.id]))

def leaderboard(request):
   user = User.objects.all().order_by('balance').reverse()
   context={
   'users':user
   }
   return render(request,'pokerapp/leaderboard.html',context)



