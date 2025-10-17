from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PokemonUsuarioViewSet, TipoPokemonViewSet, PokeAPIProxyViewSet

router = DefaultRouter()
router.register(r'pokemons', PokemonUsuarioViewSet, basename='pokemon')
router.register(r'tipos', TipoPokemonViewSet, basename='tipo-pokemon')
router.register(r'pokeapi', PokeAPIProxyViewSet, basename='pokeapi')

urlpatterns = [
    path('', include(router.urls)),
]
