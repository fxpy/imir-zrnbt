from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib.auth.models import User as DjangoUser, Group as DjangoGroup

from preferences.admin import PreferencesAdmin

from main.models import User, Phone, Texts, Post


def mail(modeladmin, request, queryset):
    post = Post()
    post.save()

    for user in queryset:
        post.users.add(user)

    return redirect(f'/main/post/{post.pk}/change/')
mail.short_description = 'Отправить сообщение'


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'joined', 'username_url', 'first_name', 'last_name',
    ]
    list_display_links = None

    date_hierarchy = 'joined'
    search_fields = [
        'user_id', 'username', 'first_name', 'last_name',
    ]

    actions = [
        mail,
    ]

    def username_url(self, obj):
        if obj.username:
            url = 'https://t.me/' + obj.username
            html = f'<a href="{url}" target="_blank">@{obj.username}</a>'
            return format_html(html)
        else:
            return '-'
    username_url.short_description = '@username'

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class PhoneAdmin(admin.ModelAdmin):
    list_display = [
        'phone', 'name', 'profession', 'geobase', 'status',
    ]
    list_display_links = None
    list_editable = [
        'phone', 'name', 'profession', 'geobase', 'status',
    ]

    search_fields = [
        'phone', 'name', 'profession', 'geobase',
    ]
    list_filter = [
        'status',
    ]

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False

        return super().add_view(request, form_url, extra_context)


class TextsAdmin(PreferencesAdmin):
    change_form_template = 'admin/texts_change_form.html'

    fieldsets = [
        (
            'Сообщения',
            {
                'fields': [
                    'start_message',
                    'main_message',
                    'result_message',
                    'no_result_message',
                ]
            }
        )
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False

        return super().change_view(request, object_id, form_url, extra_context)


class PostAdmin(admin.ModelAdmin):
    change_form_template = 'admin/post_change_form.html'

    list_display = [
        'created', 'status', 'amount_of_receivers',
        'text', 'image',
    ]
    list_display_links = [
        'created',
    ]

    search_fields = [
        'text',
    ]
    list_filter = [
        'status',
    ]

    list_per_page = 10

    def get_fieldsets(self, request, obj=None):
        base_fieldsets = [
            ('Сообщение', {'fields': [
                'image',
                'text',
            ]}),
        ]

        if not obj:
            return base_fieldsets
        else:
            return [
                ('Информация', {'fields': [
                    'created',
                    'status',
                    'users',
                ] + (['amount_of_receivers'] if obj.status == 'done' else [])}),
            ] + base_fieldsets

    def get_readonly_fields(self, request, obj=None):
        return ['created', 'status', 'users', 'amount_of_receivers']

    def has_change_permission(self, request, obj=None):
        return (obj is None) or (obj.status in ['created'])

    def has_delete_permission(self, request, obj=None):
        return (obj is None) or (obj.status in ['created', 'queue', 'done'])

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False

        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False

        return super().change_view(request, object_id, form_url, extra_context)


admin.site.site_header = admin.site.site_title = 'Администрирование бота'
admin.site.site_url = ''

admin.site.register(User, UserAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Texts, TextsAdmin)
admin.site.register(Post, PostAdmin)

admin.site.unregister(DjangoUser)
admin.site.unregister(DjangoGroup)
