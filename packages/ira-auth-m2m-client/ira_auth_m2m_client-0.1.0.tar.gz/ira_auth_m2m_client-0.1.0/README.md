# IraAuthM2M client

IraAuthM2M (machine-to-machine authentication) is used to authenticate an application by IraAuth so that it can access APIs protected by IraAuth.

## Install
    pip install ira_auth_m2m_client

## Sample Usage

```py
import os
import asyncio
from ira_auth_m2m.auth import IraAuth


ira_auth = IraAuth(
    client_id=os.environ.get("IRA_AUTH_M2M_CLIENT_ID"), 
    client_secret=os.environ.get("IRA_AUTH_M2M_CLIENT_SECRET"),
    token_endpoint=os.environ.get("IRA_AUTH_M2M_TOKEN_ENDPOINT"),
    cookie_name=os.environ.get("IRA_AUTH_M2M_COOKIE_NAME")
)


http = ira_auth.get_http_client(base_path="https://xyz.com")


async def main():
    response = await http("GET", "/animals/dog/husky/info")
    if response != None:
        print(response.json())
    
    await ira_auth.cleanup()


asyncio.run(main())
```