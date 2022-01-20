from django.urls import path
from .views import (
    FrontEndHome,
    FrontEndAbout,
    FrontEndCources,
    FrontEndEvent,
    FrontEndGallery,
    FrontEndContact,
    FrontEndLogin,
    FrontEndRegister,
    FrontEndLogout,
    NoticBoard,
    emptypage
)

urlpatterns = [
    path('', FrontEndHome, name="frontendhome"),
    path('frontendabout/', FrontEndAbout, name="frontendabout"),
    path('frontendcources/', FrontEndCources, name="frontendcources"),
    path('frontendevent/', FrontEndEvent, name="frontendevent"),
    path('frontendgallery/', FrontEndGallery, name="frontendgallery"),
    path('frontendcontact/', FrontEndContact, name="frontendcontact"),
    path('noticboard/', NoticBoard, name="noticboard"),
    path('frontendlogin/', FrontEndLogin.as_view(), name="frontendlogin"),
    path('frontendregister/', FrontEndRegister.as_view(), name="frontendregister"),
    path('frontendlogout/', FrontEndLogout, name="frontendlogout"),
    path('emptypage/', emptypage, name="emptypage"),
]