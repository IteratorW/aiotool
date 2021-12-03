from typing import Awaitable

handlers: list = []


def postload():
    def decorator(func):
        handlers.append(func)

        return func

    return decorator


async def activate_handlers():
    for handler in handlers:
        await handler()
