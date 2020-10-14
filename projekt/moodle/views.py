from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnici, Predmeti, Upisi
from .forms import KorisniciForm, AddCourseForm
from django.contrib import messages
from .decorators import mentor_required, student_required


# Create your views here.


def index(request):
    return render(request, 'moodle/index.html')

def register(request):
    if request.method == 'GET':
        korisniciForm = KorisniciForm()
        return render(request, 'register.html', {'form': korisniciForm})
    elif request.method == 'POST':
        korisniciForm = KorisniciForm(request.POST)
        if korisniciForm.is_valid():
            korisnik = korisniciForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {korisnik}!')
            korisniciForm.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': korisniciForm})
    else:
        return redirect('register')

def enroll(course_id,student):
    if not Upisi.objects.filter(student_id=student.id, predmet_id=course_id):
                Upisi.objects.create(student_id=student.id, predmet_id=course_id, status="enrolled")
def dismiss(course_id,student):
    Upisi.objects.filter(predmet_id=course_id, student_id=student.id).delete()

def passed(course_id,student):
    Upisi.objects.filter(predmet_id=course_id, student_id=student.id).update(status="passed")

def not_passed(course_id,student):
    Upisi.objects.filter(predmet_id=course_id, student_id=student.id).delete()



@student_required
def upisni_list(request):
    if (request.user.is_authenticated):
        username = request.user.get_username()
        student = Korisnici.objects.get(username=username)
        if (request.method == 'POST'):
            if request.POST.get("enroll"):
                enroll(request.POST.get("enroll"),student)
            elif request.POST.get("dismiss"):
                dismiss(request.POST.get("dismiss"),student)
            elif request.POST.get("passed"):
                passed(request.POST.get("passed"),student)
            elif request.POST.get("not-passed"):
                not_passed(request.POST.get("not-passed"),student)

        upisani = Upisi.objects.filter(student=student.id).order_by('predmet_id')
        predmeti = Predmeti.objects.exclude(id__in=upisani.values('predmet_id'))
        if student.status == "REDOVNI":
            br_semestara=6
        else:
            br_semestara=8
        context = {
            'predmeti': predmeti, 
            'upisani': upisani, 
            'student': student, 
            'semestri': range(1, br_semestara + 1)
        }
        return render(request, 'upisni-list.html', context)
    else:
        return redirect('login')


@mentor_required
def studenti(request):
    studenti = Korisnici.objects.filter(user_role='STUDENT')
    return render(request, 'studenti.html', {'studenti': studenti})



@mentor_required
def upisni_list_studenta(request, student_id):
    student = Korisnici.objects.get(id=student_id)
    if (request.method == 'POST'):
        if request.POST.get("enroll"):
            enroll(request.POST.get("enroll"),student)
        elif request.POST.get("dismiss"):
            dismiss(request.POST.get("dismiss"),student)
        elif request.POST.get("passed"):
            passed(request.POST.get("passed"),student)
        elif request.POST.get("not-passed"):
            not_passed(request.POST.get("not-passed"),student)
    
    upisani = Upisi.objects.filter(student=student.id).order_by('predmet_id')
    predmeti = Predmeti.objects.exclude(id__in=upisani.values('predmet_id'))
    if student.status == "REDOVNI":
            br_semestara=6
    else:
            br_semestara=8
    context = {
        'predmeti': predmeti, 
        'upisani': upisani, 
        'student': student, 
        'semestri': range(1, br_semestara + 1)
    }
    return render(request, 'upisni-list.html', context)


@mentor_required
def courses(request):
    if request.method == 'GET':
        courses = Predmeti.objects.all()
        return render(request, 'courses.html', {'courses': courses})
    elif request.method == 'POST':
        if request.POST.get("delete"):
            delete = request.POST.get("delete")
            Predmeti.objects.filter(id=delete).delete()
            return redirect('courses')

@mentor_required
def add_course(request):
    if request.method == 'GET':
        addcourseform = AddCourseForm()
        return render(request, 'add-course.html', {'form': addcourseform})
    elif request.method == 'POST':
        addcourseform = AddCourseForm(request.POST)
        if addcourseform.is_valid():
            addcourseform.save()
            return redirect('courses')
        else:
            return render(request, 'add-course.html', {'form': addcourseform})

@mentor_required
def edit_course(request, course_id):
    course = Predmeti.objects.get(id=course_id)
    if request.method == 'GET':
        courseForm = AddCourseForm()
        courseForm.fields['ime'].initial = course.ime
        courseForm.fields['kod'].initial = course.kod
        courseForm.fields['program'].initial = course.program
        courseForm.fields['bodovi'].initial = course.bodovi
        courseForm.fields['sem_redovni'].initial = course.sem_redovni
        courseForm.fields['sem_izvanredni'].initial = course.sem_izvanredni
        courseForm.fields['izborni'].initial = course.izborni
        return render(request, 'edit-course.html', {'form': courseForm})
    elif request.method == 'POST':
        courseForm = AddCourseForm(request.POST, instance=course)
        if courseForm.is_valid():
            courseForm.save()
            return redirect('courses')
        else: 
            return render(request, 'edit-course.html', {'form': courseForm})



@mentor_required
def course_details(request, course_id):
    course = Predmeti.objects.get(id=course_id)
    return render(request, 'course-details.html', {'course': course})