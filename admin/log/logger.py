import logging

# create a logger for requests and responses at the admin level
logger = logging.getLogger("admin_requests")

logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("admin/log/admin.log", mode="w")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()

# create the formatter and add to to handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s -" + "%(levelname)s - %(message)s"
)

fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
