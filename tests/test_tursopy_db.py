import pytest
import responses

from tursopy import TursoClient
from tursopy.db import DatabasesClient
from tursopy.exceptions import TursoRequestException


@pytest.fixture
def db_client(client: TursoClient) -> DatabasesClient:
    return DatabasesClient(base_client=client)


class TestTursoDBClient:
    @responses.activate
    def test_list_databases(self, db_client: DatabasesClient) -> None:
        response_object = {
            "databases": [
                {
                    "DbId": "0eb771dd-6906-11ee-8553-eaa7715aeaf2",
                    "Hostname": "[databaseName]-[organizationName].turso.io",
                    "hostname": "[databaseName]-[organizationName].turso.io",
                    "Name": "my-db",
                    "allow_attach": True,
                    "block_reads": True,
                    "block_writes": True,
                    "group": "default",
                    "is_schema": True,
                    "primaryRegion": "lhr",
                    "regions": ["lhr", "bos", "nrt"],
                    "schema": "<string>",
                    "sleeping": True,
                    "type": "logical",
                    "version": "0.22.22",
                }
            ]
        }
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases",
            json=response_object,
            status=200,
        )

        response = db_client.list_databases(org_name="my-org")
        assert [x.to_dict() for x in response] == response_object["databases"]

    @responses.activate
    def test_list_database(self, db_client: DatabasesClient) -> None:
        response_object = {"error": "some error"}
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases",
            json=response_object,
            status=400,
        )

        with pytest.raises(TursoRequestException):
            db_client.list_databases(org_name="my-org")

    @responses.activate
    def test_database_update_allow_attach(self, db_client: DatabasesClient) -> None:
        response_object = {"allow_attach": True}
        responses.add(
            responses.PATCH,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/configuration",
            json=response_object,
            status=200,
        )
        response = db_client.update(org_name="my-org", db_name="my-db", allow_attach=True)

        assert response.to_dict() == {"allow_attach": True, "size_limit": None}

    @responses.activate
    def test_database_update_size_limit(self, db_client: DatabasesClient) -> None:
        response_object = {"size_limit": "250mb"}
        responses.add(
            responses.PATCH,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/configuration",
            json=response_object,
            status=200,
        )
        response = db_client.update(org_name="my-org", db_name="my-db", size_limit="250mb")

        assert response.to_dict() == {"allow_attach": None, "size_limit": "250mb"}

    @responses.activate
    def test_database_update_raises_error(self, db_client: DatabasesClient) -> None:
        response_object = {"error": "some error"}
        responses.add(
            responses.PATCH,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/configuration",
            json=response_object,
            status=400,
        )

        with pytest.raises(TursoRequestException):
            db_client.update(org_name="my-org", db_name="my-db", allow_attach=False)

    @responses.activate
    def test_database_creation_successful(self, db_client: DatabasesClient) -> None:
        response_object = {
            "database": {
                "DbId": "0eb771dd-6906-11ee-8553-eaa7715aeaf2",
                "Hostname": "my-db-my-org.turso.io",
                "Name": "my-db",
                "IssuedCertCount": 0,
                "IssuedCertLimit": 2,
            }
        }
        responses.add(
            responses.POST,
            "https://api.turso.tech/v1/organizations/my-org/databases",
            json=response_object,
            status=200,
        )
        response = db_client.create_database(org_name="my-org", name="my-db")

        assert response.to_dict() == response_object["database"]

    @responses.activate
    def test_database_creation_with_seed_type_database_successful(self, db_client: DatabasesClient) -> None:
        response_object = {
            "database": {
                "DbId": "0eb771dd-6906-11ee-8553-eaa7715aeaf2",
                "Hostname": "my-db-my-org.turso.io",
                "Name": "my-db",
                "IssuedCertCount": 0,
                "IssuedCertLimit": 2,
            }
        }
        responses.add(
            responses.POST,
            "https://api.turso.tech/v1/organizations/my-org/databases",
            json=response_object,
            status=200,
        )
        response = db_client.create_database(
            org_name="my-org", name="my-db", seed_type="database", seed_name="my-schema-db"
        )

        assert response.to_dict() == response_object["database"]

    def test_database_creation_triggers_error_on_wrong_parameter_combination(self, db_client: DatabasesClient) -> None:
        # is_schema + schema
        with pytest.raises(ValueError):
            db_client.create_database(org_name="my-org", name="my-db", is_schema=True, schema="my-schema-db")

        # wrong seed_type
        with pytest.raises(ValueError):
            db_client.create_database(org_name="my-org", name="my-db", seed_type="other-type")  # type:ignore [arg-type]

        # seed_type=database + no name
        with pytest.raises(ValueError):
            db_client.create_database(org_name="my-org", name="my-db", seed_type="database")

        # seed_type=dump + no url
        with pytest.raises(ValueError):
            db_client.create_database(org_name="my-org", name="my-db", seed_type="dump")

    @responses.activate
    def test_retrieve_db_successful(self, db_client: DatabasesClient) -> None:
        response_object = {
            "instance": {
                "hostname": "[databaseName]-[organizationName].turso.io",
                "name": "lhr",
                "region": "lhr",
                "type": "primary",
                "uuid": "0be90471-6906-11ee-8553-eaa7715aeaf2",
            }
        }
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/instances/lhr",
            json=response_object,
            status=200,
        )
        response = db_client.get_instance(org_name="my-org", db_name="my-db", instance_name="lhr")
        assert response.to_dict() == response_object["instance"]

    @responses.activate
    def test_retrieve_db_fails(self, db_client: DatabasesClient) -> None:
        response_object = {"error": "Something went wrong."}
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/instances/lhr",
            json=response_object,
            status=404,
        )

        with pytest.raises(TursoRequestException):
            db_client.get_instance(org_name="my-org", db_name="my-db", instance_name="lhr")

    @responses.activate
    def test_get_usage_db_successful(self, db_client: DatabasesClient) -> None:
        response_object = {
            "database": {
                "instances": [
                    {
                        "usage": {"rows_read": 0, "rows_written": 0, "storage_bytes": 4096},
                        "uuid": "cd831986-94e5-11ee-a6fe-7a52e1f7759a",
                    },
                    {
                        "usage": {"rows_read": 0, "rows_written": 0, "storage_bytes": 4096},
                        "uuid": "0be90471-6906-11ee-8553-eaa7715aeaf2",
                    },
                ],
                "total": {"rows_read": 123, "rows_written": 123, "storage_bytes": 123},
                "uuid": "0eb771dd-6906-11ee-8553-eaa7715aeaf2",
            }
        }
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/usage",
            json=response_object,
            status=200,
        )
        response = db_client.get_usage(org_name="my-org", db_name="my-db")
        assert response.to_dict() == response_object["database"]

    @responses.activate
    def test_get_usage_db_fails(self, db_client: DatabasesClient) -> None:
        response_object = {"error": "Something went wrong."}
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/usage",
            json=response_object,
            status=404,
        )

        with pytest.raises(TursoRequestException):
            db_client.get_usage(org_name="my-org", db_name="my-db")

    @responses.activate
    def test_get_db_stats_successful(self, db_client: DatabasesClient) -> None:
        response_object = {
            "top_queries": [
                {
                    "query": "SELECT COUNT(*), CustomerID FROM Orders GROUP BY CustomerID HAVING COUNT(*) > 5;",
                    "rows_read": 123,
                    "rows_written": 4567,
                }
            ]
        }
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/stats",
            json=response_object,
            status=200,
        )
        response = db_client.get_stats(org_name="my-org", db_name="my-db")
        for indx, qry in enumerate(response):
            assert qry.to_dict() == response_object["top_queries"][indx]

    @responses.activate
    def test_get_db_stats_fails(self, db_client: DatabasesClient) -> None:
        response_object = {"error": "Something went wrong."}
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/organizations/my-org/databases/my-db/stats",
            json=response_object,
            status=404,
        )
        with pytest.raises(TursoRequestException):
            db_client.get_stats(org_name="my-org", db_name="my-db")
