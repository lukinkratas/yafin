# Yafin

Unofficial [Yahoo!Ⓡ finance](https://finance.yahoo.com) API client.

- Not affiliated with Yahoo, Inc.
- Open source library that uses publicly available APIs.
- Intended for research, educational purposes and personal use only.
- Synchronous and asynchronous.
- Not returning pandas dataframes (because why?).
- Uses caching and utilizes singleton pattern in symbol class to save resources.
- Minimal and build on [curl-cffi](https://github.com/lexiforest/curl_cffi)
- Approx. 2x faster, than other Yahoo finance clients. Run the tests yourself - `make test-perf` (All tests running synchronously, returning pandas DataFrame and http responses are mocked.)

![test-perf](docs/test-perf.png)

## Installation

=== "pip"

    ```bash
    pip install yafin
    ```

=== "uv"

    ```bash
    uv add yafin
    ```

**Documentation and Examples**: [https://lukinkratas.github.io/yafin/](https://lukinkratas.github.io/yafin/)

[**Examples**](https://lukinkratas.github.io/yafin/examples/)
