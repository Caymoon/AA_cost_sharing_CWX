#coding:utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from .forms import AddForm
from models import User
from models import Act
from django import forms
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='username',max_length=15)
    nickname = forms.CharField(label='nickname',max_length=15)    
    password = forms.CharField(label='password',widget=forms.PasswordInput())  
    age      = forms.IntegerField(label='age')
    sexChoices=((True,'Man'),(False,'Woman'))
    sex      = forms.ChoiceField(choices=sexChoices,label='sex')    

class LoginForm(forms.Form):
    username = forms.CharField(label='username',max_length=15)
    password = forms.CharField(label='password',widget=forms.PasswordInput())  

class CreateForm(forms.Form):
    actname = forms.CharField(label='actname',max_length=15)
    actdate = forms.DateField(label='actdate')
    location= forms.CharField(label='location',max_length=100)
    before  = forms.BooleanField(label='before')
    budget  = forms.FloatField(label='budget')
    cost    = forms.FloatField(label='cost')

def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            nickname = uf.cleaned_data['nickname']
            password = uf.cleaned_data['password']
            age      = uf.cleaned_data['age']
            sex      = uf.cleaned_data['sex']
            User.objects.create(username=username,nickname=nickname,password=password,age=age,sex=sex)
            return HttpResponse('Regist success.')
    else:
        uf=UserForm()
    return render_to_response('regist.html',{'uf':uf})
    
def login(request):
    if request.method =='POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                response = HttpResponseRedirect('/online/index/')
                response.set_cookie('username',username,3600)
                return response
            else:
                return HttpResponseRedirect('/online/login/')
    else: lf = LoginForm()
    return render_to_response('login.html',{'lf':lf})
    
def index(request):
    username = request.COOKIES.get('username','')
    return render_to_response('index.html',{'username':username})
    
def logout(request):
    response = HttpResponse('logout')
    response.delete_cookie('username')
    return response
        
def userinfo(request):
    username = request.COOKIES.get('username','')
    p = User.objects.get(username = username)
    password = p.password
    nickname = p.nickname
    age      = p.age
    sex      = p.sex    
    ud={'username':username,'nickname':nickname,'password':password,'age':age,'sex':sex}
    return render_to_response('userinfo.html',{'ud':ud})

def createact(request):
    username = request.COOKIES.get('username','')
    nowuser  = User.objects.get(username=username)
    nowID    = nowuser.id
    if request.method == 'POST':
        cf = CreateForm(request.POST)
        if cf.is_valid():
            actname = cf.cleaned_data['actname']
            actdate = cf.cleaned_data['actdate']
            location= cf.cleaned_data['location']
            before  = cf.cleaned_data['before']
            budget  = cf.cleaned_data['budget']
            cost    = cf.cleaned_data['cost']
            Act.objects.create(actname=actname,actdate=actdate,location=location,before=before,budget=budget,cost=cost,owner=nowID,partner=nowuser,recive=0)
            return HttpResponse('Create Action success.')
    else:
        cf = CreateForm()
    return render_to_response('createact.html',{'cf':cf})
        
            
        
    