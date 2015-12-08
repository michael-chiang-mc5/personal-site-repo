from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def user_profile(request,user_pk):
    user_pk = int(user_pk)
    if request.user.pk == user_pk:
        user = request.user
        context = {'user':user,}
        return render(request, 'MCUser/user_profile_self.html', context)
    else:
        user = User.objects.get(pk=user_pk)
        context = {'user':user,}
        return render(request, 'MCUser/user_profile.html', context)
