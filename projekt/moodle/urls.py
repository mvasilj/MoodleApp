from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('upisni-list/', views.upisni_list, name="upisni-list"),
    path('upisni-list/<int:student_id>', views.upisni_list_studenta, name="upisni-list"),
    path('studenti/', views.studenti, name="studenti"),
    path('courses/', views.courses, name="courses"),
    path('add-course/', views.add_course, name="add-course"),
    path('edit-course/<int:course_id>', views.edit_course, name="edit-course"),
    path('course-details/<int:course_id>', views.course_details, name="course-details"),
]