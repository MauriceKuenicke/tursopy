import json
from typing import TYPE_CHECKING, List, Literal, Optional

import requests

from .dataclasses import ConfigUpdateResponse, DatabaseCreated, DatabaseRead, DbInstance, StatQuery, UsageRead
from .endpoints import API_PATH
from .exceptions import TursoRequestException

if TYPE_CHECKING:
    import tursopy

OptStr = Optional[str]
OptBool = Optional[bool]


class DatabasesClient:
    """
    Databases client managing the databases endpoints.
    """

    def __init__(self, base_client: "tursopy.TursoClient") -> None:
        """
        Initialize the database client for api request management.
        :param base_client: Base TursoClient.
        """
        self.client = base_client

    def generate_token(self, org_name: str, db_name: str) -> str:
        """
        Generates an authorization token for the specified database.
        TODO: Add attach body
        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :return: JWT token
        """
        endpoint = API_PATH["generate_db_token"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint
        response = requests.post(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content!r}")

        content = response.json()
        res: str = content["jwt"]
        return res

    def invalidate_tokens(self, org_name: str, db_name: str) -> None:
        """
        Invalidates all authorization tokens for the specified database.
        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :return: None
        """
        endpoint = API_PATH["invalidate_tokens"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint
        response = requests.post(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content!r}")

    def list_databases(self, org_name: str) -> List[DatabaseRead]:
        """
        Return a list of databases belonging to the organization or user.
        :param org_name: Organization or username.
        :return: List of databases.
        """
        endpoint = API_PATH["list_databases"].format(org_name=org_name)
        request_url = self.client.base_url + endpoint
        response = requests.get(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content!r}")

        content = response.json()
        return [DatabaseRead.load(x) for x in content["databases"]]

    def list_instances(self, org_name: str, db_name: str) -> List[DbInstance]:
        """
        Returns a list of instances of a database. Instances are the individual primary or replica databases in each region defined by the group.
        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :return: List of database instances.
        """
        endpoint = API_PATH["list_instances"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint

        response = requests.get(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()
        return [DbInstance.load(x) for x in content["instances"]]

    def get_instance(self, org_name: str, db_name: str, instance_name: str) -> DbInstance:
        """
        Return the individual database instance by name.
        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :param instance_name: The name of the instance (location code).
        :return: Database Instance
        """
        endpoint = API_PATH["retrieve_instance"].format(org_name=org_name, name=db_name, instance_name=instance_name)
        request_url = self.client.base_url + endpoint

        response = requests.get(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()
        print(content)
        return DbInstance.load(content["instance"])

    def create_database(
        self,
        org_name: str,
        name: str,
        is_schema: OptBool = None,
        schema: OptStr = None,
        seed_name: OptStr = None,
        seed_ts: OptStr = None,
        seed_type: Optional[Literal["database", "dump"]] = None,
        seed_url: OptStr = None,
        size_limit: OptStr = None,
        group: str = "default",
    ) -> DatabaseCreated:
        """
        Creates a new database in a group for the organization or user.

        :param org_name: The name of the organization or user.
        :param name: The name of the new database. Must contain only lowercase letters, numbers, dashes. No longer than 32 characters.
        :param is_schema: Mark this database as the parent schema database that updates child databases with any schema changes.
        :param schema: The name of the parent database to use as the schema. See Multi-DB Schemas.
        :param seed_name: The name of the existing database when database is used as a seed type.
        :param seed_ts: A formatted ISO 8601 recovery point to create a database from. This must be within the last 24 hours, or 30 days on the scaler plan.
        :param seed_type: The type of seed to be used to create a new database. Either 'database' or 'dump'.
        :param seed_url: The URL returned by upload dump can be used with the dump seed type.
        :param size_limit: The maximum size of the database in bytes. Values with units are also accepted, e.g. '1mb', '256mb', '1gb'.
        :param group: The name of the group where the database should be created. The group must already exist. Defaults to 'default'.
        :return: DatabaseCreated
        """
        self._validate_create_database_body_parameters(
            is_schema=is_schema,
            schema=schema,
            seed_type=seed_type,
            seed_name=seed_name,
            seed_url=seed_url,
            seed_ts=seed_ts,
        )

        endpoint = API_PATH["create_database"].format(org_name=org_name)
        request_url = self.client.base_url + endpoint

        data = {
            "name": name,
            "group": group,
        }

        if is_schema is not None:
            data["is_schema"] = is_schema  # type:ignore[assignment]
        if schema:
            data["schema"] = schema
        if size_limit:
            data["size_limit"] = size_limit

        if any([seed_name, seed_ts, seed_url, seed_type]):
            seed_data = {"type": seed_type}

            # At this point we can assume that every parameter set, is part of a valid combination
            if seed_name:
                seed_data["name"] = seed_name  # type:ignore[assignment]
            if seed_ts:
                seed_data["timestamp"] = seed_ts  # type:ignore[assignment]
            if seed_url:
                seed_data["url"] = seed_url  # type:ignore[assignment]

            data["seed"] = seed_data  # type:ignore[assignment]

        response = requests.post(request_url, data=json.dumps(data), headers=self.client.base_header)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()["database"]
        return DatabaseCreated.load(content)

    @staticmethod
    def _validate_create_database_body_parameters(
        is_schema: OptBool,
        schema: OptStr,
        seed_type: Optional[Literal["database", "dump"]],
        seed_name: OptStr,
        seed_url: OptStr,
        seed_ts: OptStr,
    ) -> None:
        """
        Validate the body parameters to be a valid combination of parameters.
        Raises a ValueException upon detection of invalid parameter combinations.
        """
        if is_schema is not None and schema:
            raise ValueError("Can not specify a database as a parent and child database at the same time.")

        if any([seed_name, seed_ts, seed_url, seed_type]):
            if seed_type not in ["database", "dump"]:
                raise ValueError("Seed type needs to be either 'database' or 'dump'.")

            if seed_type == "database" and not seed_name:
                raise ValueError("The name of an existing database when database is used as a seed type is missing.")

            if seed_type == "dump" and not seed_url:
                raise ValueError(
                    "Seed URL missing. The URL returned by upload dump can be used " "with the dump seed type."
                )

            # TODO: What about seed_url + seed_ts?

    def delete_database(self, org_name: str, db_name: str) -> str:
        """
        Delete a database belonging to the organization or user.
        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :return: Name of deleted database.
        """
        endpoint = API_PATH["delete_database"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint

        response = requests.delete(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        deleted_db: str = response.json()["database"]
        return deleted_db

    def retrieve(self, org_name: str, db_name: str) -> DatabaseRead:
        """
        Retrieve database information belonging to the organization or user.
        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :return: DatabaseRead
        """
        endpoint = API_PATH["retrieve_database"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint

        response = requests.get(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()["database"]
        return DatabaseRead.load(content)

    def update(
        self, org_name: str, db_name: str, allow_attach: OptBool = None, size_limit: OptStr = None
    ) -> ConfigUpdateResponse:
        """
        Update a database configuration belonging to the organization or user. A return value of None just declares
        that no value has been updated for that parameter.

        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :param allow_attach: Allow or disallow attaching databases to the current database.
        :param size_limit: The maximum size of the database in bytes. Values with units are also accepted, e.g. 1mb, 256mb, 1gb.
        :return: ConfigUpdateResponse
        """
        endpoint = API_PATH["update_database"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint

        if allow_attach is None and size_limit is None:
            raise ValueError("Either a value for 'allow_attach' or 'size_limit' needs to be given.")

        data = {}
        if allow_attach is not None:
            data["allow_attach"] = allow_attach

        if size_limit is not None:
            data["size_limit"] = size_limit  # type:ignore[assignment]

        response = requests.patch(request_url, headers=self.client.base_header, json=data)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()
        return ConfigUpdateResponse.load(content)

    def get_usage(self, org_name: str, db_name: str, from_ts: OptStr = None, to_ts: OptStr = None) -> UsageRead:
        """
        Get the usage statistics for a database in the given timeframe.

        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :param from_ts: The datetime to retrieve usage from in ISO 8601 format. Defaults to the current calendar
         month if not provided. Example: 2023-01-01T00:00:00Z
        :param to_ts: The datetime to retrieve usage to in ISO 8601 format. Defaults to the current calendar
         month if not provided. Example: 2023-02-01T00:00:00Z
        :return: UsageRead
        """
        endpoint = API_PATH["get_usage"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint

        params = {}
        if from_ts:
            params["from"] = from_ts
        if to_ts:
            params["to"] = to_ts

        response = requests.get(request_url, headers=self.client.base_header, params=params)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()
        return UsageRead.load(content["database"])

    def get_stats(self, org_name: str, db_name: str) -> List[StatQuery]:
        """
        Fetch the top queries of a database, including the count of rows read and written.
        :param org_name: The name of the organization or user.
        :param db_name: The name of the database.
        :return: List of top queries
        """
        endpoint = API_PATH["get_stats"].format(org_name=org_name, name=db_name)
        request_url = self.client.base_url + endpoint

        response = requests.get(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()
        return [StatQuery.load(x) for x in content["top_queries"]]
