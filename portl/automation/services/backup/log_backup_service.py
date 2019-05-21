from datetime import datetime
from json import dump
from os import makedirs, remove
from pathlib import Path
from shutil import rmtree
from tarfile import open as open_tar

from paramiko import SSHClient, AutoAddPolicy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from portl.automation.models import Service
from portl.classes import service_classes
from portl.functions import fetch_all, strip_all
from portl.inventory.models import Device


class LogBackupService(Service):
    __tablename__ = "LogBackupService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    has_targets = True
    direction = "put"
    protocol = Column(String(255), default="")
    protocol_values = (("scp", "SCP"), ("sftp", "SFTP"))
    delete_folder = Column(Boolean, default=False)
    delete_archive = Column(Boolean, default=False)
    destination_path = Column(String(255), default="")

    __mapper_args__ = {"polymorphic_identity": "LogBackupService"}

    def job(self, payload: dict, device: Device) -> dict:
        path_backup = Path.cwd() / "logs" / "job_logs"
        now = strip_all(str(datetime.now()))
        path_dir = path_backup / f"logs_{now}"
        source = path_backup / f"logs_{now}.tgz"
        makedirs(path_dir)
        for job in fetch_all("Job"):
            with open(path_dir / f"{job.name}.json", "w") as log_file:
                dump(job.logs, log_file)
        with open_tar(source, "w:gz") as tar:
            tar.add(path_dir, arcname="/")
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(
            device.ip_address,
            username=device.username,
            password=device.password,
            look_for_keys=False,
        )
        destination = f"{self.destination_path}/logs_{now}.tgz"
        self.transfer_file(ssh_client, [(source, destination)])
        ssh_client.close()
        if self.delete_folder:
            rmtree(path_dir)
        if self.delete_archive:
            remove(source)
        return {
            "success": True,
            "result": f"logs stored in {destination} ({device.ip_address})",
        }


service_classes["LogBackupService"] = LogBackupService
