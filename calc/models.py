from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Operacao(models.Model):
    id = models.AutoField(primary_key=True, db_column='IDOperacao')
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='IDUsuario', related_name='operacoes')
    parametros = models.CharField(max_length=255, db_column='Parametros')
    resultado = models.CharField(max_length=255, db_column='Resultado')
    dt_inclusao = models.DateTimeField(auto_now_add=True, db_column='DTInclusao')

    def __str__(self):
        return f"{self.parametros} = {self.resultado} ({self.usuario.nome})"

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha=None):
        if not email:
            raise ValueError('O usuário deve ter um email')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, senha):
        user = self.create_user(email, nome, senha)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True, db_column='IDUsuario')
    nome = models.CharField(max_length=255, db_column='Nome')
    email = models.EmailField(unique=True, db_column='Email')
    # password = models.CharField(max_length=128)  # herdado de AbstractBaseUser, campo obrigatório NOT NULL
    dt_inclusao = models.DateTimeField(auto_now_add=True, db_column='DTInclusao')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome

    @property
    def is_staff(self):
        return self.is_admin
