from cornice.service import Service

from ..config import path


nuimo_setup = Service(
    name='nuimo_setup',
    path=path('setup/nuimo'),
    renderer='json',
    accept='application/json')


@nuimo_setup.get()
def discover_and_connect_nuimo(request):
    return {'aa:bb:cc:dd:ee:ff': {'name': "Nuimo"}}
