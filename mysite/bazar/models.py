from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)

    USERNAME_FIELD = 'usuario__email'

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=255)
    inicio = models.DateTimeField(auto_now_add=True)
    fim = models.DateTimeField(blank=True, null=True)
    adm = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Item(models.Model):
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='fotos/')
    descricao = models.CharField(max_length=255)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Reserva(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()

    def __str__(self):
        return f"Reserva de {self.usuario.nome}"