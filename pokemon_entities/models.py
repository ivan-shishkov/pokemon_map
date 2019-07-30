from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='', blank=True)
    title_jp = models.CharField(max_length=200, default='', blank=True)

    image = models.ImageField(upload_to='pokemons', null=True, blank=True)
    description = models.TextField(default='', blank=True)

    previous_evolution = models.ForeignKey(
        'self',
        related_name='next_evolution',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    latitude = models.FloatField()
    longitude = models.FloatField()

    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)

    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} ({self.latitude}, {self.longitude})'
