from django.contrib import admin
from .models import User,Log,Work,Topic,Usertopic

# Register your models here.

admin.site.register(User)
admin.site.register(Log)
admin.site.register(Work)
admin.site.register(Topic)
admin.site.register(Usertopic)