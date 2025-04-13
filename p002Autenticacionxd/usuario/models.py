from django.db import models

# Create your models here.
from django.conf import settings
#crear modelo para fecha de cumpleaños de cada usuario  que se guardara en usuario_profile, ahora cada usuario al registrase tendra su perfil CADA USUARIO donde podra editar SU LASTNAME Y FIRSNAME Y EDITAR O AÑADIR SU CUMPLE ACADA USUARIO 
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'