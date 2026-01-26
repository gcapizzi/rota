import collections.abc
import random

import requests
import requests.adapters


class RandomProxyAdapter(requests.adapters.BaseAdapter):
    def __init__(self, adapter: requests.adapters.BaseAdapter, proxies: list[str]):
        if not proxies:
            raise ValueError("Proxy list cannot be empty")

        self._adapter = adapter
        self._proxies = proxies

    def send(
        self,
        request: requests.PreparedRequest,
        stream: bool = False,
        timeout: None | float | tuple[float, float] | tuple[float, None] = None,
        verify: bool | str = True,
        cert: None | bytes | str | tuple[bytes | str, bytes | str] = None,
        proxies: collections.abc.Mapping[str, str] | None = None,
    ) -> requests.Response:
        selected_proxy = random.choice(self._proxies)

        return self._adapter.send(
            request,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies={"http": selected_proxy, "https": selected_proxy},
        )

    def close(self) -> None:
        self._adapter.close()


__all__ = ["RandomProxyAdapter"]
