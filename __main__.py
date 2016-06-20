import argparse

from modem import Modem
from model import Model
from emulator import Emulator

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--emu', default='../qemu/emulator', help='emulator path')
    args = parser.parse_args()

    device = Emulator(args.emu)
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
