import asyncio
import logging
import os
import sys

import coloredlogs as coloredlogs
from tortoise import Tortoise

from api.extension import extension_handler
from api.filters import custom_filters
from api.menu import menu_handler
from bot import main, env

coloredlogs.install(fmt="[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s", datefmt="%H:%M:%S",
                    field_styles={"levelname": {"color": "blue"}, "message": {"color": "white", "bright": True}})
logging.basicConfig(level=logging.INFO)

custom_filters.bind_all()

logging.info("Loading extensions...")

for directory in env.EXTENSION_DIRS:
    if not os.path.isdir(directory):
        os.mkdir(directory)

    for python_module in os.listdir(directory):
        path = f"{directory}.{python_module}"

        extension = getattr(__import__(path, globals(), locals()), python_module)

        if os.path.isfile(f"{directory}/{python_module}/models.py"):
            extension_handler.extensions_models.append(f"{path}.models")

            logging.info(f"Added models for extension {python_module}")

        logging.info(f"Loaded extension {python_module}")


logging.info("Processing menu")

menu_handler.register_handlers()


logging.info("Running async...")

loop = asyncio.new_event_loop()
asyncio.ensure_future(main.run(), loop=loop)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    logging.info("Shitdown")

    loop.run_until_complete(main.executor._shutdown_polling())

    loop.run_until_complete(Tortoise.close_connections())
