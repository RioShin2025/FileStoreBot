from pyromod import listen  # ✅ MUST be before importing Bot

try:
    from Bot import Bot
except ModuleNotFoundError:
    try:
        from bot import Bot
    except ModuleNotFoundError:
        try:
            from plugins.Bot import Bot
        except ModuleNotFoundError:
            from plugins.bot import Bot

from pyromod.listen import ListenerTypes

if __name__ == "__main__":
    app = Bot()

    # ✅ Prevent KeyError even if something resets listeners
    app.listeners.setdefault(ListenerTypes.MESSAGE, [])
    app.listeners.setdefault(ListenerTypes.CALLBACK_QUERY, [])

    app.run()
