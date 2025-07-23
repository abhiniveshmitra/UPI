# UPI Simulation Performance Comparison: Sequential vs. Concurrent for 10,000 Users

This document compares the performance of a sequential (basic) UPI simulation versus an optimized concurrent (parallel) version, based on benchmarks for 10,000 simulated users. The concurrent version leverages asyncio, semaphores, and socket programming for parallelism, while the sequential version processes everything in a single thread without networking. Both include random failure modes (e.g., wrong PIN or insufficient funds) for realism, ensuring a fair comparison.

## Key Metrics Comparison

| Metric                          | Sequential                  | Concurrent                  | Improvement/Gain                  |
|---------------------------------|-----------------------------|-----------------------------|-----------------------------------|
| **Total Time (seconds)**       | 196.77                     | 45.55                      | 76.86% faster (4.32x speedup)    |
| **Avg Time per User (seconds)**| 0.0197                     | 0.0046                     | 76.65% faster (4.28x speedup)    |
| **Avg Time per Transaction (seconds)** | 0.0197              | 0.0046                     | 76.65% faster (4.28x speedup)    |
| **Throughput (tx/second)**     | 50.82                      | 218.25                     | +167.43 tx/sec (4.30x higher)    |
| **Registration Success Rate**  | 100.00% (10000/10000)      | 99.42% (9942/10000)        | -0.58% (minor concurrency overhead) |
| **Transaction Success Rate**   | 33.63% (3363/10000)        | 33.41% (3322/9942)         | Comparable (due to random modes) |
| **Successful Transactions**    | 3363                       | 3322                       | Comparable                       |
| **Wrong PIN Failures**         | 3260                       | 3313                       | Comparable                       |
| **Insufficient Funds Failures**| 3377                       | 3306                       | Comparable                       |
| **Other Errors**               | 0                          | 1                          | Minor (e.g., rare timeout)       |

- **Speedup Calculation**: Concurrent total time is 4.32x faster (196.77 / 45.55).
- **Time Savings**: 151.22 seconds saved, or ~77% reduction.
- **Throughput Gain**: Concurrent handles 4.30x more transactions per second, scaling efficiently with load.

## Explanation of Testing Methodology

### Overview
Testing was conducted on a local machine (Windows, home WiFi network) to benchmark scalability and concurrency benefits. Both versions simulated 10,000 users, each involving merchant/user registration, QR code generation, and a payment transaction. Random failure modes were applied equally ('ok' for success, 'bad_pin' for PIN errors, 'low_funds' for insufficient balance) to mimic real-world UPI scenarios, targeting ~33% success rates.

### Sequential Version Setup and Execution
- **Files**: Self-contained in `simulate_10000_users.py` (imports functions from supporting files like `bank_server.py`, `upi_machine.py`, etc.).
- **Environment**: No separate servers needed; all operations use direct function calls (in-memory, no sockets).
- **Steps**:
  1. Set `num_users = 10000` in the script.
  2. Run `python simulate_10000_users.py` in a terminal.
  3. The script processes users one by one sequentially, generating QR PNG files and logging results.
- **Metrics Collection**: Timing uses Python's `time` module; failures are simulated by adjusting PIN/amount before calling `initiate_payment`.
- **Runtime**: ~3 minutes 17 seconds, limited by linear execution (e.g., QR image saving is a bottleneck).

### Concurrent Version Setup and Execution
- **Files**: Main script (e.g., with `asyncio.run(simulate_all(10000))`), plus separate `bank_server.py` and `upi_machine.py` for async servers.
- **Environment**: Uses localhost sockets (127.0.0.1); semaphore limits concurrency to 250 tasks to prevent overload.
- **Steps**:
  1. Start servers in separate terminals:
     - `python bank_server.py` (listens on port 5000).
     - Run UPI machine script (listens on port 6001).
  2. Set `num_users=10000` in the main script.
  3. Run the script in a third terminal: `python concurrent_script.py`.
  4. Asyncio gathers tasks for parallel registrations/transactions; results saved to `simulation_results.json`.
- **Metrics Collection**: Timing via `time` module; failures simulated randomly per user.
- **Runtime**: ~46 seconds, benefiting from parallel I/O (e.g., overlapping network calls).

### Testing Conditions and Notes
- **Hardware/Network**: Same machine for both runs to ensure fairness; no external factors (e.g., closed apps).
- **Dependencies**: Python 3.x with `pillow` and `qrcode` for QR generation.
- **Randomness**: Seeded via `random` module; failure modes ensure ~1/3 success rate.
- **Limitations**: Concurrent had minor registration failures (0.58%) possibly due to high load—adjustable via semaphore. Tests were single runs; averages from multiple could refine results.
- **Purpose**: To quantify concurrency gains (e.g., 4x+ speedup) for a UPI-like system with blockchain ledger and cryptography.

For code/details, see the repository files. If reproducing, ensure consistent environments.
