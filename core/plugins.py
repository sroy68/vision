PLUGINS_ENABLED = False

def enable_plugins(owner_confirm=False):
    global PLUGINS_ENABLED
    if owner_confirm:
        PLUGINS_ENABLED = True

def freeze_all():
    global PLUGINS_ENABLED
    PLUGINS_ENABLED = False
