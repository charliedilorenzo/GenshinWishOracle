from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View

# from .models import 


class IndexView(generic.ListView):
    # TODO
    template_name = 'analyze/index.html'
    # context_object_name = 

    # def get_queryset(self):
    #     """
    #     Return the last five published questions (not including those set to be
    #     published in the future).
    #     """
    #     return Question.objects.filter(
    #         pub_date__lte=timezone.now()
    #     ).order_by('-pub_date')[:5]

class AnalyzeCharacterBannerView(generic.ListView):
    # TODO
    # template_name = 'analyze/index.html'
    # context_object_name = 
    pass

class AnalyzeWeaponBannerView(generic.ListView):
    # TODO
    # template_name = 'analyze/index.html'
    # context_object_name = 
    pass