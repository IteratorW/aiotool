import logging
import os

import coloredlogs as coloredlogs

from bot import main, const

coloredlogs.install(fmt="[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s", datefmt="%H:%M:%S",
                    field_styles={"levelname": {"color": "blue"}, "message": {"color": "white", "bright": True}})
logging.basicConfig(level=logging.INFO)

logging.info("Loading extensions...")

for directory in const.EXT_DIRS:
    if not os.path.isdir(directory):
        os.mkdir(directory)

    for python_module in os.listdir(directory):
        path = f"{directory}.{python_module}"

        extension = getattr(__import__(path, globals(), locals()), python_module)

        logging.info(f"Loaded extension {python_module}")

logging.info("Running aiogram...")

main.run()
