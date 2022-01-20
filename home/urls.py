from django.urls import path, include
from .views import MainPage, Register, LogoutView, SchoolProfiles, csvfile, html_to_pdf_view

app_name = 'home'
urlpatterns = [
    path('', MainPage , name='main_page' ),
    # path('setting/change', ChangeSetting.as_view(template_name='setting.html') , name='setting' ),
    path('register/register/', Register.as_view(), name='register'),
    path('profile/<int:pk>/complete', SchoolProfiles.as_view(), name='school_profile'),
    path('register/', include('django.contrib.auth.urls'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csv/', csvfile, name="csvfile"),
    path('html_to_pdf_view/', html_to_pdf_view, name="html_to_pdf_view")
]