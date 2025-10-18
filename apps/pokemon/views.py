from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PokemonUsuario, TipoPokemon
from .serializers import (
    PokemonUsuarioSerializer,
    TipoPokemonSerializer,
    ToggleFavoritoSerializer,
    ToggleGrupoBatalhaSerializer,
)
from .services import PokeAPIService


class TipoPokemonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoPokemon.objects.all()
    serializer_class = TipoPokemonSerializer
    permission_classes = [IsAuthenticated]


class PokemonUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = PokemonUsuarioSerializer
    permission_classes = []

    def get_queryset(self):
        return PokemonUsuario.objects.filter(
            id_usuario=self.request.user
        ).select_related('id_tipo_pokemon')

    def perform_create(self, serializer):
        serializer.save(id_usuario=self.request.user)

    def _criar_pokemon_do_api(self, codigo):
        pass

    @action(detail=False, methods=['get'])
    def favoritos(self, request):
        favoritos = self.get_queryset().filter(favorito=True)
        serializer = self.get_serializer(favoritos, many=True)
        return Response({'results': serializer.data})

    @action(detail=False, methods=['get'])
    def grupo_batalha(self, request):
        grupo = self.get_queryset().filter(grupo_batalha=True)
        serializer = self.get_serializer(grupo, many=True)
        return Response({
            'count': grupo.count(),
            'max': 6,
            'results': serializer.data
        })

    @action(detail=True, methods=['patch'])
    def toggle_favorito(self, request, pk=None):
        codigo = pk

        try:
            pokemon = PokemonUsuario.objects.get(
                id_usuario=request.user, codigo=codigo)
        except PokemonUsuario.DoesNotExist:
            pokemon = None

        serializer = ToggleFavoritoSerializer(
            data=request.data,
            instance=pokemon,
            context={'request': request, 'codigo': codigo}
        )

        if serializer.is_valid():
            pokemon_atualizado = serializer.save()
            return Response(PokemonUsuarioSerializer(pokemon_atualizado).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def toggle_grupo_batalha(self, request, pk=None):
        codigo = pk

        try:
            pokemon = PokemonUsuario.objects.get(
                id_usuario=request.user, codigo=codigo)
        except PokemonUsuario.DoesNotExist:
            pokemon = None

        serializer = ToggleGrupoBatalhaSerializer(
            data=request.data,
            instance=pokemon,
            context={'request': request, 'codigo': codigo}
        )

        if serializer.is_valid():
            pokemon_atualizado = serializer.save()
            return Response(PokemonUsuarioSerializer(pokemon_atualizado).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PokeAPIProxyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _anexar_status_usuario(self, request, pokemons):
        user = request.user
        banco = PokemonUsuario.objects.filter(id_usuario=user)
        status_map = {p.codigo: {'favorito': p.favorito,
                                 'grupo_batalha': p.grupo_batalha} for p in banco}

        for p in pokemons:
            codigo = str(p['id'])
            if codigo in status_map:
                p['favorito'] = status_map[codigo]['favorito']
                p['grupo_batalha'] = status_map[codigo]['grupo_batalha']
            else:
                p['favorito'] = False
                p['grupo_batalha'] = False

        return pokemons

    @action(detail=False, methods=['get'])
    def listar(self, request):
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        try:
            data = PokeAPIService.listar_pokemons(limit, offset)
            data['results'] = self._anexar_status_usuario(
                request, data['results'])
            return Response(data)
        except Exception as e:
            return Response({'error': f'Erro ao buscar Pokémons: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def detalhes(self, request):
        nome_ou_id = request.query_params.get(
            'nome') or request.query_params.get('id')
        if not nome_ou_id:
            return Response({'error': 'Parâmetro "nome" ou "id" é obrigatório'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            data = PokeAPIService.obter_detalhes_pokemon(nome_ou_id)
            data['favorito'] = PokemonUsuario.objects.filter(
                id_usuario=request.user, codigo=str(data['id']), favorito=True).exists()
            data['grupo_batalha'] = PokemonUsuario.objects.filter(
                id_usuario=request.user, codigo=str(data['id']), grupo_batalha=True).exists()
            return Response(data)
        except Exception as e:
            return Response({'error': f'Pokémon não encontrado: {str(e)}'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def por_geracao(self, request):
        geracao = request.query_params.get('geracao')
        if not geracao:
            return Response({'error': 'Parâmetro "geracao" é obrigatório'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            geracao = int(geracao)
            if geracao < 1 or geracao > 9:
                return Response({'error': 'Geração deve estar entre 1 e 9'},
                                status=status.HTTP_400_BAD_REQUEST)

            data = PokeAPIService.buscar_por_geracao(geracao)

            data['pokemons'] = self._anexar_status_usuario(
                request, data['pokemons'])

            return Response(data)

        except ValueError:
            return Response({'error': 'Geração deve ser um número inteiro'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Erro ao buscar geração: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        tipo = request.query_params.get('tipo')
        if not tipo:
            return Response({'error': 'Parâmetro "tipo" é obrigatório'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            data = PokeAPIService.buscar_por_tipo(tipo)
            data['pokemons'] = self._anexar_status_usuario(
                request, data['pokemons'])
            return Response(data)
        except Exception as e:
            return Response({'error': f'Erro ao buscar tipo: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
