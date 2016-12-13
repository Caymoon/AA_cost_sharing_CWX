#coding:utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from .forms import AddForm
from models import User
from models import Act
from django import forms
import math
# Create your views here.

class UserForm(forms.Form):
    username1 = forms.CharField(label='username',max_length=15)
    nickname1 = forms.CharField(label='nickname',max_length=15)    
    password1 = forms.CharField(label='password',widget=forms.PasswordInput())  
    age1      = forms.IntegerField(label='age')
    sexChoices=((True,'Man'),(False,'Woman'))
    sex      = forms.ChoiceField(choices=sexChoices,label='sex')    

class LoginForm(forms.Form):
    username = forms.CharField(label='username',max_length=15)
    password = forms.CharField(label='password',widget=forms.PasswordInput())  

class CreateForm(forms.Form):
    actname = forms.CharField(label='actname',max_length=15)
    #actdate = forms.DateField(label='actdate')
    actdate = forms.DateField(label='Date(mm/dd/yy)')
    location= forms.CharField(label='location',max_length=100)
    beforeChoices=((True,'Yes'),(False,'No'))
    before  = forms.ChoiceField(choices=beforeChoices,label='before')
    budget  = forms.FloatField(label='budget')
    cost    = forms.FloatField(label='cost')


def login(request):
    username = request.COOKIES.get('username','')
    if username:
        return HttpResponseRedirect('/online/userinfo/')
    if request.method =='POST':
        lf = LoginForm(request.POST)
        uf = UserForm(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                response = HttpResponseRedirect('/online/userinfo_new/')
                response.set_cookie('username',username,36000)
                return response
            else:
                return HttpResponseRedirect('/online/login/')
        if uf.is_valid():
            username = uf.cleaned_data['username1']
            nickname = uf.cleaned_data['nickname1']
            password = uf.cleaned_data['password1']
            age      = uf.cleaned_data['age1']
            sex      = uf.cleaned_data['sex']
            user     = User.objects.filter(username=username)
            if len(user)>0:
                return HttpResponse('Regist failed --- User name has already been used.')
            User.objects.create(username=username,nickname=nickname,password=password,age=age,sex=sex)
            response = HttpResponseRedirect('/online/userinfo_new/')
            response.set_cookie('username',username,36000)
            return response
    else:
        lf = LoginForm()
        uf = UserForm()
    return render_to_response('login.html',{'lf':lf,'uf':uf})
    
'''def index(request):
    username = request.COOKIES.get('username','')
    return render_to_response('index.html',{'username':username})'''
def index(request):
    return render_to_response('index.html')
    
def logout(request):
    response = HttpResponseRedirect('/online/login/')
    response.delete_cookie('username')
    return response
        
def userinfo(request):
    username = request.COOKIES.get('username','')
    p = User.objects.get(username = username)
    nickname = p.nickname
    age      = p.age
    sex      = p.sex

    if sex:
        sexot = 'Man'
    else:
        sexot = 'Woman'
    acts     = {}
    for act in p.act_set.all():
        acts[act.id] = act.actname
    ud={'username':username,'nickname':nickname,'age':age,'sex':sexot}
    
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
            actnow=Act.objects.create(actname=actname,actdate=actdate,location=location,before=before,budget=budget,cost=cost,owner=nowID)
            actnow.partner.add(nowuser)            
            return HttpResponseRedirect('/online/userinfo/')
    else:
        cf = CreateForm()    
    
    return render_to_response('userinfo.html',{'ud':ud,'username':username,'acts':acts,'nickname':nickname,'cf':cf})
    
def actinfo(request,actid):
    username = request.COOKIES.get('username','')
    nowuser  = User.objects.get(username=username)
    now      = Act.objects.filter(id=actid)
    if len(now)!=0:
        actname = now[0].actname
        actdate = now[0].actdate
        location= now[0].location
        brefore = now[0].before
        budget  = now[0].budget
        cost    = now[0].cost
        recive  = now[0].recive
        owner   = now[0].owner
        able    = now[0].able
        partner = {}
        u       = User.objects.get(id=owner)
        alluser = User.objects.all()
        nu      = []
        flag    = nowuser in now[0].accept.all()
        num1    = len(now[0].partner.all())
        num2    = len(now[0].accept.all())
        num3    = num1-num2
        fflag   = (num1*3 <= num2*4)

        for user in now[0].partner.all():
            if user.id == u.id: partner[user.id]=user.username+" (Owner)"
            else: partner[user.id]=user.username
        for user in alluser:
            if not user in now[0].partner.all():
                nu.append(user)
        if request.method == 'POST':
           # return HttpResponse('Create Action success.')
            for key,value in request.POST.items():
                if key == 'yes':
                    now[0].able = False
                    now[0].save()
                    return HttpResponseRedirect('/online/actinfo/'+actid)

                if key == 'exit':
                	now[0].partner.remove(nowuser)
                	now[0].accept.remove(nowuser)
                	now[0].save()
                	return HttpResponseRedirect('/online/actinfo/'+actid)

                if key == 'join':
                	now[0].partner.add(nowuser)
                	now[0].save()
                	return HttpResponseRedirect('/online/actinfo/'+actid)

                if key == 'accept':
                	now[0].accept.add(nowuser)
                	now[0].save()
                	return HttpResponseRedirect('/online/actinfo/'+actid)

                if key == 'refuse':
                	now[0].accept.remove(nowuser)
                	now[0].save()
                	return HttpResponseRedirect('/online/actinfo/'+actid)

                s = User.objects.get(id=key)
                if s in nu : now[0].partner.add(s)
                else:  
                	now[0].partner.remove(s)
                	now[0].accept.remove(s)
            now[0].save()
            return HttpResponseRedirect('/online/actinfo/'+actid)
        nd=budget-recive
        pnd=nd/len(partner)
        return render_to_response('actinfo.html',{'pnd':pnd,'actname':actname,'actdate':actdate,'able':able,'partner':partner,\
        	'u':u,'username':username,'nu':nu,'owner':owner,'budget':budget,'location':location,'recive':recive,'nd':nd,\
        	'cost':cost,'now':now,'nowuser':nowuser,'flag':flag,'fflag':fflag,'num1':num1,'num2':num2,'num3':num3})
    return HttpResponse('Wrong Action ID!')



def userinfo_new(request):
    username = request.COOKIES.get('username','')
    q_id = request.GET.get('q')
    if(q_id != None):
        return HttpResponseRedirect('/online/actinfo_new/'+ q_id)

    p = User.objects.get(username = username)
    nickname = p.nickname
    age      = p.age
    sex      = p.sex

    if sex:
        sexot = 'Man'
    else:
        sexot = 'Woman'
    acts     = {}
    for act in p.act_set.all():
        acts[act.id] = act.actname
    ud={'username':username,'nickname':nickname,'age':age,'sex':sexot}
    
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
            actnow=Act.objects.create(actname=actname,actdate=actdate,location=location,before=before,budget=budget,cost=cost,owner=nowID)
            actnow.partner.add(nowuser)            
            return HttpResponseRedirect('/online/userinfo_new/')
    else:
        cf = CreateForm()    
    acts_id=acts.keys()
    acts_id.sort()
    acts_list=[]
    cost=0.0
    for i in acts_id:
        act_now=Act.objects.get(id=i)
        owner_name=User.objects.get(id=act_now.owner).username
        acts_list.append( (i,act_now.actname,owner_name,act_now.actdate,act_now.able) )
        pnum=len(act_now.partner.all())
        if not act_now.able:
            cost=cost+act_now.cost/pnum
    acts_num=len(acts_list)
    cost=round(cost,2)
    return render_to_response('userinfo_new.html',{'q_id':q_id,'cost':cost,'ud':ud,'username':username,'acts':acts_list,'nickname':nickname,'cf':cf,'acts_id':acts_id,'acts_num':acts_num,'p':p,})


def actinfo_new(request,actid):
    username = request.COOKIES.get('username','')
    nowuser  = User.objects.get(username=username)
    now      = Act.objects.filter(id=actid)
    q_id = request.GET.get('q')
    if(q_id != None):
        return HttpResponseRedirect('/online/actinfo_new/'+ q_id)
    if len(now)!=0:
        actname = now[0].actname
        actdate = now[0].actdate
        location= now[0].location
        brefore = now[0].before
        budget  = now[0].budget
        cost    = now[0].cost
        recive  = now[0].recive
        owner   = now[0].owner
        able    = now[0].able
        partner = {}
        u       = User.objects.get(id=owner)
        alluser = User.objects.all()
        nu      = []
        flag    = nowuser in now[0].accept.all()
        num1    = len(now[0].partner.all())
        num2    = len(now[0].accept.all())
        num3    = num1-num2
        num4    = num1*3-num2*4
        num4    = int(math.ceil(num4/4.0))
        fflag   = (num1*3 <= num2*4)
        status  = now[0].status
        twp     = now[0].twp.all()
        tp_list = []
        fin     = now[0].fin.all()
        fin_list= []
        for i in twp:
            tp_list.append(i.id)
        for i in fin:
            fin_list.append(i.id)
        num5    =len(fin_list)
        for user in now[0].partner.all():
            if user.id == u.id: partner[user.id]=user.nickname
            else: partner[user.id]=user.nickname
        for user in alluser:
            if not user in now[0].partner.all():
                nu.append(user)
        if request.method == 'POST':
           # return HttpResponse('Create Action success.')
            for key,value in request.POST.items():
                if key == 'yes':
                    now[0].able = False
                    now[0].save()
                    return HttpResponseRedirect('/online/actinfo_new/'+actid)

                if key == 'exit':
                    now[0].partner.remove(nowuser)
                    now[0].accept.remove(nowuser)
                    now[0].save()
                    return HttpResponseRedirect('/online/actinfo_new/'+actid)

                if key == 'join':
                    now[0].partner.add(nowuser)
                    now[0].save()
                    return HttpResponseRedirect('/online/actinfo_new/'+actid)

                if key == 'accept':
                    now[0].accept.add(nowuser)
                    now[0].save()
                    return HttpResponseRedirect('/online/actinfo_new/'+actid)

                if key == 'refuse':
                    now[0].accept.remove(nowuser)
                    now[0].save()
                    return HttpResponseRedirect('/online/actinfo_new/'+actid)
                if key == 'pay':
                    now[0].fin.add(nowuser)
                    now[0].save()
                    return HttpResponseRedirect('/online/actinfo_new/'+actid)

                s = User.objects.get(id=key)
                if s in nu : now[0].partner.add(s)
                else:  
                    now[0].partner.remove(s)
                    now[0].accept.remove(s)
            now[0].save()
            return HttpResponseRedirect('/online/actinfo_new/'+actid)
        nd=budget-recive
        pnd=nd/len(partner)
        pnd=round(pnd,2)
        accept_list=[]
        aaname=''
        ma=0
        ma=max(now[0].p1,ma)
        ma=max(now[0].p2,ma)
        ma=max(now[0].p3,ma)
        ma=max(now[0].p4,ma)
        ma=max(now[0].p5,ma)
        if ma == now[0].p1:
            aaname='完全均摊的AA制'
        elif ma == now[0].p2:
            aaname='女生少付款哦'
        elif ma == now[0].p3:
            aaname='男生少付款哦'
        elif ma == now[0].p4:
            aaname='长者少付款吼'
        elif ma == now[0].p5:
            aaname='管理员制定AA方案'
        if status == 0 or status == 1:
            aaname='投票中……'

        if status == 0:
            jd='添加活动成员'
            jdn='20%'
        elif status == 1:
            jd='投票决定AA方案'
            jdn='40%'
        elif status == 2:
            jd='等待成员接受方案'
            jdn='60%'
        elif status == 3:
            jd='等待成员付款'
            jdn='80%'
        else:
            jd='活动已经结束啦～'
            jdn='100%'
        for i in now[0].accept.all():
            accept_list.append(i.id)
        nxtst=True
        if status == 2:
            nxtst=fflag
        if status == 3:
            nxtst=(num1 == num5)
        if status == 4:
            nxtst=False;
        return render_to_response('actinfo_new.html',{'num5':num5,'fin_list':fin_list,'nxtst':nxtst,'jdn':jdn,'jd':jd,'pnd':pnd,'actid':actid,'actname':actname,'actdate':actdate,'able':able,'partner':partner,\
            'u':u,'username':username,'nu':nu,'owner':owner,'budget':budget,'location':location,'recive':recive,'nd':nd,\
            'cost':cost,'now':now,'nowuser':nowuser,'flag':flag,'fflag':fflag,'num1':num1,'num2':num2,'num3':num3,'num4':num4,'q_id':q_id,'accept_list':accept_list,'status':status,'aaname':aaname,'twp_list':tp_list,})
    return HttpResponse('Wrong Action ID!')

def add_action(request):
    username = request.COOKIES.get('username','')
    nowuser  = User.objects.get(username=username)
    before   = request.POST["before"]
    tp       = request.POST["tp"]
    q_id = request.GET.get('q')
    if(q_id != None):
        return HttpResponseRedirect('/online/actinfo_new/'+ q_id)
    return render_to_response('add_action.html',{'before':before,'tp':tp,'p':nowuser,})

def add_action_f(request):
    username = request.COOKIES.get('username','')
    nowuser  = User.objects.get(username=username)
    nowID    = nowuser.id
    actname  = request.POST["actname"]
    actdate  = request.POST["actdate"]
    actlocate  = request.POST["actlocate"]
    actcost  = request.POST["actcost"]
    before   = request.POST["before"]
    tp       = request.POST["tp"]

    if before == '0' :

        actnow=Act.objects.create(actname=actname,actdate=actdate,location=actlocate,before=True,budget=actcost,cost=0,owner=nowID,tp=tp)
    else:
        actnow=Act.objects.create(actname=actname,actdate=actdate,location=actlocate,before=False,budget=0,cost=actcost,owner=nowID,tp=tp)
    actnow.partner.add(nowuser)  
    return HttpResponseRedirect('/online/userinfo_new/')

def tping(request):
    username = request.COOKIES.get('username','')
    nowuser  = User.objects.get(username=username)
    nowID    = nowuser.id
    tp       = request.POST["tp"]
    actid    = request.POST["actid"]
    act      = Act.objects.get(id=actid)
    act.twp.add(nowuser)
    if tp == '1':
        act.p1=act.p1+1
    elif tp == '2':
        act.p2=act.p2+1
    elif tp == '3':
        act.p3=act.p3+1
    elif tp == '4':
        act.p4=act.p4+1
    elif tp == '1':
        act.p5=act.p5+1
    act.save()
    return HttpResponseRedirect('/online/actinfo_new/'+actid)

def add_status(request):
    username = request.COOKIES.get('username','')
    nowuser  = User.objects.get(username=username)
    nowID    = nowuser.id
    actid    = request.POST["actid"]
    act      = Act.objects.get(id=actid)
    act.status=act.status+1
    act.save()
    return HttpResponseRedirect('/online/actinfo_new/'+actid)