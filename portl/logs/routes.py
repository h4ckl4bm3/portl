from flask import request

from portl.functions import get, serialize
from portl.logs import bp
from portl.logs.forms import LogAutomationForm
from portl.properties import log_public_properties, log_rule_table_properties


@get(bp, "/log_management", "View")
def log_management() -> dict:
    return dict(fields=log_public_properties, logs=serialize("Log"))


@get(bp, "/log_automation", "View")
def log_automation() -> dict:
    return dict(
        log_automation_form=LogAutomationForm(request.form),
        fields=log_rule_table_properties,
        log_rules=serialize("LogRule"),
    )
