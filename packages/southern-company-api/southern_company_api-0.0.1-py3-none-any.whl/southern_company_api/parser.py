import re
import typing
from typing import List

import aiohttp as aiohttp

from src.southern_company_api.account import Account
from src.southern_company_api.company import COMPANY_MAP


async def get_request_verification_token() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            http_response = await session.get(
                "https://webauth.southernco.com/account/login"
            )
            login_page = await http_response.text()
            matches = re.findall(r'data-aft="(\S+)"', login_page)
    except Exception as error:
        raise error
    return matches[0]


class SouthernCompanyAPI:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.jwt: typing.Optional[str] = None
        self.sc: typing.Optional[str] = None
        self.request_token: typing.Optional[str] = None
        self.accounts: typing.Optional[List[Account]] = None

    async def connect(self) -> None:
        self.request_token = await get_request_verification_token()
        self.sc = await self.get_sc_web_token()
        self.jwt = await self.get_jwt()
        self.accounts = await self._get_accounts()

    async def get_sc_web_token(self) -> str:
        # Grab a ScWebToken by log in
        if self.request_token is None:
            raise Exception("Cannot get sc web token without verification token")
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "RequestVerificationToken": self.request_token,
        }

        data = {
            "username": self.username,
            "password": self.password,
            "targetPage": 1,
            "params": {"ReturnUrl": "null"},
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://webauth.southernco.com/api/login", json=data, headers=headers
            ) as response:
                connection = await response.json()
        sc_regex = re.compile(r"NAME='ScWebToken' value='(\S+.\S+.\S+)'", re.IGNORECASE)
        sc_data = sc_regex.search(connection["data"]["html"])
        if sc_data and sc_data.group(1):
            if "'>" in sc_data.group(1):
                return sc_data.group(1).split("'>")[0]
            else:
                return sc_data.group(1)
        else:
            raise Exception()

    async def get_jwt(self) -> str:
        # Trading ScWebToken for Jwt
        if self.sc is None:
            raise Exception("can't get jwt without sc_web_token")
        data = {"ScWebToken": self.sc}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://customerservice2.southerncompany.com/Account/LoginComplete?"
                "ReturnUrl=null",
                data=data,
            ) as resp:
                # Checking for unsuccessful login
                if resp.status != 200:
                    raise Exception(
                        f"Failed to get secondary ScWebToken: {resp.status} "
                        f"{resp.headers} {data}"
                    )
                # Regex to parse JWT out of headers
                swtregex = re.compile(r"ScWebToken=(\S*);", re.IGNORECASE)

                # Parsing response header to get token
                swtcookies = resp.headers.get("set-cookie")
                if swtcookies:
                    swtmatches = swtregex.search(swtcookies)

                    # Checking for matches
                    if swtmatches and swtmatches.group(1):
                        swtoken = swtmatches.group(1)
                    else:
                        raise Exception(
                            "Failed to get secondary ScWebToken: Could not find any "
                            "token matches in headers"
                        )
                else:
                    raise Exception(
                        "Failed to get secondary ScWebToken: No Cookies were sent back"
                    )

        # Now fetch JWT after secondary ScWebToken
        headers = {"Cookie": f"ScWebToken={swtoken}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://customerservice2.southerncompany.com/Account/LoginValidated/"
                "JwtToken",
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Failed to get JWT: {resp.status} {await resp.text()} "
                        f"{headers}"
                    )

                # Regex to parse JWT out of headers
                regex = re.compile(r"ScJwtToken=(\S*);", re.IGNORECASE)

                # Parsing response header to get token
                cookies = resp.headers.get("set-cookie")
                if cookies:
                    matches = regex.search(cookies)

                    # Checking for matches
                    if matches and matches.group(1):
                        token = matches.group(1)
                    else:
                        raise Exception(
                            "Failed to get JWT: Could not find any token matches in "
                            "headers"
                        )
                else:
                    raise Exception("Failed to get JWT: No Cookies were sent back")

        # Returning JWT
        return token

    async def _get_accounts(self) -> List[Account]:
        if self.jwt is None:
            raise Exception("can't get accounts without jwt")
        headers = {"Authorization": f"bearer {self.jwt}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://customerservice2api.southerncompany.com/api/account/"
                "getAllAccounts",
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    raise Exception("failed to get accounts")
                account_json = await resp.json()
                accounts = []
                for account in account_json["Data"]:
                    accounts.append(
                        Account(
                            name=account["Description"],
                            primary=account["PrimaryAccount"] == "Y",
                            number=account["AccountNumber"],
                            company=COMPANY_MAP.get(account["Company"]),
                        )
                    )
        return accounts
