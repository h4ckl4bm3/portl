from flask import Blueprint

bp = Blueprint(
    "admin_blueprint",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
    static_folder="static",
)

from portl.functions import add_classes
from portl.admin.models import Instance, User, Parameters

add_classes(Instance, User, Parameters)

import portl.admin.routes  # noqa: F401
