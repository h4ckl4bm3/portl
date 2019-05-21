from subprocess import check_output
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from portl.automation.models import Service
from portl.classes import service_classes
from portl.extensions import DB_STRING_LENGTH
from portl.inventory.models import Device


class UnixCommandService(Service):
    __tablename__ = "UnixCommandService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    command = Column(String(255), default="")
    content_match = Column(Text(), default="")
    content_match_textarea = True
    content_match_regex = Column(Boolean, default=False)
    negative_logic = Column(Boolean, default=False)
    delete_spaces_before_matching = Column(Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "UnixCommandService"}

    def job(self, payload: dict, device: Optional[Device] = None) -> dict:
        command = self.sub(self.command, locals())
        match = self.sub(self.content_match, locals())
        self.logs.append(f"Running Unix command ({command}) on {device.name}")
        result = check_output(command.split()).decode()
        return {
            "success": self.match_content(result, match),
            "match": match,
            "negative_logic": self.negative_logic,
            "result": result,
        }


service_classes["UnixCommandService"] = UnixCommandService
