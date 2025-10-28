def has_config(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r"):
            return True
    except OSError:
        return False
