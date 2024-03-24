from django.contrib import admin
from .models import *


admin.site.register(Vtype)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('machine','user','timestamp')
    
admin.site.register(Client,ClientAdmin)



class MachineAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_unavailabled','timestamp')

admin.site.register(Machine,MachineAdmin)

class BookmarkMachineAdmin(admin.ModelAdmin):
    list_display = ('machine','user','timestamp')
admin.site.register(BookmarkMachine,BookmarkMachineAdmin)


from django.contrib import admin

# Register your models here.
