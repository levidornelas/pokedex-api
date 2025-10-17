from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, login, email, nome, password=None):
        if not login:
            raise ValueError('Usuário deve ter um login')
        if not email:
            raise ValueError('Usuário deve ter um email')

        user = self.model(
            login=login,
            email=self.normalize_email(email),
            nome=nome
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, nome, password=None):
        user = self.create_user(
            login=login,
            email=email,
            nome=nome,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
