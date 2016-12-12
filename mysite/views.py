# -*- coding: utf-8 -*-

# from django.template.loader import get_template
# from django.template import Context
from django.http import Http404, HttpResponse
from django.shortcuts import render
import datetime
import sqlite3


def hello(request):
    return HttpResponse('Hello, World !')
    
def my_homepage(request):
    return HttpResponse("It's the Home Page !")

'''
# version 1    
def current_datetime(request):
    now = datetime.datetime.now()
    # html = "<html><body>It's %s.</body></html>" % now
    t = get_template('datetime.html')
    # html = t.render(Context({'datetime':now}))
    html = t.render({'datetime':now})
    return HttpResponse(html)
'''

'''
# version 2
def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'datetime.html', {'datetime':now})
'''
    
# version 3
def current_datetime(request):
    time = datetime.datetime.now()
    return render(request, 'datetime.html', locals())

'''
# version 1    
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
'''

# version 2    
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
    base = 'base.html'
    return render(request, 'hours_ahead.html', locals())
    
def book_list(request):
    mydb = sqlite3.connect(user='', db='D:/Django/djcode/mysite/mydb.sqlite3', passwd='', host='')
    cursor = mydb.cursor()
    cursor.execute('SELECT name FROM books ORDER BY name')
    names = [row[0] for row in cursor.fetchall()]
    mydb.close()
    return render(request, 'book.html', locals())
    
    
    

