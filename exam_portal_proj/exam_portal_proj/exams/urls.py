from django.urls import path
from . import views

urlpatterns = [
    path('',          views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('dashboard/',views.dashboard,     name='dashboard'),
    path('exam-form/',views.exam_form_view,name='exam_form'),
    path('success/',  views.success_view,  name='success'),
]
