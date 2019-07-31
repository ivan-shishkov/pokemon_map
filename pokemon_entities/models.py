from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField('название', max_length=200)

    def __str__(self):
        return f'{self.title}'


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    title_en = models.CharField('название (англ)', max_length=200, default='', blank=True)
    title_jp = models.CharField('название (япон)', max_length=200, default='', blank=True)

    image = models.ImageField('картинка', upload_to='pokemons', null=True, blank=True)
    description = models.TextField('описание', default='', blank=True)

    element_type = models.ManyToManyField(
        PokemonElementType,
        verbose_name='стихии',
        blank=True,
    )

    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='из кого эволюционировал',
        related_name='next_evolution',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='покемон',
    )

    latitude = models.FloatField('широта')
    longitude = models.FloatField('долгота')

    appeared_at = models.DateTimeField('когда появится', null=True, blank=True)
    disappeared_at = models.DateTimeField('когда исчезнет', null=True, blank=True)

    level = models.IntegerField('уровень', null=True, blank=True)
    health = models.IntegerField('здоровье', null=True, blank=True)
    strength = models.IntegerField('сила', null=True, blank=True)
    defence = models.IntegerField('защита', null=True, blank=True)
    stamina = models.IntegerField('выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} ({self.latitude}, {self.longitude})'
