from django.db import models

from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

# Create your models here.

class Korisnici(AbstractUser):
    class UserRole(models.TextChoices):
        MENTOR = 'MENTOR', _('Mentor')
        STUDENT = 'STUDENT', _('Student')

    user_role = models.CharField(
        max_length=16,
        choices=UserRole.choices,
        null=False,
    )

    class Status(models.TextChoices):
        NONE = 'NONE', _('None')
        REDOVNI = 'REDOVNI', _('Redovni')
        IZVANREDNI = 'IZVANREDNI', _('Izvanredni')

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        null=False,
    )


class Predmeti(models.Model):
    ime = models.CharField(max_length=255, null=False,)
    kod = models.CharField(max_length=16, null=False, unique=True,)
    program = models.TextField(null=False,)
    bodovi = models.IntegerField(null=False,)
    sem_redovni = models.IntegerField(null=False,)
    sem_izvanredni = models.IntegerField(null=False,)

    class Izborni(models.TextChoices):
        DA = 'DA', _('Da')
        NE = 'NE', _('Ne')

    izborni = models.CharField(max_length=8, choices=Izborni.choices, null=False,)

    '''def __str__(self):
        return '%s - %s - %s ECTS-a' % (self.kod, self.ime)'''

    def __str__(self):
        return '%s - %s' % (self.kod, self.ime)

class Upisi(models.Model):
    student = models.ForeignKey(
        'Korisnici',
        on_delete=models.CASCADE,
        null=False,
    )
    predmet = models.ForeignKey(
        'Predmeti',
        on_delete=models.CASCADE,
        null=False,
    )
    status = models.CharField(max_length=64, null=False,)

    def __str__(self):
        return '%s - %s - %s' % (self.student, self.predmet, self.status)

