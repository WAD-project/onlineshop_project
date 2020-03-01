from django.contrib import admin
from reuse.models import Category, Subcategory, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)


