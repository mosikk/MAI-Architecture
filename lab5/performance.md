# Нагрузочное тестирование с кэшом и без кэша

Без кэша:
```
4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    61.23ms    9.36ms 110.46ms   72.90%
    Req/Sec   459.69     51.38   580.00     72.75%
  56659 requests in 30.09s, 11.43MB read
Requests/sec:   1949.20
Transfer/sec:      1.47MB
```


С кэшом:
```
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    44.70ms    8.43ms  84.59ms   73.58%
    Req/Sec   561.34     57.63   700.00     69.08%
  67209 requests in 30.08s, 12.24MB read
Requests/sec:   2234.66
Transfer/sec:    416.82KB
```
