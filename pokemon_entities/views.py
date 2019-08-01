import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def get_string_representation(pokemon_entity_property):
    return str(pokemon_entity_property) if pokemon_entity_property is not None else 'N/A'


def get_pokemon_entity_popup_content(pokemon_entity):
    info_strings = [
        f'<h4>{pokemon_entity.pokemon.title}</h4>',
        f'<h5>Уровень: {get_string_representation(pokemon_entity.level)}</h5>',
        f'<h5>Здоровье: {get_string_representation(pokemon_entity.health)}</h5>',
        f'<h5>Сила: {get_string_representation(pokemon_entity.strength)}</h5>',
        f'<h5>Защита: {get_string_representation(pokemon_entity.defence)}</h5>',
        f'<h5>Выносливость: {get_string_representation(pokemon_entity.stamina)}</h5>',
    ]
    return ''.join(info_strings)


def add_pokemon_entity_to_map(pokemon_entity, folium_map):
    image = pokemon_entity.pokemon.image
    image_location = image.path if image else DEFAULT_IMAGE_URL

    icon = folium.features.CustomIcon(
        image_location,
        icon_size=(50, 50),
    )
    folium.Marker(
        [pokemon_entity.latitude, pokemon_entity.longitude],
        tooltip=pokemon_entity.pokemon.title,
        icon=icon,
        popup=folium.Popup(get_pokemon_entity_popup_content(pokemon_entity), max_width=150),
    ).add_to(folium_map)


def get_essential_pokemon_info(pokemon):
    if not pokemon:
        return None

    return {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
    }


def get_pokemon_element_type_info(pokemon):
    return [
        {
            'title': element_type.title,
            'img': element_type.image.url if element_type.image else DEFAULT_IMAGE_URL,
            'strong_against': [
                weak_type.title for weak_type in element_type.strong_against.all()
            ],
        }
        for element_type in pokemon.element_type.all()
    ]


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        add_pokemon_entity_to_map(
            pokemon_entity=pokemon_entity,
            folium_map=folium_map,
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
        add_pokemon_entity_to_map(
            pokemon_entity=pokemon_entity,
            folium_map=folium_map,
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
        'element_type': get_pokemon_element_type_info(pokemon),
    }

    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_info,
    })
