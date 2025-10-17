from rest_framework import serializers
from .models import PokemonUsuario, TipoPokemon
from .services import PokeAPIService


class TipoPokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPokemon
        fields = ('id_tipo_pokemon', 'descricao')
        read_only_fields = ('id_tipo_pokemon',)


class PokemonUsuarioSerializer(serializers.ModelSerializer):
    tipo_pokemon = TipoPokemonSerializer(
        source='id_tipo_pokemon', read_only=True)

    class Meta:
        model = PokemonUsuario
        fields = (
            'id_pokemon_usuario',
            'codigo',
            'nome',
            'imagem_url',
            'id_tipo_pokemon',
            'tipo_pokemon',
            'favorito',
            'grupo_batalha'
        )
        read_only_fields = ('id_pokemon_usuario', 'id_usuario')

    def validate_grupo_batalha(self, value):
        if value:
            user = self.context['request'].user

            if self.instance:
                count = PokemonUsuario.objects.filter(
                    id_usuario=user,
                    grupo_batalha=True
                ).exclude(id_pokemon_usuario=self.instance.id_pokemon_usuario).count()
            else:
                count = PokemonUsuario.objects.filter(
                    id_usuario=user,
                    grupo_batalha=True
                ).count()

            if count >= 6:
                raise serializers.ValidationError(
                    "Você já tem 6 pokémons no grupo de batalha. Remova um antes de adicionar outro."
                )
        return value


class ToggleBaseSerializer(serializers.Serializer):
    def _obter_ou_criar_pokemon(self, codigo, user):

        if self.instance:
            return self.instance
        try:
            data = PokeAPIService.obter_detalhes_pokemon(codigo)
            tipo, _ = TipoPokemon.objects.get_or_create(
                descricao=data['tipo_principal'])

            pokemon_data = {
                'codigo': codigo,
                'nome': data['nome'],
                'imagem_url': data['imagem_url'],
                'id_tipo_pokemon': tipo,
                'id_usuario': user,
                'favorito': False,
                'grupo_batalha': False,
            }

            pokemon = PokemonUsuario.objects.create(**pokemon_data)
            return pokemon
        except Exception as e:
            raise serializers.ValidationError(
                f"Erro ao obter dados do Pokémon na API: {e}")


class ToggleFavoritoSerializer(ToggleBaseSerializer):
    favorito = serializers.BooleanField()

    def save(self, **kwargs):
        user = self.context['request'].user
        codigo = self.context['codigo']

        pokemon = self._obter_ou_criar_pokemon(codigo, user)

        pokemon.favorito = self.validated_data['favorito']
        pokemon.save()

        return pokemon


class ToggleGrupoBatalhaSerializer(ToggleBaseSerializer):
    grupo_batalha = serializers.BooleanField()

    def validate_grupo_batalha(self, value):
        if value:
            user = self.context['request'].user

            queryset = PokemonUsuario.objects.filter(
                id_usuario=user,
                grupo_batalha=True
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.count() >= 6:
                raise serializers.ValidationError(
                    "Limite de 6 pokémons no grupo de batalha atingido."
                )
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        codigo = self.context['codigo']
        pokemon = self._obter_ou_criar_pokemon(codigo, user)
        pokemon.grupo_batalha = self.validated_data['grupo_batalha']
        pokemon.save()

        return pokemon
