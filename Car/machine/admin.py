from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Brand, Color, Car, Comment

# Register your models here.

admin.site.register(Brand)
admin.site.register(Color)

class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "color", "price")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_per_page = 10
    list_max_show_all = 10

    def get_image(self, obj):
        if obj.photo:
            image_url = obj.photo.url
        else:
            image_url = "https://demofree.sirv.com/nope-not-here.jpg"
        return mark_safe(f'<img src="{image_url}" width="150">')

    get_image.short_description = "Photo"


admin.site.register(Car, CarAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'author', 'created_at')
    list_display_links = ('id', 'car')
    search_fields = ('author', 'comment',)
    list_filter = ('created_at',)
    list_per_page = 10


admin.site.register(Comment, CommentAdmin)