from re import findall

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text

from portl.automation.functions import NETMIKO_DRIVERS
from portl.automation.models import Service
from portl.classes import service_classes
from portl.extensions import DB_STRING_LENGTH
from portl.inventory.models import Device


class NetmikoDataExtractionService(Service):
    __tablename__ = "NetmikoDataExtractionService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    has_targets = True
    variable1 = Column(String(255), default="")
    command1 = Column(String(255), default="")
    regular_expression1 = Column(Text(), default="")
    variable2 = Column(String(255), default="")
    command2 = Column(String(255), default="")
    regular_expression2 = Column(Text(), default="")
    variable3 = Column(String(255), default="")
    command3 = Column(String(255), default="")
    regular_expression3 = Column(Text(), default="")
    driver = Column(String(255), default="")
    driver_values = NETMIKO_DRIVERS
    use_device_driver = Column(Boolean, default=True)
    fast_cli = Column(Boolean, default=False)
    timeout = Column(Integer, default=10.0)
    delay_factor = Column(Float, default=1.0)
    global_delay_factor = Column(Float, default=1.0)

    __mapper_args__ = {"polymorphic_identity": "NetmikoDataExtractionService"}

    def job(self, payload: dict, device: Device) -> dict:
        netmiko_handler = self.netmiko_connection(device)
        result, success = {}, True
        for i in range(1, 4):
            variable = getattr(self, f"variable{i}")
            regular_expression = getattr(self, f"regular_expression{i}")
            if not variable:
                continue
            command = self.sub(getattr(self, f"command{i}"), locals())
            self.logs.append(f"Sending '{command}' on {device.name} (Netmiko)")
            output = netmiko_handler.send_command(
                command, delay_factor=self.delay_factor
            )
            match = findall(regular_expression, output)
            if not match:
                success = False
            result[variable] = {
                "command": command,
                "regular_expression": regular_expression,
                "output": output,
                "value": match,
            }
        netmiko_handler.disconnect()
        return {"result": result, "success": True}


service_classes["NetmikoDataExtractionService"] = NetmikoDataExtractionService
