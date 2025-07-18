# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Serve logs process."""

from __future__ import annotations

import logging
import socket
import sys

import uvicorn

from airflow.configuration import conf

logger = logging.getLogger(__name__)


def serve_logs(port=None):
    """Serve logs generated by Worker."""
    # setproctitle causes issue on Mac OS: https://github.com/benoitc/gunicorn/issues/3021
    os_type = sys.platform
    if os_type == "darwin":
        logger.debug("Mac OS detected, skipping setproctitle")
    else:
        from setproctitle import setproctitle

        setproctitle("airflow serve-logs")

    port = port or conf.getint("logging", "WORKER_LOG_SERVER_PORT")

    # If dual stack is available and IPV6_V6ONLY is not enabled on the socket
    # then when IPV6 is bound to it will also bind to IPV4 automatically
    if getattr(socket, "has_dualstack_ipv6", lambda: False)():
        host = "::"  # ASGI uses `::` syntax for IPv6 binding instead of the `[::]` notation used in WSGI, while preserving the `[::]` format in logs
        serve_log_uri = f"http://[::]:{port}"
    else:
        host = "0.0.0.0"
        serve_log_uri = f"http://{host}:{port}"

    logger.info("Starting log server on %s", serve_log_uri)

    # Use uvicorn directly for ASGI applications
    uvicorn.run("airflow.utils.serve_logs.log_server:app", host=host, port=port, workers=2, log_level="info")
    # Note: if we want to use more than 1 workers, we **can't** use the instance of FastAPI directly
    # This is way we split the instantiation of log server to a separate module
    #
    # https://github.com/encode/uvicorn/blob/374bb6764e8d7f34abab0746857db5e3d68ecfdd/docs/deployment/index.md?plain=1#L50-L63


if __name__ == "__main__":
    serve_logs()
