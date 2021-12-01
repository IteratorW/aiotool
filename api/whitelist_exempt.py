def whitelist_exempt():
    def decorator(func):
        setattr(func, "whitelist_exempted", True)

        return func

    return decorator
