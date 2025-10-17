from django.contrib import admin

# Register your models here.
from .models import PokemonUsuario, TipoPokemon

admin.site.register(PokemonUsuario)
admin.site.register(TipoPokemon)