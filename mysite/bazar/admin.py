from django.contrib import admin
from .models import Usuario, Evento, Item, Reserva

admin.site.register(Usuario)
admin.site.register(Evento)
admin.site.register(Item)
admin.site.register(Reserva)
