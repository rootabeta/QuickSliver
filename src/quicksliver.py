import os
import asyncio
import logging
from sliver import SliverClientConfig
from config_selector_ui import selectConfig
from client_ui import launchClient
from argparse import ArgumentParser
import ttkbootstrap as ttk
from PIL import Image, ImageTk

formatter = "[%(levelname)s] %(message)s"
log = logging.getLogger(__name__)

def fetch_configs(CONFIG_DIR):
    configs = {}  # name, path
    for file in os.listdir(CONFIG_DIR):
        if file.endswith(".cfg"):
            try:
                config = SliverClientConfig.parse_config_file(
                    os.path.join(CONFIG_DIR, file)
                )
            except Exception as _:
                log.warning(f"Failed to load config file {file}")
                continue  # Skip broken config files

            name = "{OPERATOR}@{HOST}:{PORT}".format(
                OPERATOR=config.operator, HOST=config.lhost, PORT=config.lport
            )
            configs[name] = config

    return configs


def main(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=formatter)
    else:
        logging.basicConfig(level=logging.INFO, format=formatter)

    app = ttk.Window(themename="darkly")
    
    # Get absolute path of currently-executing file, so cwd of invoking script is irrelevant
    dirname, _ = os.path.split(os.path.abspath(__file__))
    
    # Backtrack into img to fetch icon
    ico = Image.open(os.path.join(dirname, "..", "img", "QuickSliver.png"))
    
    # Set program icon
    photo = ImageTk.PhotoImage(ico)
    app.wm_iconphoto(False, photo)

    app.withdraw()
    # User has not specified a specific config to use
    if not args.config:
        CONFIG_DIR = args.config_path
        try:
            configs = fetch_configs(CONFIG_DIR)
        except:
            log.error("Failed during config file detection")
            exit()

        # No configs found
        if len(configs) == 0:
            log.critical("No configuration files found")
            exit()

        # One, and only one, config found by autodetect
        elif len(configs) == 1:
            log.debug("Only one config found")
            config_name = list(configs.keys())[0]

        # Multiple configs found by autodetect - ask the user
        else:
            config_name = selectConfig(app, configs)

        if config_name:
            log.debug(f"Selected config {config_name}")
            config = configs[config_name]
        else:
            log.debug("User aborted config selection")
            exit()

    else:
        try:
            config = SliverClientConfig.parse_config_file(args.config)
        except Exception as _:
            log.critical("Failed to load custom config file")
            exit()

    #launchClient(app, log, config)
    client = launchClient(app, log, config)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="QuickSliver", description="A graphical frontend for Sliver"
    )

    parser.add_argument(
        "--config-path",
        default=os.path.join(os.path.expanduser("~"), ".sliver-client", "configs"),
        metavar="PATH",
        help="directory containing sliver configuration files (default ~/.sliver-client/configs/)",
    )

    parser.add_argument(
        "-c", "--config", metavar="CONFIG", help="specific config file to use"
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug output"
    )

    args = parser.parse_args()

    main(args)
