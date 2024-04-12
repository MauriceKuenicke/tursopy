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

## Installation
```sh
pip install tursopy
```

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