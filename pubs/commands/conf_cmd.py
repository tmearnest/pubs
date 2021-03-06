from .. import uis
from .. import config
from .. import content


def parser(subparsers):
    parser = subparsers.add_parser('conf',
            help='open the configuration in an editor')
    return parser


def command(conf, args):
    uis.init_ui(conf)
    ui = uis.get_ui()

    while True:
        # get modif from user
        content.edit_file(conf['main']['edit_cmd'], config.get_confpath())

        new_conf = config.load_conf(check=False)
        try:
            config.check_conf(new_conf)
            ui.message('The configuration file was updated.')
            break
        except AssertionError as e: # TODO better error message
            ui.error('Error reading the modified configuration file [' + e.message + '].')
            options = ['edit_again', 'abort']
            choice = options[ui.input_choice(
                options, ['e', 'a'],
                question=('Edit again or abort? If you abort, the changes will be reverted.')
                )]

            if choice == 'abort':
                config.save_conf(conf)
                ui.message('The changes have been reverted.')
                break
