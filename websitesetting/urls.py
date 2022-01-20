from django.urls import path
from .views import (
    websitesettinghome,
    SliderCreate,
    SliderUpdate,
    SliderDelete,
    StudentActivitiesCreate,
    StudentActivitiesUpdate,
    SchoolSummeryList,
    SchoolSummeryUpdate,
    ExtraCourcesCreate,
    ExtraCourcesUpdate,
    ExtraCourcesDelete,
    GalleryCreate,
    GalleryUpdate,
    GalleryDelete,
    NoticeBoardCreate,
    NoticeBoardUpdate,
    NoticeBoardDelete,
    EventsCreate,
    EventsUpdate,
    EventsDelete,
    RegisterNowList,
    RegisterNowUpdate,
    registerstudent,
    register_request,
    AboutList,
    AboutUpdate
)



urlpatterns = [
    path('', websitesettinghome, name='websitesettinghome'),
    path('sliders/', SliderCreate.as_view(), name='sliders_create'),
    path('sliders/<int:pk>/edit/', SliderUpdate.as_view(), name='sliders_update'),
    path('sliders/<int:pk>/delete/', SliderDelete.as_view(), name='sliders_delete'),
    path('studentactivities/', StudentActivitiesCreate.as_view(), name='studentactivities_create'),
    path('studentactivities/<int:pk>/edit/', StudentActivitiesUpdate.as_view(), name='studentactivities_update'),
    path('summeryactivity/', SchoolSummeryList.as_view(), name='summeryactivity_list'),
    path('summeryactivity/<int:pk>/edit/', SchoolSummeryUpdate.as_view(), name='summeryactivity_update'),
     path('about/', AboutList.as_view(), name='about_list'),
    path('about/<int:pk>/edit/', AboutUpdate.as_view(), name='about_update'),
    path('registernow/', RegisterNowList.as_view(), name='registernow_list'),
    path('registernow/<int:pk>/edit/', RegisterNowUpdate.as_view(), name='registernow_update'),
    path('extracources/', ExtraCourcesCreate.as_view(), name='extracources_create'),
    path('extracources/<int:pk>/edit/', ExtraCourcesUpdate.as_view(), name='extracources_update'),
    path('extracources/<int:pk>/delete/', ExtraCourcesDelete.as_view(), name='extracources_delete'),
    
    path('gallery/', GalleryCreate.as_view(), name='gallery_create'),
    path('gallery/<int:pk>/edit/', GalleryUpdate.as_view(), name='gallery_update'),
    path('gallery/<int:pk>/delete/', GalleryDelete.as_view(), name='gallery_delete'),

    path('noticeboard/', NoticeBoardCreate.as_view(), name='noticeboard_create'),
    path('noticeboard/<int:pk>/edit/', NoticeBoardUpdate.as_view(), name='noticeboard_update'),
    path('noticeboard/<int:pk>/delete/', NoticeBoardDelete.as_view(), name='noticeboard_delete'),
    
    path('events/', EventsCreate.as_view(), name='events_create'),
    path('events/<int:pk>/edit/', EventsUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', EventsDelete.as_view(), name='events_delete'),
    path('registerstudent/', registerstudent, name='registerstudent'),
    path('register_request/', register_request, name='register_request')

]