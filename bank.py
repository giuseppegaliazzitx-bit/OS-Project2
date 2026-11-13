
import threading
import random
import time

# Number of tellers and customers
NUM_TELLERS = 3
NUM_CUSTOMERS = 5

# Lock so prints don't mix
print_lock = threading.Lock()

# Last teller to get ready opens the bank
ready_lock = threading.Lock()
tellers_ready = 0
bank_open = threading.Event()

# Door lets 2 customers in at a time
door = threading.Semaphore(2)


# Print in the right format
def log(thread_type, tid, msg, other=""):
    with print_lock:
        print(f"{thread_type} {tid} [{other}]: {msg}")


# Teller thread
def teller(tid):
    global tellers_ready
    log("Teller", tid, "ready to serve")

    with ready_lock:
        tellers_ready += 1
        if tellers_ready == NUM_TELLERS:
            bank_open.set()

    log("Teller", tid, "waiting for a customer")


# Customer thread
def customer(cid):
    transaction = random.choice(["deposit", "withdrawal"])
    log("Customer", cid, f"wants to perform a {transaction} transaction")

    # Wait a bit before showing up
    time.sleep(random.uniform(0, 0.1))

    # Wait for the bank to open
    bank_open.wait()

    # Go through the door
    log("Customer", cid, "going to the door to enter")
    door.acquire()
    log("Customer", cid, "entered the bank")
    door.release()


# Start tellers then customers then wait for all
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
