from datetime import datetime
from os import remove
from pathlib import Path
from shutil import rmtree
from tarfile import open as open_tar

from paramiko import SSHClient, AutoAddPolicy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from portl.admin.functions import migrate_export
from portl.automation.models import Service
from portl.classes import service_classes
from portl.functions import strip_all
from portl.inventory.models import Device
from portl.properties import import_properties


class DatabaseBackupService(Service):
    __tablename__ = "DatabaseBackupService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    has_targets = True
    direction = "put"
    protocol = Column(String(255), default="")
    protocol_values = (("scp", "SCP"), ("sftp", "SFTP"))
    delete_folder = Column(Boolean, default=False)
    delete_archive = Column(Boolean, default=False)
    destination_path = Column(String(255), default="")

    __mapper_args__ = {"polymorphic_identity": "DatabaseBackupService"}

    def job(self, payload: dict, device: Device) -> dict:
        now = strip_all(str(datetime.now()))
        source = Path.cwd() / "migrations" / f"backup_{now}.tgz"
        migrate_export(
            Path.cwd(),
            {"import_export_types": list(import_properties), "name": f"backup_{now}"},
        )
        with open_tar(source, "w:gz") as tar:
            tar.add(Path.cwd() / "migrations" / f"backup_{now}", arcname="/")
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(
            device.ip_address,
            username=device.username,
            password=device.password,
            look_for_keys=False,
        )
        destination = f"{self.destination_path}/backup_{now}.tgz"
        self.transfer_file(ssh_client, [(source, destination)])
        ssh_client.close()
        if self.delete_folder:
            rmtree(Path.cwd() / "migrations" / f"backup_{now}")
        if self.delete_archive:
            remove(source)
        return {
            "success": True,
            "result": f"backup stored in {destination} ({device.ip_address})",
        }


service_classes["DatabaseBackupService"] = DatabaseBackupService
