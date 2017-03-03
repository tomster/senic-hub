from cornice.service import Service
from os import path
# TODO: We better rename `config.path` to something else. Conflicts with `os.path`
from ..config import path as service_path
from ..subprocess_run import run


nuimo_bootstrap = Service(
    name='start_nuimo_setup',
    path=service_path('setup/nuimos/bootstrap'),
    renderer='json',
    accept='application/json')


connected_nuimos = Service(
    name='connected_nuimos',
    path=service_path('setup/nuimos'),
    renderer='json',
    accept='application/json')


# TODO: Remove get()
@nuimo_bootstrap.get()
@nuimo_bootstrap.post(renderer='json')
def bootstrap_nuimos(request):
    # TODO: Collect Bluetooth adapter name from some settings
    run([
        'sudo',
        path.join(request.registry.settings['fs_bin'], 'setup_nuimo'),
        '-o', request.registry.settings['nuimo_mac_address_filepath'],
        'hci0'
    ])
    return get_nuimo_mac_address(request)


@connected_nuimos.get()
def get_nuimo_mac_address(request):
    nuimo_mac_address_filepath = request.registry.settings.get('nuimo_mac_address_filepath')
    if not path.exists(nuimo_mac_address_filepath):
        return []
    with open(nuimo_mac_address_filepath, 'r') as nuimo_mac_address_file:
        mac_address = nuimo_mac_address_file.read().split('\n', 1)[0]
        return {'connectedControllers': [mac_address]}
