from django.urls import path
from CampusInsight import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('',views.home,name="home"),
    path('gallery/',views.gallery,name="gallery"),
    path('about/',views.about,name="about"),
    path('events/',views.events,name="events"),
    path('activities/',views.activities,name="activities"),
    path('terms/',views.terms,name="terms"),
    path('contact/',views.contact,name="contact"),
    path('profile/', views.profile, name='profile'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('exam_creation/', views.exam_creation, name='exam_creation'),
    path('edit_exam/<str:j>/', views.edit_exam, name='edit_exam'),
    path('exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('exam/<int:exam_id>/edit/', views.edit_question, name='edit_question'),
    path('exam/<int:exam_id>/save/', views.save_all_questions, name='save_all_questions'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
]