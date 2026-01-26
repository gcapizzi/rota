# Rota

A Python requests adapter that randomly selects a proxy from a list for each request.

## Usage

```python
from requests import Session
from requests.adapters import HTTPAdapter
from rota import RandomProxyAdapter

proxies = ["http://proxy1:8080", "http://proxy2:8080", "http://proxy3:8080"]
adapter = RandomProxyAdapter(HTTPAdapter(), proxies)

session = Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

response = session.get("http://example.com")
```

Each request will use a randomly selected proxy from the list.
