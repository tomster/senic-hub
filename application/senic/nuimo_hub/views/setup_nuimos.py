from cornice.service import Service
from os import path
# TODO: We better rename `config.path` to something else. Conflicts with `os.path`
from ..config import path as service_path
from ..subprocess_run import run


nuimo_setup_starter = Service(
    name='start_nuimo_setup',
    path=service_path('setup/nuimos/start'),
    renderer='json',
    accept='application/json')


connected_nuimos = Service(
    name='connected_nuimos',
    path=service_path('setup/nuimos'),
    renderer='json',
    accept='application/json')


# TODO: Remove get()
@nuimo_setup_starter.get()
@nuimo_setup_starter.post(renderer='json')
def start_nuimo_setup(request):
    # TODO: Collect config file from some settings
    # TODO: Collect Bluetooth adapter name from some settings
    # TODO: Should be started via supervisorctl to avoid multiple instances running
    run([
        'sudo',
        path.join(request.registry.settings['fs_bin'], 'setup_nuimo'),
        '-c', '/srv/nuimo_hub/production.ini',
        'hci0'
    ])
    return {}


@connected_nuimos.get()
def get_nuimo_mac_address(request):
    nuimo_mac_address_filepath = request.registry.settings.get('nuimo_mac_address_filepath')
    if not path.exists(nuimo_mac_address_filepath):
        return []
    with open(nuimo_mac_address_filepath, 'r') as nuimo_mac_address_file:
        mac_address = nuimo_mac_address_file.read().split('\n', 1)[0]
        return {'connectedControllers': [mac_address]}