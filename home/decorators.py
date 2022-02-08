from django.http import  HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, Permission

def unuthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('userprofile')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func 


def allowed_users(allowed_roles):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # print('=========kkkk=========')
            if Group.objects.filter(name=request.user.username):
                group_created = Group.objects.get(name=request.user.username)
                # print('got some thing')
            else:
                # print('got nothing')
                group_created = Group.objects.get(name='school_user')
            permission_list = []

            for permission in Permission.objects.values('codename').filter(group=group_created):
                permission_list.append(permission['codename'])
                # print('===========coming---=======')
                # print(permission_list)
                # print('===========second============')
                # print(group_created)
            permission_list.append('profile')
            if allowed_roles in permission_list:
                # print('============USER ALLOWED===========')
                return view_func(request, *args, **kwargs)
            else:
                return render(request,'403.html')
        return wrapper_func
    return decorator