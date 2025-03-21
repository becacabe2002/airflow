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
from __future__ import annotations

from flask_appbuilder.security.views import RoleModelView

from airflow.providers.fab.www.security import permissions


class CustomRoleModelView(RoleModelView):
    """Customize permission names for FAB's builtin RoleModelView."""

    class_permission_name = permissions.RESOURCE_ROLE
    method_permission_name = {
        "delete": "delete",
        "download": "read",
        "show": "read",
        "list": "read",
        "edit": "edit",
        "add": "create",
        "copy_role": "create",
    }
    base_permissions = [
        permissions.ACTION_CAN_CREATE,
        permissions.ACTION_CAN_READ,
        permissions.ACTION_CAN_EDIT,
        permissions.ACTION_CAN_DELETE,
    ]
