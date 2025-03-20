# description
This repository is used for Assignemnt part-1
# output for 10^6
Processing 1000000 numbers
Sequential time: 0.08588123321533203
Multiprocessing individual processes time: 0.258150577545166
Multiprocessing pool map time: 0.09995651245117188
Multiprocessing pool apply time: 0.03635239601135254
ProcessPoolExecutor time: 111.18416500091553
Async pool map time: 0.2148299217224121

# output for 10^7
Processing 10000000 numbers
Sequential time: 0.8591287136077881
Multiprocessing individual processes time: 0.28902435302734375
Multiprocessing pool map time: 0.8338913917541504
Multiprocessing pool apply time: 0.04844808578491211
ProcessPoolExecutor time: 1099.1383101940155
Async pool map time: 1.526427984237671

# Connection pool
Process-1 acquired Connection 2
Process-2 acquired Connection 2
Process-3 acquired Connection 2
Process-2 released Connection 2
Process-4 acquired Connection 2
Process-3 released Connection 2
Process-5 acquired Connection 2
Process-1 released Connection 2
Process-6 acquired Connection 2
Process-5 released Connection 2
Process-7 acquired Connection 2
Process-6 released Connection 2
Process-8 acquired Connection 2
Process-7 released Connection 2
Process-9 acquired Connection 2
Process-4 released Connection 2
Process-10 acquired Connection 2
Process-9 released Connection 2
Process-10 released Connection 2
Process-8 released Connection 2
All processes completed.

# Semaphore Observations:
# If more processes request connections than available, they wait until a slot is freed.
# The semaphore prevents race conditions by ensuring only a fixed number of processes access shared resources concurrently.
