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
        for i in now[0].accept.all():
            accept_list.append(i.id)
        return render_to_response('actinfo_new.html',{'pnd':pnd,'actname':actname,'actdate':actdate,'able':able,'partner':partner,\
            'u':u,'username':username,'nu':nu,'owner':owner,'budget':budget,'location':location,'recive':recive,'nd':nd,\
            'cost':cost,'now':now,'nowuser':nowuser,'flag':flag,'fflag':fflag,'num1':num1,'num2':num2,'num3':num3,'num4':num4,'q_id':q_id,'accept_list':accept_list,})
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

