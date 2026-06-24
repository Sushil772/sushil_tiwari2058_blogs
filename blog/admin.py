from django.contrib import admin
from .models import Category,Post,Comment

# Register your models here.
#admin.site.register(Category)




#show comments inside post page
class CommentInline(admin.TabularInline):
    model=Comment
    extra=0








@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields=["name"]
    list_display=['id','name']
    ordering=['name']
#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields=["title"]
    list_filter=['category','author']
   # list_filter=['author']
    list_display=['title','author','category','Created_at']
    ordering=['-Created_at']
    autocomplete_fields=['author','category']
    inlines=[CommentInline]
    list_per_page=2
    



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields=["body","user__username"]
    list_filter=['post','user']
    list_display=['post','user','body','created_at']
    ordering=['created_at']
    autocomplete_fields=['post']
