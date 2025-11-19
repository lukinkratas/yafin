# Yafin

Unofficial [Yahoo!Ⓡ finance](https://finance.yahoo.com) Python API client.

- Not affiliated with Yahoo, Inc.
- Open source library that uses publicly available APIs.
- Intended for research, educational purposes and personal use only.
- Synchronous and asynchronous.
- Not returning pandas dataframes (because why?).
- Uses caching and utilizes singleton pattern in symbol class to save resources.
- Minimal and build on [curl-cffi](https://github.com/lexiforest/curl_cffi)
- Approx. 2x faster, than other Yahoo finance clients. Run the tests yourself - `make test-perf` (All tests running synchronously, returning pandas DataFrame and http responses are mocked.)

![test-perf](docs/test-perf.png)

**Documentation and Examples**: [https://lukinkratas.github.io/yafin/](https://lukinkratas.github.io/yafin/)

**Installation**: `pip install yafin` for more details, see the [Documentation](https://lukinkratas.github.io/yafin/)

**Quick Example**: for more details, see the [Examples](https://lukinkratas.github.io/yafin/examples/symbol/) section in documentation.

```python
from yafin import Symbol

# opt. 1 use context manager (recommended)
with Symbol('META') as meta:
    meta_1y_chart = meta.get_chart(interval='1d', period_range='1y')

# opt. 2 use close to avoid resource leakage
aapl = Symbol('AAPL')
aapl_5d_chart = aapl.get_chart(
    interval='1h', period_range='5d', include_div=True, include_split=False
)
aapl.close()
```