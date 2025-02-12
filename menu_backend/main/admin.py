from django.contrib import admin
from .models import Category, MenuItem, Headertext, SubCategory

admin.site.register(Category, admin.ModelAdmin)
admin.site.register(MenuItem, admin.ModelAdmin)
admin.site.register(Headertext, admin.ModelAdmin)
admin.site.register(SubCategory, admin.ModelAdmin)
