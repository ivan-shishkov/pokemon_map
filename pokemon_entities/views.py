import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        image = pokemon_entity.pokemon.image
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.latitude,
            lon=pokemon_entity.longitude,
            name=pokemon_entity.pokemon.title,
            image_url=image.path if image else DEFAULT_IMAGE_URL,
        )

    pokemons_on_page = [
        {
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        }
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
        image = pokemon_entity.pokemon.image
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.latitude,
            lon=pokemon_entity.longitude,
            name=pokemon_entity.pokemon.title,
            image_url=image.path if image else DEFAULT_IMAGE_URL,
        )

    pokemon_info = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }

    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_info,
    })
