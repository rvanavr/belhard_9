from django.contrib import admin

# Register your models here.

from .models import Category, Post, Contact


@admin.action(description='опубликовать')
def make_published(self, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='снять с публикации')
def make_unpublished(self, request, queryset):
    queryset.update(is_published=False)


class ManagerPanel(admin.AdminSite):
    site_header = 'Manager Panel'
    site_title = 'manager'
    index_title = 'manager index'


manager = ManagerPanel(name='manager')


class PostInLine(admin.StackedInline):
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    actions = (make_published, make_unpublished)
    inlines = (PostInLine,)
    list_display = ('id', 'name', 'is_published')
    list_editable = ('name',)
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = (make_published, make_unpublished)
    search_fields = ('title',)
    search_help_text = 'Поиск по заголовку'
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('date_created',)
    date_hierarchy = 'date_created'
    ordering = ('date_created', '-title')
    list_display = ('title', 'full_name', 'date')
    list_filter = ('is_published', 'category', 'date_created')
    fieldsets = (
        (
            'Основное',
            {
                'fields': ('title', 'descr', 'category'),
                'description': 'Основные значения'
            }
        ),
        (
            'Дополнительное',
            {
                'fields': ('date_created', 'author', 'slug', 'image')
            }
        )
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')


class ContactManager(ContactAdmin):
    readonly_fields = ('email', 'name', 'message', 'data_created')


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Post, PostAdsmin)
manager.register(Category, CategoryAdmin)
manager.register(Post, PostAdmin)
manager.register(Contact, ContactAdmin)

