from django.forms import ModelForm
from .models import Predmeti, Korisnici
from django.contrib.auth.forms import UserCreationForm

class KorisniciForm(UserCreationForm):
        class Meta:
                model = Korisnici
                fields = ('username','password1', 'password2', 'email' , 'status' )
        def save(self, commit=True):
                user = super(KorisniciForm, self).save(commit=False)
                user.user_role = "STUDENT"
                user.save()
                return user

class AddCourseForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = ['ime', 'kod', 'program', 'bodovi', 'sem_redovni', 'sem_izvanredni', 'izborni']
