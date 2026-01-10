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

if __name__ == "__main__":
    Bot().run()
