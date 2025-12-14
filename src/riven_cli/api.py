import aiohttp
from typing import Any, Optional
from riven_cli.config import settings


class RivenClient:
    def __init__(self):
        self.base_url = settings.api_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None

    def refresh_settings(self):
        self.base_url = settings.api_url.rstrip("/")

    async def __aenter__(self):
        self.refresh_settings()
        self.session = aiohttp.ClientSession(
            headers={
                "x-api-key": settings.api_key or "",
                "Content-Type": "application/json",
            }
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def get(
        self, endpoint: str, params: dict[str, Any] | None = None, **kwargs: Any
    ) -> Any:
        assert self.session
        url = f"{self.base_url}/api/v1{endpoint}"
        async with self.session.get(url, params=params, **kwargs) as resp:
            if not resp.ok:
                text = await resp.text()
                raise Exception(f"{resp.status} {resp.reason}: {text}")
            return await resp.json()

    async def post(
        self, endpoint: str, json: dict[str, Any] | None = None, **kwargs: Any
    ) -> Any:
        assert self.session
        url = f"{self.base_url}/api/v1{endpoint}"
        async with self.session.post(url, json=json, **kwargs) as resp:
            if not resp.ok:
                text = await resp.text()
                raise Exception(f"{resp.status} {resp.reason}: {text}")
            return await resp.json()

    async def delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        assert self.session
        url = f"{self.base_url}/api/v1{endpoint}"
        async with self.session.delete(url, params=params, json=json, **kwargs) as resp:
            if not resp.ok:
                text = await resp.text()
                raise Exception(f"{resp.status} {resp.reason}: {text}")
            return await resp.json()

    async def check_health(self) -> bool:
        try:
            await self.get("/health")
            return True
        except Exception:
            return False


client = RivenClient()
