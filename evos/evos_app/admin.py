from django.contrib import admin
from .models import Category,Dish
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Category)

class DishAdmin(admin.ModelAdmin):
    list_display=('pk','name','category','get_images')
    list_display_links = ('name','pk')
    list_editable = ('category',)
    list_filter = ('category',)
    search_fields = ('pk','name','about')
    list_per_page = 5

    def get_images(self,ovqat):
        if ovqat.photo:
            return mark_safe(f'<img src="{ovqat.photo.url}"width="150px"/>')
        else:
            return '-'
        get_images.short_description = 'Rasmi'

admin.site.register(Dish, DishAdmin)




