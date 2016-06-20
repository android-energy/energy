import argparse

import os.path

from modem import Modem
from model import Model
from emulator import Emulator


def main():
    # objs/emulator -verbose @Nexus4

    parser = argparse.ArgumentParser()
    parser.add_argument('--emu-path', default=os.path.abspath('../qemu/obj/emulator'),
                        help='emulator path')
    parser.add_argument('emu_args', default=['-verbose', '@Nexus4'], nargs='*',
                        help='args for the emulator. e.g: @Nexus4')
    args = parser.parse_args()

    device = Emulator(args.emu_path, *args.emu_args)
    model = Model(device)

    modem = Modem()
    model.add_component('modem_driver_read', modem)

    try:
        model.run()
    except (KeyboardInterrupt, SystemExit):
        print("got Ctrl+C (SIGINT) or exit() is called")
        model.stop()

if __name__ == '__main__':
    main()
