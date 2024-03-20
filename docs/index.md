<h1 align="center">
  TursoPy
</h1>

<p align="center">
    <em>Fully type-hinted Turso Platform API wrapper for Python.</em>
</p>

<p align="center">
<a href="https://github.com/MauriceKuenicke/tursopy/actions/workflows/cicd.yml?query=workflow%3ACICD+branch%3Amain++" target="_blank">
    <img src="https://github.com/MauriceKuenicke/tursopy/actions/workflows/cicd.yml/badge.svg?branch=main" alt="Test">
</a>
<a href="https://codecov.io/gh/MauriceKuenicke/tursopy" > 
    <img src="https://codecov.io/gh/MauriceKuenicke/tursopy/branch/main/graph/badge.svg?token=NYH162MDJD"/> 
</a>
</p>

---

**Documentation**: <a href="https://mauricekuenicke.github.io/tursopy/" target="_blank">https://mauricekuenicke.github.io/tursopy/</a>

**Source Code**: <a href="https://github.com/MauriceKuenicke/tursopy" target="_blank">https://github.com/MauriceKuenicke/tursopy</a>

---

# ⚠️ Important

This project is in early development and currently not safe for use in a production environment. Use at your own risk.

---
## Example Usage
```py
from tursopy import TursoClient

client = TursoClient()
new_api_token = client.create_platform_api_token(name="my-test-token")  # Create a new platform token
client.revoke_token(name=new_api_token.name) # Revoke it again

# You can also create a new database
new_db = client.db.create_database(org_name="my-org", name="delete-me-later")
print("New database:", new_db)

# List available databases in your organization or for your user
print(client.db.list_databases(org_name="my-org"))
client.db.delete_database(org_name="my-org", db_name=new_db.Name) # Delete your database again
```

## Initial Platform API Token
TursoPy assumes a platform api token to be available when running the first time. Please refer to the
[official documentation](https://docs.turso.tech/cli/auth/token) to find out how to generate your token.


## Response Models

TursoPy models mirror the Turso platform API response models as much as possible. This way, you'll always know how
to access the data just by looking at the platform documentation. TursoPy sometimes flattens the responses if it makes
sense. This happens mostly for response models which only contain a single field with data.

<div class="termy">

```console
$ curl -L https://api.turso.tech/v1/organizations/your-org/databases -H 'Authorization: Bearer YOUR-TOKEN'


---> 100%

{
  "databases": [
    {
      "DbId": "0eb771dd-6906-11ee-8553-eaa7715aeaf2",
      "Hostname": "your-db-your-org.turso.io",
      "Name": "my-db",
      "allow_attach": true,
      "block_reads": true,
      "block_writes": true,
      "group": "default",
      "is_schema": true,
      "primaryRegion": "lhr",
      "regions": [
        "lhr",
        "bos",
        "nrt"
      ],
      "schema": "<string>",
      "sleeping": true,
      "type": "logical",
      "version": "0.22.22"
    }
  ]
}
```

</div>

In those cases,
you'll be able to access the data directly without going through that extra level.

```py
from tursopy import TursoClient

client = TursoClient()
my_databases = client.db.list_databases(org_name="my-org")   # (1)

print("Schema:", my_databases[0].schema)   # (2)
print("Group:", my_databases[0].group)
print("Primary Region:", my_databases[0].primaryRegion)
```

1.  Returns a list of databases directly
2.  Supports code completion