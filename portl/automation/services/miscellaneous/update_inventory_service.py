from sqlalchemy import Column, ForeignKey, Integer, PickleType
from sqlalchemy.ext.mutable import MutableDict

from portl.automation.models import Service
from portl.classes import service_classes
from portl.inventory.models import Device


class UpdateInventoryService(Service):
    __tablename__ = "UpdateInventoryService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    has_targets = True
    update_dictionary = Column(MutableDict.as_mutable(PickleType), default={})

    __mapper_args__ = {"polymorphic_identity": "UpdateInventoryService"}

    def job(self, payload: dict, device: Device) -> dict:
        for property, value in self.update_dictionary.items():
            setattr(device, property, value)
        return {"success": True, "result": "properties updated"}


service_classes["UpdateInventoryService"] = UpdateInventoryService
