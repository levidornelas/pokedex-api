from django.db import models
from apps.usuario.models import Usuario


class TipoPokemon(models.Model):
    id_tipo_pokemon = models.AutoField(
        primary_key=True, db_column='IDTipoPokemon')
    descricao = models.CharField(
        max_length=50, unique=True, db_column='Descricao')

    class Meta:
        db_table = 'TipoPokemon'
        verbose_name = 'Tipo de Pokémon'
        verbose_name_plural = 'Tipos de Pokémon'

    def __str__(self):
        return self.descricao


class PokemonUsuario(models.Model):
    id_pokemon_usuario = models.AutoField(
        primary_key=True, db_column='IDPokemonUsuario')
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='IDUsuario',
        related_name='pokemons'
    )
    id_tipo_pokemon = models.ForeignKey(
        TipoPokemon,
        on_delete=models.PROTECT,
        db_column='IDTipoPokemon',
        related_name='pokemons'
    )
    codigo = models.CharField(max_length=20, db_column='Codigo')
    imagem_url = models.CharField(max_length=255, db_column='ImagemUrl')
    nome = models.CharField(max_length=100, db_column='Nome')
    grupo_batalha = models.BooleanField(
        default=False, db_column='GrupoBatalha')
    favorito = models.BooleanField(default=False, db_column='Favorito')

    class Meta:
        db_table = 'PokemonUsuario'
        verbose_name = 'Pokémon do Usuário'
        verbose_name_plural = 'Pokémons dos Usuários'
        # Garante que um usuário não tenha dois pokémons com o mesmo código
        unique_together = [['id_usuario', 'codigo']]

    def __str__(self):
        return f"{self.nome} ({self.codigo}) - {self.id_usuario.login}"
