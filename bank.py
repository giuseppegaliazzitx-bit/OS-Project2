
import threading
import random

# How many tellers and customers to start. The spec wants 3 tellers and
# 50 customers, but I am starting small so the output is easy to read.
NUM_TELLERS = 3
NUM_CUSTOMERS = 3

# Lock so the print lines from different threads don't mix together
print_lock = threading.Lock()


# Print in the format the assignment wants: TYPE ID [OTHER ID]: MSG
def log(thread_type, tid, msg, other=""):
    with print_lock:
        print(f"{thread_type} {tid} [{other}]: {msg}")


# Teller thread, for now it just says it is ready and waiting
def teller(tid):
    log("Teller", tid, "ready to serve")
    log("Teller", tid, "waiting for a customer")


# Customer thread, for now it just picks a transaction and says it
def customer(cid):
    transaction = random.choice(["deposit", "withdrawal"])
    log("Customer", cid, f"wants to perform a {transaction} transaction")


# Start all the teller threads, then all the customer threads, then wait
def main():
    threads = []

    for tid in range(NUM_TELLERS):
        t = threading.Thread(target=teller, args=(tid,))
        threads.append(t)
        t.start()

    for cid in range(NUM_CUSTOMERS):
        t = threading.Thread(target=customer, args=(cid,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
