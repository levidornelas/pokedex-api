from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from .managers import UsuarioManager


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column='IDUsuario')
    nome = models.CharField(max_length=100, db_column='Nome')
    login = models.CharField(max_length=50, unique=True, db_column='Login')
    email = models.EmailField(max_length=100, unique=True, db_column='Email')
    password = models.CharField(max_length=255, db_column='Password')
    dt_inclusao = models.DateTimeField(
        default=timezone.now, db_column='DtInclusao')
    dt_alteracao = models.DateTimeField(auto_now=True, db_column='DtAlteracao')

    is_active = models.BooleanField(default=True, db_column='IsActive')
    is_admin = models.BooleanField(default=False, db_column='IsAdmin')

    objects = UsuarioManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'nome']

    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
