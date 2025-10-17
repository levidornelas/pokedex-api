from django.urls import path, include

urlpatterns = [
    path('', include('apps.pokemon.urls')),
    path('auth/', include('apps.usuario.urls')),
]
