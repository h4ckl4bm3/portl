from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text

from portl.automation.functions import NETMIKO_DRIVERS
from portl.automation.models import Service
from portl.classes import service_classes
from portl.extensions import DB_STRING_LENGTH
from portl.inventory.models import Device


class NetmikoConfigurationService(Service):
    __tablename__ = "NetmikoConfigurationService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    has_targets = True
    content = Column(Text(), default="")
    content_textarea = True
    driver = Column(String(255), default="")
    driver_values = NETMIKO_DRIVERS
    use_device_driver = Column(Boolean, default=True)
    enable_mode = Column(Boolean, default=False)
    fast_cli = Column(Boolean, default=False)
    timeout = Column(Integer, default=1.0)
    delay_factor = Column(Float, default=1.0)
    global_delay_factor = Column(Float, default=1.0)

    __mapper_args__ = {"polymorphic_identity": "NetmikoConfigurationService"}

    def job(self, payload: dict, device: Device) -> dict:
        netmiko_handler = self.netmiko_connection(device)
        if self.enable_mode:
            netmiko_handler.enable()
        config = self.sub(self.content, locals())
        self.logs.append(f"Pushing configuration on {device.name} (Netmiko)")
        netmiko_handler.send_config_set(
            config.splitlines(), delay_factor=self.delay_factor
        )
        netmiko_handler.disconnect()
        return {"success": True, "result": f"configuration OK {config}"}


service_classes["NetmikoConfigurationService"] = NetmikoConfigurationService
