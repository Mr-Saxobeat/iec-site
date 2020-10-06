from vismet.models import ElementCategory

def run():
    ElementCategory.objects.get_or_create(
        name = 'observados',
    )

    ElementCategory.objects.get_or_create(
        name = 'reanálise',
    )

    ElementCategory.objects.get_or_create(
        name = 'simulados',
    )
