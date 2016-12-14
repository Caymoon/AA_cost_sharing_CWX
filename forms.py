# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 10:08:03 2016

@author: Wangzhpp
"""
from django import forms
 
class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()