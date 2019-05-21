from flask import Blueprint

bp = Blueprint(
    "scheduling_blueprint",
    __name__,
    url_prefix="/scheduling",
    template_folder="templates",
    static_folder="static",
)

from portl.functions import add_classes
from portl.scheduling.models import Task

add_classes(Task)

import portl.scheduling.routes  # noqa: F401
