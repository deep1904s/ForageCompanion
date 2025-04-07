from utils.logger import logger
from config import Config

app_config = Config()


def allowed_file(filename):
    is_allowed = (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app_config.ALLOWED_EXTENSIONS
    )
    logger.debug("Checking file extension: %s - Allowed: %s", filename, is_allowed)
    return is_allowed
