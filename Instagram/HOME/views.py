from typing import Any
from django.shortcuts import render
from . import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
# Create your views here.
class AppListView(ListView):
    def __init__(self):
        self.params = {
            "appname": models.APPLIST.objects.values_list('APPNAME', flat=True),
            "appurl": models.APPLIST.objects.values_list('APPURL', flat=True),
            # "APPLIST":[],
        }
        self.params['appname'] = list(self.params['appname'])
        self.params['appurl'] = list(self.params['appurl'])
        # self.params['APPLIST'] = []

    def get(self,request):
        # print(self.params['appname'])
        return render(request, 'HOMELIST_HTML/home_top.html', self.params)