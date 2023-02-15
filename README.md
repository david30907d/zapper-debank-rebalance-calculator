
## Run

`python main.py -d <zapper/debank>`

## Install

`poetry install`

## Data Source

1. DeBank: https://api.debank.com/bundle/complex_protocol_list?id=22830
2. Zapper: https://web.zapper.fi/v2/balances/apps?addresses[]=0x038919c63aff9c932c77a0c9c9d98eabc1a4dd08&addresses[]=0x43cd745bd5fbfc8cfd79ebc855f949abc79a1e0c&addresses[]=0x7ee54ab0f204bb3a83df90fdd824d8b4abe93222&addresses[]=0x89e930ff5e1f02be23c109a4e7fffe461e3ca6a0&addresses[]=0xe4bac3e44e8080e1491c11119197d33e396ea82b&networks[]=ethereum&networks[]=polygon&networks[]=optimism&networks[]=gnosis&networks[]=binance-smart-chain&networks[]=fantom&networks[]=avalanche&networks[]=arbitrum&networks[]=bitcoin&networks[]=cronos&networks[]=aurora

## Demo


```
Current gold: xxx.51 Target Sum: xxx.06 Investment Shift: 0.06, should be lower than 0.05
Suggestion: modify this amount of USD: -4910.76 for position glp-avax, current worth: 27167.43
Suggestion: modify this amount of USD: -1922.44 for position glp-arbitrum, current worth: 10635.40
Suggestion: modify this amount of USD: -249.40 for position cvxOHMFRAXBP-f, current worth: 1379.74
Suggestion: modify this amount of USD: -244.12 for position FraxSwapOHM, current worth: 1350.54
Suggestion: modify this amount of USD: -12.73 for position balancer-usdt-eth-btc-arb, current worth: 70.40
====================
Current cash: xxx.43 Target Sum: xxx.06 Investment Shift: -0.13, should be lower than 0.05
Suggestion: modify this amount of USD: 11787.16 for position VSTFRAX-f, current worth: 10947.07
Suggestion: modify this amount of USD: 1593.96 for position crvEURSUSD, current worth: 1480.36
Suggestion: modify this amount of USD: 1485.62 for position cvxOHMFRAXBP-f, current worth: 1379.74
Suggestion: modify this amount of USD: 1454.18 for position FraxSwapOHM, current worth: 1350.54
Suggestion: modify this amount of USD: 849.19 for position compund USDT, current worth: 788.67
Suggestion: modify this amount of USD: 75.80 for position balancer-usdt-eth-btc-arb, current worth: 70.40
Suggestion: modify this amount of USD: 0.71 for position compound USDT, current worth: 0.66
====================
Current stock: xxx.80 Target Sum: xxx.06 Investment Shift: 0.08, should be lower than 0.05
Suggestion: modify this amount of USD: -3496.62 for position , current worth: 14715.22
Suggestion: modify this amount of USD: -2803.99 for position radiant-eth-LP, current worth: 11800.36
Suggestion: modify this amount of USD: -2373.13 for position sushi-dpx-weth-LP, current worth: 9987.11
Suggestion: modify this amount of USD: -639.87 for position Yeti-JLP, current worth: 2692.85
Suggestion: modify this amount of USD: -639.60 for position cvxCRV, current worth: 2691.72
Suggestion: modify this amount of USD: -324.65 for position magic-weth-sushi-LP, current worth: 1366.26
Suggestion: modify this amount of USD: -73.15 for position CVX, current worth: 307.87
Suggestion: modify this amount of USD: -16.73 for position balancer-usdt-eth-btc-arb, current worth: 70.40
====================
Current bond: xxx.48 Target Sum: xxx.06 Investment Shift: -0.00, should be lower than 0.05
Suggestion: modify this amount of USD: 212.81 for position vesta-finance, current worth: 15156.69
Suggestion: modify this amount of USD: 209.44 for position gohm, current worth: 14916.50
Suggestion: modify this amount of USD: 19.37 for position cvxOHMFRAXBP-f, current worth: 1379.74
Suggestion: modify this amount of USD: 18.96 for position FraxSwapOHM, current worth: 1350.54
====================
Current Net Worth: $xxx.22
Your Annual Interest Rate would be $xxx.15, Monthly return in NT$: xxx
```