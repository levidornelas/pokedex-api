from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('id_usuario', 'login', 'nome', 'email',
                    'is_active', 'is_admin', 'dt_inclusao')
    list_filter = ('is_active', 'is_admin', 'dt_inclusao')
    search_fields = ('login', 'nome', 'email')
    ordering = ('-dt_inclusao',)

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_admin')}),
        ('Datas', {'fields': ('dt_inclusao', 'dt_alteracao')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'nome', 'email', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )

    # Campos somente leitura
    readonly_fields = ('dt_inclusao', 'dt_alteracao')

    filter_horizontal = ()
