from django.urls import path
from .views import (
    ClassesView,
    ClassesCreate,
    ClassesUpdate,
    ClassesDelete,
    RoomView,
    RoomCreate,
    RoomUpdate,
    RoomDelete,
    SubjectView,
    SubjectCreate,
    SubjectUpdate,
    SubjectDelete,
    RoutineView,
    RoutineCreate,
    RoutineUpdate,
    RoutineDelete,
    AcademicView,
    get_section_by_class
    
)


app_name = 'academic'
urlpatterns = [
    path('', AcademicView, name='academic_main'),
    path('classes/view', ClassesView.as_view(), name='classes_view'),
    path('classes/create', ClassesCreate.as_view(), name='classes_create'),
    path('classes/<int:pk>/update', ClassesUpdate.as_view(), name='classes_update'),
    path('classes/<int:pk>/delete', ClassesDelete.as_view(), name='classes_delete'),
    path('room/view', RoomView.as_view(), name='room_view'),
    path('room/create', RoomCreate.as_view(), name='room_create'),
    path('room/<int:pk>/update', RoomUpdate.as_view(), name='room_update'),
    path('room/<int:pk>/delete', RoomDelete.as_view(), name='room_delete'),
    path('subject/view', SubjectView.as_view(), name='subject_view'),
    path('subject/create', SubjectCreate.as_view(), name='subject_create'),
    path('subject/<int:pk>/update', SubjectUpdate.as_view(), name='subject_update'),
    path('subject/<int:pk>/delete', SubjectDelete.as_view(), name='subject_delete'),
    path('routine/view', RoutineView.as_view(), name='routine_view'),
    path('routine/create', RoutineCreate.as_view(), name='routine_create'),
    path('routine/<int:pk>/update', RoutineUpdate.as_view(), name='routine_update'),
    path('routine/<int:pk>/delete', RoutineDelete.as_view(), name='routine_delete'),
    path('get_section_by_class/', get_section_by_class, name='get_section_by_class'),

]

