import requests


class PokeAPIService:
    BASE_URL = "https://pokeapi.co/api/v2"

    def listar_pokemons(limit=20, offset=0):
        response = requests.get(
            f"{PokeAPIService.BASE_URL}/pokemon",
            params={'limit': limit, 'offset': offset}
        )
        response.raise_for_status()
        data = response.json()

        pokemons_detalhados = []
        for pokemon in data['results']:
            try:
                detalhes = PokeAPIService.obter_detalhes_pokemon_por_url(
                    pokemon['url'])
                pokemons_detalhados.append(detalhes)
            except Exception as e:
                print(f"Erro ao buscar detalhes de {pokemon['name']}: {e}")

        return {
            'count': data.get('count'),
            'next': data.get('next'),
            'previous': data.get('previous'),
            'results': pokemons_detalhados
        }

    def obter_detalhes_pokemon(nome_ou_id: str):
        response = requests.get(
            f"{PokeAPIService.BASE_URL}/pokemon/{nome_ou_id}")
        response.raise_for_status()
        return PokeAPIService._formatar_pokemon(response.json())

    def obter_detalhes_pokemon_por_url(url: str):
        response = requests.get(url)
        response.raise_for_status()
        return PokeAPIService._formatar_pokemon(response.json())

    def _formatar_pokemon(data: dict):
        sprites = data.get('sprites', {})
        stats = data.get('stats', [])

        def get_stat(stat_name):
            for stat in stats:
                if stat['stat']['name'] == stat_name:
                    return stat['base_stat']
            return 0

        return {
            'id': data['id'],
            'nome': data['name'].capitalize(),
            'imagem_url': sprites.get('other', {}).get('official-artwork', {}).get('front_default') or sprites.get('front_default'),
            'tipos': [t['type']['name'] for t in data.get('types', [])],
            'tipo_principal': data['types'][0]['type']['name'] if data.get('types') else None,
            'hp': get_stat('hp'),
            'ataque': get_stat('attack'),
            'defesa': get_stat('defense'),
            'altura': data.get('height') / 10,
            'peso': data.get('weight') / 10,
            'habilidades': [h['ability']['name'] for h in data.get('abilities', [])],
            'experiencia_base': data.get('base_experience'),
        }

    def buscar_por_geracao(geracao: int):
        response = requests.get(
            f"{PokeAPIService.BASE_URL}/generation/{geracao}")
        response.raise_for_status()
        data = response.json()

        pokemons = []
        for species in data.get('pokemon_species', [])[:20]:
            nome = species['name']
            try:
                detalhes = PokeAPIService.obter_detalhes_pokemon(nome)
                pokemons.append(detalhes)
            except Exception as e:
                print(f"Erro ao buscar Pokémon {nome}: {e}")

        return {
            'geracao': geracao,
            'nome': data.get('name'),
            'pokemons': pokemons
        }

    def buscar_por_tipo(tipo: str):
        response = requests.get(
            f"{PokeAPIService.BASE_URL}/type/{tipo.lower()}")
        response.raise_for_status()
        data = response.json()

        pokemons = []
        for entry in data.get('pokemon', [])[:20]:
            nome = entry['pokemon']['name']
            try:
                detalhes = PokeAPIService.obter_detalhes_pokemon(nome)
                pokemons.append(detalhes)
            except Exception as e:
                print(f"Erro ao buscar Pokémon {nome}: {e}")

        return {
            'tipo': tipo.lower(),
            'pokemons': pokemons
        }
