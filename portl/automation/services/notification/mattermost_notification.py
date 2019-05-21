from json import dumps

from requests import post
from sqlalchemy import Column, ForeignKey, Integer, String, Text

from portl.automation.models import Service
from portl.classes import service_classes
from portl.extensions import DB_STRING_LENGTH
from portl.functions import get_one


class MattermostNotificationService(Service):
    __tablename__ = "MattermostNotificationService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    channel = Column(String(255), default="")
    body = Column(Text(), default="")
    body_textarea = True

    __mapper_args__ = {"polymorphic_identity": "MattermostNotificationService"}

    def job(self, _) -> dict:
        parameters = get_one("Parameters")
        channel = self.channel or parameters.mattermost_channel
        self.logs.append(f"Sending Mattermost notification on {channel}")
        result = post(
            parameters.mattermost_url,
            verify=parameters.mattermost_verify_certificate,
            data=dumps({"channel": channel, "text": self.body}),
        )
        return {"success": True, "result": str(result)}


service_classes["MattermostNotificationService"] = MattermostNotificationService
