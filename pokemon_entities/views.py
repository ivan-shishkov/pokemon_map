import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def get_string_representation(pokemon_entity_property):
    return str(pokemon_entity_property) if pokemon_entity_property else 'N/A'


def get_pokemon_entity_popup_content(pokemon_entity):
    info_strings = [
        f'<h4>{pokemon_entity.pokemon.title}</h4>',
        f'<h5>Уровень: {get_string_representation(pokemon_entity.level)}</h5>',
        f'<h5>Здоровье: {get_string_representation(pokemon_entity.health)}</h5>',
    ]
    return ''.join(info_strings)


def add_pokemon(folium_map, pokemon_entity):
    image = pokemon_entity.pokemon.image
    image_url = image.path if image else DEFAULT_IMAGE_URL

    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [pokemon_entity.latitude, pokemon_entity.longitude],
        tooltip=pokemon_entity.pokemon.title,
        icon=icon,
        popup=get_pokemon_entity_popup_content(pokemon_entity),
    ).add_to(folium_map)


def get_essential_pokemon_info(pokemon):
    if not pokemon:
        return None

    return {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
    }


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        add_pokemon(
            folium_map=folium_map,
            pokemon_entity=pokemon_entity,
        )

    pokemons_on_page = [
        get_essential_pokemon_info(pokemon)
        for pokemon in Pokemon.objects.all()
    ]

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon):
        add_pokemon(
            folium_map=folium_map,
            pokemon_entity=pokemon_entity,
        )

    pokemon_info = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': get_essential_pokemon_info(pokemon.previous_evolution),
        'next_evolution': get_essential_pokemon_info(pokemon.next_evolution.first()),
    }

    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_info,
    })
