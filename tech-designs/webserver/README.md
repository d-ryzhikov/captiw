# Application backend webserver

## Objective
Choose a backend webserver which would enable me to develop a robust and
effective solution.

### Options:
* [FastAPI](https://fastapi.tiangolo.com/)
  + [uvicorn](https://www.uvicorn.org/) as server;
  + [pydantic](https://pydantic-docs.helpmanual.io/) for data validation;

* [aiohttp](https://docs.aiohttp.org/en/stable/web.html)
  + [marshmallow](https://marshmallow.readthedocs.io/en/stable/)
    for data validation;

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
  + [flask-expects-json](https://github.com/fischerfredl/flask-expects-json)
    for data validation;

### Running tests

1. Setup virtual environment and install required dependencies:

    ```shell
    $ virtualenv -p python3.7 .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    ```

2. Get [wrk](https://github.com/wg/wrk).
3. Run one of the `*.py` scripts using `time` command for tracking max RAM
  usage - that should launch app server on http://127.0.0.1:5000:

    ```shell
    $ \time -f '%M kb' ./fastapi_api.py
    ```
  or

    ```shell
    $ \time -f '%M kb' ./aiohttp_api.py
    ```
  or

    ```shell
    $ \time -f '%M kb' ./flask_api.py
    ```

4. Start one of the loadtesting scripts.
    * `static.lua` - script for testing static data endpoint.
    * `validate.lua` - script for testing endpoint with json body validation.

    ```shell
    $ wrk -c 120 -t 12 http://localhost:5000 -d10s -s validate.lua
    ```
  or

    ```shell
    $ wrk -c 120 -t 12 http://localhost:5000 -d10s -s static.lua
    ```
  This script will run 12 wrk threads with 120 connections
  (120 / 12 = 10 connections per thread) for 10 seconds.

### Test results

* FastAPI

    ```shell
    $ \time -f '%M kb' ./fastapi_api.py
    ```

    - Validation

        ```shell
        $ wrk -c 120 -t 10 http://127.0.0.1:5000 -d 10s -s validate.lua
        Running 10s test @ http://127.0.0.1:5000
          10 threads and 120 connections
          Thread Stats   Avg      Stdev     Max   +/- Stdev
            Latency    64.95ms   33.17ms 253.45ms   66.14%
            Req/Sec   187.73     31.80   360.00     71.63%
          18653 requests in 10.09s, 4.31MB read
          Non-2xx or 3xx responses: 9505
        Requests/sec:   1848.28
        Transfer/sec:    437.74KB
        ```
      Max RAM usage: 41232 kb

    - Static

        ```shell
        $ wrk -c 120 -t 10 http://127.0.0.1:5000 -d 10s -s static.lua
        Running 10s test @ http://127.0.0.1:5000
          10 threads and 120 connections
          Thread Stats   Avg      Stdev     Max   +/- Stdev
            Latency     0.00us    0.00us   0.00us    -nan%
            Req/Sec     0.00      0.00     0.00      -nan%
          0 requests in 10.08s, 278.06MB read
        Requests/sec:      0.00
        Transfer/sec:     27.59MB
        ```
      Max RAM usage: 58640 kb

* aiohttp

    ```shell
    $ \time -f '%M kb' ./aiohttp_api.py
    ```

    - Validation

        ```shell
        $ wrk -c 120 -t 10 http://127.0.0.1:5000 -d 10s -s validate.lua
        Running 10s test @ http://127.0.0.1:5000
          10 threads and 120 connections
          Thread Stats   Avg      Stdev     Max   +/- Stdev
            Latency    71.59ms    6.80ms 109.65ms   94.77%
            Req/Sec   167.71     52.13   242.00     68.69%
          16762 requests in 10.09s, 2.87MB read
          Non-2xx or 3xx responses: 8424
        Requests/sec:   1661.69
        Transfer/sec:    291.53KB
        ```
      Max RAM usage: 48860 kb

    - Static

        ```shell
        $ wrk -c 120 -t 10 http://127.0.0.1:5000 -d 10s -s static.lua
        Running 10s test @ http://127.0.0.1:5000
          10 threads and 120 connections
          Thread Stats   Avg      Stdev     Max   +/- Stdev
            Latency   314.95ms   30.04ms 425.09ms   85.39%
            Req/Sec    37.78     14.88   100.00     68.63%
          3771 requests in 10.10s, 18.41GB read
        Requests/sec:    373.55
        Transfer/sec:      1.82GB
        ```
      Max RAM usage: 39936 kb

* Flask
    **Note:** flask should be deployed with gunicorn which will spawn an additional
    master process that will use ~30 MB RAM.


    ```shell
    $ \time -f '%M kb' ./flask_api.py
    ```

    - Validation

        ```shell
        $ wrk -c 120 -t 10 http://127.0.0.1:5000 -d 10s -s validate.lua
        Running 10s test @ http://127.0.0.1:5000
          10 threads and 120 connections
          Thread Stats   Avg      Stdev     Max   +/- Stdev
            Latency   235.67ms  175.23ms   2.00s    94.10%
            Req/Sec    50.64     28.75   262.00     73.27%
          3086 requests in 10.09s, 1.23MB read
          Socket errors: connect 0, read 0, write 0, timeout 39
          Non-2xx or 3xx responses: 1593
        Requests/sec:    305.81
        Transfer/sec:    125.13KB
        ```
      Max RAM usage: 38476 kb for master + 32MB for worker

    - Static

        ```shell
        $ wrk -c 120 -t 10 http://127.0.0.1:5000 -d 10s -s static.lua
        Running 10s test @ http://127.0.0.1:5000
          10 threads and 120 connections
          Thread Stats   Avg      Stdev     Max   +/- Stdev
            Latency   298.66ms   47.36ms 618.83ms   94.50%
            Req/Sec    41.04     20.64   220.00     68.12%
          3982 requests in 10.10s, 19.44GB read
        Requests/sec:    394.30
        Transfer/sec:      1.93GB
        ```
      Max RAM usage: 38424 kb for master + 32MB for worker

# Final decision
aiohttp has shown the best performance for static file serving and was 2nd on body
validation. Pydantic however is known to be faster for serialization and validation than
marshmallow ([source](https://pydantic-docs.helpmanual.io/benchmarks/)),
which is why it is going to be used for json validation.
