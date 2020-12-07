from lechang import settings

def proxy():
    if settings.USE_PROXY:
        return {}
    else:
        return {}