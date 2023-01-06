from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View

class IndexView(generic.TemplateView):
    template_name = 'genshinwishoracle/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context