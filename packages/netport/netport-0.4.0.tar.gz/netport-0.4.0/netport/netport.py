# pylint: disable-import-outside-toplevel
"""Netport fastapi server.

Contains all netport functionalities.
"""
import os
import re
import uuid
import socket
import platform
import subprocess
from os.path import exists

import psutil
from loguru import logger
from fastapi import FastAPI, Request
from redis import exceptions as redis_errors

from netport.common import R_PORT, R_PATH, R_PROCESS, Response
from netport.database import RedisDatabase, LocalDatabase, IDatabase

app = FastAPI()
running_processes = []
db: IDatabase = NotImplemented


def _is_port_in_use(port: int):
    """Checks if the given port is in use.

    Args:
        port (int): The port to check

    Returns:
        bool. If the port is in use.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


@app.get("/db/reserve")
def reserve(request: Request, resource: str, value):
    result = db.reserve(client_ip=request.client.host, resource=resource, value=value)
    return Response(data=result)


@app.get("/db/is_reserved")
def is_reserved(resource: str, value: str):
    """Check if the given resource is in use.

    Args:
        resource (str): The resource type
        value (str): The value of the resource

    Returns:
        bool. If the port is in use.
    """
    return Response(data=db.is_reserved(resource, value))


@app.get("/db/my_resources")
def my_resources(request: Request, resource: str):
    """Get all resources that are reserved to the client."""
    return Response(data=db.get_client_resources(request.client.host, resource))


@app.get("/db/get_client_resources")
def get_client_resources(
    request: Request,
    client_ip: str = None,
    resource: str = r"(.)+",
    value: str = r"(.)+",
):
    """Get all resources that are reserved for a specific client."""
    if not client_ip:
        client_ip = request.client.host

    return Response(data=db.get_client_resources(client_ip, resource, value))


@app.get("/db/release_resource")
def release_resource(request: Request, resource: str, value):
    """Release a resource for the requesting client."""
    return Response(data=db.release_resource(request.client.host, resource, value) == 1)


@app.get("/db/release_client")
def release_client(request: Request, client: str = None):
    """Release all resources that are reserved for the requesting client."""
    if client:
        return db.release_client(client) == 1

    return Response(db.release_client(request.client.host) == 1)


@app.get("/db/get_all_resources")
def get_all_resources():
    """Get all clients that hold resources."""
    return Response(data=db.get_all_resources())


@app.get("/db/get_all_clients")
def get_all_clients():
    """Get all clients that hold resources."""
    return Response(data=db.get_all_clients())


@app.get("/networking/get_port")
def get_port(request: Request, port: int = None):
    """Get an empty port.

    Opens a socket on random port, gets its port number, and closes the socket.

    This action is not atomic, so race condition is possible...
    """
    if port and not _is_port_in_use(port):
        if db.reserve(request.client.host, R_PORT, port):
            return Response(data={"port": port})

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        _, port = s.getsockname()
        if db.reserve(request.client.host, R_PORT, port):
            return Response(data={"port": port})

    return Response(data=False)


@app.get("/networking/is_port_in_use")
def is_port_in_use(port: int):
    """Checks if the given port is in use.

    Args:
        port (int): The port to use

    Returns:
        bool. If the port is in use.
    """
    return Response(data=_is_port_in_use(port))


@app.get("/networking/whats_my_ip")
def whats_my_ip(request: Request):
    """Check how netport sees the client's ip."""
    return Response(data=request.client.host)


@app.get("/networking/list_interfaces")
def list_interfaces():
    """List all available network interfaces.

    Returns:
        list. Network interfaces.
    """
    interfaces = psutil.net_if_addrs()
    return Response(data=list(interfaces.keys()))


@app.get("/fs/is_path_exist")
def is_path_exist(path: str):
    """Check if the given path exists on the machine."""
    return Response(data=exists(path.strip()))


@app.get("/fs/reserve_path")
def reserve_path(request: Request, path: str):
    """Reserve a path for the client."""
    if not exists(path):
        return Response(data=False)

    return Response(data=db.reserve(request.client.host, R_PATH, path))


@app.get("/shell/execute_command")
def execute_command(command: str):
    """Run a shell command and returns its result."""
    return Response(
        data=subprocess.call(
            command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        == 0
    )


@app.get("/shell/run_process")
def run_process(request: Request, command: str):
    """Run a process on the machine."""
    if db.reserve(request.client.host, R_PROCESS, command):
        process = subprocess.Popen(command.split(" "))
        running_processes.append(process)
        return Response(data=process.pid)

    return Response(data=-1)


@app.get("/shell/is_process_running")
def is_process_running(name: str):
    """Check if the process already runs."""
    for proc in psutil.process_iter():
        try:
            if name.lower() in proc.name().lower():
                return Response(data=proc.name())

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return Response(data=False)


@app.get("/system/get_system_info")
def get_system_info():
    return Response(
        data={
            "platform": platform.system(),
            "platform-release": platform.release(),
            "platform-version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "ip-address": socket.gethostbyname(socket.gethostname()),
            "mac-address": ":".join(re.findall("..", "%012x" % uuid.getnode())),
            "processor": platform.processor(),
            "ram": str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB",
        }
    )


def run_app():
    global db
    redis_host = os.environ.get("NETPORT_REDIS_HOST", None)
    redis_port = os.environ.get("NETPORT_REDIS_PORT", None)
    redis_db = os.environ.get("NETPORT_REDIS_DB", None)

    try:
        if None in [redis_host, redis_port, redis_db]:
            raise AttributeError

        db = RedisDatabase(host=redis_host, port=redis_port, db_instance=redis_db)
        logger.success(
            f"Connected to Redis database at {redis_host}:{redis_port},{redis_db}"
        )

    except AttributeError:
        db = LocalDatabase()
        logger.success("Initiated a local database")

    except (redis_errors.ConnectionError, TypeError) as error:
        msg = (
            f"Couldn't connect to the redis database due to bad parameters: host={redis_host}, "
            f"port={redis_port}, db={redis_db}."
        )

        logger.error(msg)
        raise ConnectionError(msg) from error

    return app


if __name__ == "__main__":
    run_app()
