from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote, UserManager, QuoteManager
from django.contrib import messages
from django.db.models import Count 
import bcrypt

def index(request):
    return render(request, 'quotes/index.html')

def login(request):
    if User.objects.filter(email = request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            messages.success(request, "Successfully logged in!")
            return redirect('/quotes')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect ('/')
    else:
        messages.error(request, "Invalid email or password.")
        return redirect('/')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed)
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        messages.success(request, "Successfully registered!")
        return redirect('/quotes')

def quotes(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to view this page!")
        return redirect('/')
    
    context = {
        'first_name': request.session['first_name'],
        'last_name': request.session['last_name'],
        'user': User.objects.get(id=request.session['user_id']),
        'Quotes': Quote.objects.annotate(count_likes=Count('liked_users')),
        'Users': User.objects.all()
    }

    return render(request, 'quotes/quotes.html', context)

def like(request):
    if request.method == "POST":
        liked_users = Quote.objects.process_like(request.POST)
        return redirect('/quotes')

def delete(request):
    this_quote = Quote.objects.get(id=request.POST['quote_id'])
    this_quote.delete()
    return redirect('/quotes')

def add(request):
    errors = Quote.objects.quoteValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        quote = request.POST['quote']
        author = request.POST['author']
        id = request.session['user_id']
        user = User.objects.get(id=id)
        Quote.objects.create(quote = quote, author = author, uploader = user)

    return redirect('/quotes')

def logout(request):
    request.session.clear()
    messages.error(request, "Successfully logged out!")
    return redirect('/')

def show(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to view this page!")
        return redirect('/')

    context = {
        'id': id,
        'first_name': User.objects.get(id=id).first_name,
        'last_name': User.objects.get(id=id).last_name,
        'Users': User.objects.all(),
        'Quotes': Quote.objects.filter(uploader__id__contains=id)
    }

    return render(request, 'quotes/show.html', context)

def edit(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to view this page!")
        return redirect('/')

    context = {
        'id': request.session['user_id'],
        'first_name': User.objects.get(id=id).first_name,
        'last_name': User.objects.get(id=id).last_name,
        'email': User.objects.get(id=id).email,
    }

    return render(request, 'quotes/edit.html', context)

def update(request, id):
    user = User.objects.get(id=id)
    errors = User.objects.infoValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/myaccount/'+str(user.id))
    else:
        user = User.objects.get(id=id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.error(request, "Updated successfully!")
        return redirect('/myaccount/'+str(user.id))
