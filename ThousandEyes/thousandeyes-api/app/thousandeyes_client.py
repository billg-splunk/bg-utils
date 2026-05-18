import os
from typing import Any

import requests

THOUSANDEYES_API_BASE = "https://api.thousandeyes.com/v7"


class ThousandEyesError(Exception):
    def __init__(self, message: str, status_code: int | None = None, details: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details


class ThousandEyesClient:
    def __init__(
        self,
        api_token: str | None = None,
        account_group_id: str | None = None,
        default_role_ids: list[str] | None = None,
        login_account_group_id: str | None = None,
    ):
        self.api_token = api_token or os.environ.get("THOUSANDEYES_API_TOKEN", "")
        self.account_group_id = account_group_id or os.environ.get("THOUSANDEYES_ACCOUNT_GROUP_ID")
        self.login_account_group_id = login_account_group_id or os.environ.get(
            "THOUSANDEYES_LOGIN_ACCOUNT_GROUP_ID"
        )
        role_ids_env = os.environ.get("THOUSANDEYES_DEFAULT_ROLE_IDS", "")
        self.default_role_ids = default_role_ids or [
            role_id.strip() for role_id in role_ids_env.split(",") if role_id.strip()
        ]

        if not self.api_token:
            raise ValueError("THOUSANDEYES_API_TOKEN is required")

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/hal+json",
        }

    def _get(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        response = requests.get(
            f"{THOUSANDEYES_API_BASE}{path}",
            headers=self._headers(),
            params=params or None,
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()

        details: Any
        try:
            details = response.json()
        except ValueError:
            details = response.text

        raise ThousandEyesError(
            f"ThousandEyes API returned {response.status_code} for {path}",
            status_code=response.status_code,
            details=details,
        )

    def _post(
        self, path: str, payload: dict[str, Any], params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        response = requests.post(
            f"{THOUSANDEYES_API_BASE}{path}",
            headers=self._headers(),
            json=payload,
            params=params or None,
            timeout=30,
        )

        if response.status_code in (200, 201):
            if not response.content:
                return {}
            return response.json()

        details: Any
        try:
            details = response.json()
        except ValueError:
            details = response.text

        raise ThousandEyesError(
            f"ThousandEyes API returned {response.status_code} for {path}",
            status_code=response.status_code,
            details=details,
        )

    def list_account_groups(self) -> list[dict[str, Any]]:
        data = self._get("/account-groups")
        return data.get("accountGroups", [])

    def list_roles(self, account_group_id: str | None = None) -> list[dict[str, Any]]:
        params = {"aid": account_group_id} if account_group_id else None
        data = self._get("/roles", params=params)
        return data.get("roles", [])

    def list_users(self, account_group_id: str | None = None) -> list[dict[str, Any]]:
        params = {"aid": account_group_id} if account_group_id else None
        data = self._get("/users", params=params)
        return data.get("users", [])

    def get_settings_info(self) -> dict[str, Any]:
        account_groups = self.list_account_groups()

        default_group = next(
            (group for group in account_groups if group.get("isDefaultAccountGroup")),
            None,
        )
        current_group = next(
            (group for group in account_groups if group.get("isCurrentAccountGroup")),
            None,
        )
        suggested_account_group = default_group or current_group or (
            account_groups[0] if account_groups else None
        )
        suggested_aid = suggested_account_group.get("aid") if suggested_account_group else None

        account_group_options = [
            {
                "value": group.get("aid"),
                "label": group.get("accountGroupName"),
                "organization_name": group.get("organizationName"),
                "org_id": group.get("orgId"),
                "is_default_account_group": group.get("isDefaultAccountGroup", False),
                "is_current_account_group": group.get("isCurrentAccountGroup", False),
            }
            for group in account_groups
            if group.get("aid")
        ]

        roles: list[dict[str, Any]] = []
        roles_error: dict[str, Any] | None = None
        try:
            roles = self.list_roles(account_group_id=suggested_aid)
        except ThousandEyesError as exc:
            roles_error = {
                "message": str(exc),
                "status_code": exc.status_code,
                "details": exc.details,
            }

        role_options = [
            {
                "value": role.get("roleId"),
                "label": role.get("name"),
                "is_builtin": role.get("isBuiltin", False),
                "has_management_permissions": role.get("hasManagementPermissions", False),
            }
            for role in roles
            if role.get("roleId")
        ]

        builtin_regular = next(
            (
                role
                for role in role_options
                if role.get("is_builtin") and role.get("label") == "Regular User"
            ),
            None,
        )
        suggested_role_id = (
            builtin_regular.get("value")
            if builtin_regular
            else (role_options[0].get("value") if role_options else None)
        )

        users_sample: list[dict[str, Any]] = []
        users_error: dict[str, Any] | None = None
        try:
            users = self.list_users(account_group_id=suggested_aid)
            users_sample = [
                {
                    "email": user.get("email"),
                    "name": user.get("name"),
                    "uid": user.get("uid"),
                    "login_account_group": user.get("loginAccountGroup"),
                }
                for user in users[:5]
            ]
        except ThousandEyesError as exc:
            users_error = {
                "message": str(exc),
                "status_code": exc.status_code,
                "details": exc.details,
            }

        return {
            "current_config": {
                "THOUSANDEYES_API_TOKEN": "configured" if self.api_token else "missing",
                "THOUSANDEYES_ACCOUNT_GROUP_ID": self.account_group_id or None,
                "THOUSANDEYES_LOGIN_ACCOUNT_GROUP_ID": self.login_account_group_id or None,
                "THOUSANDEYES_DEFAULT_ROLE_IDS": (
                    ",".join(self.default_role_ids) if self.default_role_ids else None
                ),
            },
            "settings": {
                "THOUSANDEYES_ACCOUNT_GROUP_ID": {
                    "description": (
                        "Account group context for API calls (ThousandEyes aid query parameter). "
                        "Omit if you only have one account group."
                    ),
                    "suggested_value": suggested_aid,
                    "options": account_group_options,
                },
                "THOUSANDEYES_LOGIN_ACCOUNT_GROUP_ID": {
                    "description": (
                        "Account group where new users land when they sign in "
                        "(loginAccountGroupId). Usually the same aid as THOUSANDEYES_ACCOUNT_GROUP_ID."
                    ),
                    "suggested_value": suggested_aid,
                    "options": account_group_options,
                },
                "THOUSANDEYES_DEFAULT_ROLE_IDS": {
                    "description": (
                        "Comma-separated role IDs assigned to new users "
                        "(allAccountGroupRoleIds). Use roleId values from the options list."
                    ),
                    "suggested_value": suggested_role_id,
                    "options": role_options,
                },
            },
            "hints": {
                "default_account_group": default_group,
                "current_account_group": current_group,
            },
            "users_sample": users_sample,
            "errors": {
                key: value
                for key, value in {
                    "roles": roles_error,
                    "users": users_error,
                }.items()
                if value
            },
        }

    def create_user(self, email: str, name: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"email": email}

        if name:
            payload["name"] = name
        elif "@" in email:
            payload["name"] = email.split("@", 1)[0]

        if self.login_account_group_id:
            payload["loginAccountGroupId"] = self.login_account_group_id

        if self.default_role_ids:
            payload["allAccountGroupRoleIds"] = self.default_role_ids

        params = {}
        if self.account_group_id:
            params["aid"] = self.account_group_id

        return self._post("/users", payload=payload, params=params or None)
