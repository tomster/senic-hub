from cornice.service import Service
from os import path
# TODO: We better rename `config.path` to something else. Conflicts with `os.path`
from ..config import path as service_path


nuimo_setup = Service(
    name='nuimo_setup',
    path=path('setup/nuimo'),
    renderer='json',
    accept='application/json')


@nuimo_setup.get()
def get_nuimo_mac_address(request):
    nuimo_mac_address_filepath = request.registry.settings.get('nuimo_mac_address_filepath')
    if not path.exists(nuimo_mac_address_filepath):
        return []
    with open(nuimo_mac_address_filepath, 'r') as nuimo_mac_address_file:
        mac_address = nuimo_mac_address_file.read().split('\n', 1)[0]
        return {'connectedControllers': [mac_address]}
