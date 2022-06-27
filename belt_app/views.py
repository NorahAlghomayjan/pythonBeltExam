from multiprocessing import context
from urllib import request
from django.urls import reverse
from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User,Item
import bcrypt
from datetime import datetime,timedelta
import pytz
# from django.http import HttpResponseRedirect

# 
def index(request):
    try:
        id = request.session['userId']  
        return redirect('/dashboard') 
    except:
        return redirect('/main')

# main
def main(request):
    return render(request,'register&login.html')

# dashboard
def dashboard(request):
    try:
        id = request.session['userId']  
    except:
        return redirect('/')
    user = User.objects.filter(id=id).first()
    items = Item.objects.all().exclude(users__in=[user])
    context = {
        'user': user,
        'items' : items
    }
    return render(request,'dashboard.html',context)

# register
def register(request):
    #check if it post..
    if request.method != 'POST':
        return redirect ('/main')
    
    #check if its valid..
    errors = User.objects.validRegister(request.POST)
    if(len(errors)>0):
        for key, value in errors.items():
            messages.error(request, value, 'alert alert-danger')
            print('--'*80,'Not registered')
        return redirect('/')
        
    #gather info from post..
    name = request.POST.get('name')
    username = request.POST.get('username')
    user_pw = request.POST.get('pw')
    date_hired = request.POST.get('date')
    if not(date_hired):
        date_hired = pytz.utc.localize(datetime.utcnow())

    #hashing pasword..
    pw_hash = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
    

    #create new user..
    User.objects.create(name=name,username=username,password=pw_hash,date_hired=date_hired)
    id = User.objects.last().id
    messages.success(request, "registered succefully", 'alert alert-success')
    return redirect(f'/saveUser/{id}')

# login
def login(request):
    #checking if the request is post.
    if request.method != 'POST':
        return redirect('/')

    #matching user-inputs with the what stored in db.
    errors = User.objects.validLogin(request.POST)
    if (len(errors)>0):
        for key, value in errors.items():
            messages.error(request, value, 'alert alert-danger')
        return redirect('/')

    #fetching for the id to redirect user to success page.
    id = User.objects.filter(username = request.POST['username'])[0].id
    messages.success(request, "logged-in succefully", 'alert alert-success')
    return redirect(f'/saveUser/{id}')


#saveUser/<int:id>
def saveUser(request,id):
    #keeping user logged in
    request.session['userId'] = id
    return redirect('/')


#logout/<int:id>
def logout (request,id):
    request.session.clear()
    list(messages.get_messages(request))
    messages.success(request, "You have been logged out!",'alert alert-success')
    return redirect('/')

#wish_items/create
def create(request):
    context = {
        'userId' : request.session['userId']
    }
    return render(request,'new_item.html',context)

#addItem/<int:id>
def addItem (request,id):
    if request.method != 'POST':
        return redirect ('/main')

    errors = Item.objects.validItem(request.POST)
    if(len(errors)>0):
        for key, value in errors.items():
            messages.error(request, value, 'alert alert-danger')
        return redirect('/wish_items/create')

    user = User.objects.filter(id=id).first()
    item_name = request.POST.get('item_name')
    print('item_name')
    item = Item.objects.create(name=item_name,user=user)
    item.save()
    user.wishlist.add(item)
    return redirect('/dashboard')

#deleteItem/<int:id>
def deleteItem(request,id):
    item = Item.objects.filter(id=id).first()
    item.delete()
    return redirect ('/dashboard')

#removeItem/<int:id>
def removeItem(request,id):
    item = Item.objects.filter(id=id).first()
    userId = request.session['userId']
    user = User.objects.filter(id=userId).first()
    user.wishlist.remove(item)
    return redirect ('/dashboard')

#addtoWishList/<int:itemId>
def addtoWishList(request,itemId):
    userId = request.session['userId']
    user = User.objects.filter(id=userId).first()
    item = Item.objects.filter(id=itemId).first()
    user.wishlist.add(item)
    return redirect ('/dashboard')

#wish_items/<int:itemId>
def item(request,itemId):
    userId = request.session['userId']
    item = Item.objects.filter(id=itemId).first()
    context = {
        'item' : item,
        'userId':userId
    }
    return render(request,'item.html',context)


