from flask import Blueprint

bp = Blueprint(
    "automation_blueprint",
    __name__,
    url_prefix="/automation",
    template_folder="templates",
    static_folder="static",
)

from portl.automation.models import Job, Service, Workflow, WorkflowEdge
from portl.functions import add_classes

add_classes(Job, Service, Workflow, WorkflowEdge)

import portl.automation.routes  # noqa: F401
