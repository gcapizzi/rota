from unittest.mock import Mock

import pytest
from requests import PreparedRequest
from requests.adapters import HTTPAdapter

from rota import RandomProxyAdapter


class TestRandomProxyAdapter:
    def test_empty_proxy_list_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Proxy list cannot be empty"):
            RandomProxyAdapter(HTTPAdapter(), [])

    def test_send_delegates_to_wrapped_adapter(self) -> None:
        mock_adapter = Mock(spec=HTTPAdapter)
        mock_response = Mock()
        mock_adapter.send.return_value = mock_response

        proxies = ["http://proxy1:8080", "http://proxy2:8080", "http://proxy3:8080"]
        adapter = RandomProxyAdapter(mock_adapter, proxies)
        request = PreparedRequest()

        response = adapter.send(
            request, stream=True, timeout=60, verify=False, cert="path/to/cert"
        )

        assert response is mock_response
        mock_adapter.send.assert_called_once()

        _, kwargs = mock_adapter.send.call_args
        assert kwargs["proxies"]["http"] == kwargs["proxies"]["https"]
        assert kwargs["proxies"]["http"] in proxies
        assert kwargs["proxies"]["https"] in proxies

        assert kwargs["stream"] is True
        assert kwargs["timeout"] == 60
        assert kwargs["verify"] is False
        assert kwargs["cert"] == "path/to/cert"

    def test_close_delegates_to_wrapped_adapter(self) -> None:
        mock_adapter = Mock(spec=HTTPAdapter)

        adapter = RandomProxyAdapter(mock_adapter, ["http://proxy1:8080"])

        adapter.close()

        mock_adapter.close.assert_called_once()
