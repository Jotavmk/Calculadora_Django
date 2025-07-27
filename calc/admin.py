from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Operacao

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nome', 'is_admin', 'is_superuser', 'is_active', 'dt_inclusao')
    list_filter = ('is_admin', 'is_superuser', 'is_active', 'dt_inclusao')
    search_fields = ('email', 'nome')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('dt_inclusao',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'password1', 'password2'),
        }),
    )
    
    # Remover campos que não existem no nosso modelo
    filter_horizontal = ()
    filter_vertical = ()

@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'parametros', 'resultado', 'dt_inclusao')
    list_filter = ('dt_inclusao', 'usuario')
    search_fields = ('parametros', 'resultado', 'usuario__nome', 'usuario__email')
    ordering = ('-dt_inclusao',)
    readonly_fields = ('dt_inclusao',)
