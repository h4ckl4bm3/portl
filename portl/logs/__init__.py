from flask import Blueprint

bp = Blueprint(
    "logs_blueprint",
    __name__,
    url_prefix="/logs",
    template_folder="templates",
    static_folder="static",
)

from portl.functions import add_classes
from portl.logs.models import Log, LogRule, SyslogServer

add_classes(Log, LogRule, SyslogServer)

import portl.logs.routes  # noqa: F401
