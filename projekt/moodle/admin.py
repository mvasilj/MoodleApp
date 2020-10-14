from django.contrib import admin
from .models import Korisnici
from .models import Predmeti
from .models import Upisi
# Register your models here.
admin.site.register(Korisnici)
admin.site.register(Upisi)
admin.site.register(Predmeti)
