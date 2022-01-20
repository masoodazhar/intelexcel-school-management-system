from django.shortcuts import redirect, render

def check_user_login(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session['student_login']:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('frontendhome')            
    return wrapper_func