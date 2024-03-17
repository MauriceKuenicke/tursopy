from typing import TYPE_CHECKING
from .endpoints import API_PATH
import requests
from typing import List, Optional
import json
from .dataclasses import DatabaseRead, DatabaseCreated
from .exceptions import TursoRequestException

if TYPE_CHECKING:
    import tursopy

OptStr = Optional[str]
OptBool = Optional[bool]


class DatabasesClient:
    """
    Databases client managing the databases endpoints.
    """
    def __init__(self, base_client: "tursopy.TursoClient"):
        self.client = base_client

    def list_databases(self, org_name: str) -> List[DatabaseRead]:
        endpoint = API_PATH["list_databases"].format(org_name=org_name)
        request_url = self.client.base_url + endpoint
        response = requests.get(request_url, headers=self.client.base_header)

        if response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content}")

        content = response.json()
        return [DatabaseRead.load(x) for x in content["databases"]]

    def create_database(self, org_name: str,
                        name: str, is_schema: OptBool = None,
                        schema: OptStr = None, seed_name: OptStr = None,
                        seed_ts: OptStr = None, seed_type: OptStr = None,
                        seed_url: OptStr = None, size_limit: OptStr = None,
                        group: str = "default"):
        """
        Creates a new database in a group for the organization or user.

        :param org_name: The name of the organization or user.
        :param name: The name of the new database. Must contain only lowercase letters, numbers, dashes.
         No longer than 32 characters.
        :param is_schema: Mark this database as the parent schema database that updates child
        databases with any schema changes.
        :param schema: The name of the parent database to use as the schema. See Multi-DB Schemas.
        :param seed_name: The name of the existing database when database is used as a seed type.
        :param seed_ts: A formatted ISO 8601 recovery point to create a database from.
        This must be within the last 24 hours, or 30 days on the scaler plan.
        :param seed_type: The type of seed to be used to create a new database. Either 'database' or 'dump'.
        :param seed_url: The URL returned by upload dump can be used with the dump seed type.
        :param size_limit: The maximum size of the database in bytes. Values with units are also accepted,
         e.g. '1mb', '256mb', '1gb'.
        :param group: The name of the group where the database should be created.
        The group must already exist. Defaults to 'default'.
        :return:
        """
        endpoint = API_PATH["create_database"].format(org_name=org_name)
        request_url = self.client.base_url + endpoint

        data = {
            "name": name,
            "group": group,
        }

        if is_schema:
            data["is_schema"] = is_schema
        if schema:
            data["schema"] = schema
        if size_limit:
            data["size_limit"] = size_limit
        if any([seed_name, seed_ts, seed_url, seed_type]):
            seed_data = {
                "name": seed_name,
                "timestamp": seed_ts,
                "type": seed_type,
                "url": seed_url}
            data["seed"] = seed_data

        response = requests.post(request_url, data=json.dumps(data), headers=self.client.base_header)

        if response.status_code != 200:
            error_message = response.json()["error"]
            raise TursoRequestException(f"Something went wrong: {error_message}")

        content = response.json()["database"]
        return DatabaseCreated.load(content)

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
