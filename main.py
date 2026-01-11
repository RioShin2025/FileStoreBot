from pyromod import listen  # MUST be before importing Bot

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


    # ✅ Works in old/new pyromod (no ListenerTypes import)
    app.listeners.setdefault("message", [])
    app.listeners.setdefault("callback_query", [])

    app.run()
if __name__ == "__main__":
    Bot.run()
