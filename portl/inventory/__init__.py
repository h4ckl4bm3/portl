from flask import Blueprint

bp = Blueprint(
    "inventory_blueprint",
    __name__,
    url_prefix="/inventory",
    template_folder="templates",
    static_folder="static",
)

from portl.functions import add_classes
from portl.inventory.models import Device, Link, Object, Pool

add_classes(Device, Link, Object, Pool)

import portl.inventory.routes  # noqa: F401
