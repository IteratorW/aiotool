import asyncio
import logging
import os
import sys

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

    sys.exit()
