# Name: Giuseppe Galiazzi
# NetId: dal315218

import threading
import random
import time

# Number of tellers and customers
NUM_TELLERS = 3
NUM_CUSTOMERS = 50

# Lock so prints don't mix
print_lock = threading.Lock()

# Last teller to get ready opens the bank
ready_lock = threading.Lock()
tellers_ready = 0
bank_open = threading.Event()

# Door lets 2 customers in at a time
door = threading.Semaphore(2)

# Line of free tellers that customers pick from
line_lock = threading.Lock()
free_tellers = []
teller_free = threading.Semaphore(0)

# Semaphores for each teller so the teller and customer take turns
customer_here = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
ask_txn = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
gave_txn = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
txn_done = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
customer_left = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]

# What each teller's customer told them
teller_customer = [None] * NUM_TELLERS
teller_txn = [None] * NUM_TELLERS

# Safe fits 2 tellers and the manager talks to 1 at a time
safe = threading.Semaphore(2)
manager = threading.Semaphore(1)

# Set when all customers are gone
bank_closed = False


# Print in the right format
def log(thread_type, tid, msg, other=""):
    with print_lock:
        print(f"{thread_type} {tid} [{other}]: {msg}")


# Teller thread
def teller(tid):
    global tellers_ready
    counted = False

    while True:
        log("Teller", tid, "ready to serve")

        # Only count once for opening the bank
        if not counted:
            with ready_lock:
                tellers_ready += 1
                if tellers_ready == NUM_TELLERS:
                    bank_open.set()
            counted = True

        log("Teller", tid, "waiting for a customer")

        # Get in the free line so a customer can pick me
        with line_lock:
            free_tellers.append(tid)
        teller_free.release()

        # Wait for a customer to come up
        customer_here[tid].acquire()
        if bank_closed:
            log("Teller", tid, "leaving for the day")
            break

        cid = teller_customer[tid]
        other = f"Customer {cid}"
        log("Teller", tid, "serving a customer", other)

        # Ask for the transaction and wait for the answer
        log("Teller", tid, "asks for transaction", other)
        ask_txn[tid].release()
        gave_txn[tid].acquire()
        txn = teller_txn[tid]
        log("Teller", tid, f"handling {txn} transaction", other)

        # Withdrawals need the manager first
        if txn == "withdrawal":
            log("Teller", tid, "going to the manager", other)
            manager.acquire()
            log("Teller", tid, "getting manager's permission", other)
            time.sleep(random.uniform(0.005, 0.030))
            log("Teller", tid, "got manager's permission", other)
            manager.release()

        # Go in the safe and do the transaction
        log("Teller", tid, "going to safe", other)
        safe.acquire()
        log("Teller", tid, "enter safe", other)
        time.sleep(random.uniform(0.010, 0.050))
        log("Teller", tid, "leaving safe", other)
        safe.release()

        # Tell the customer it is done and wait for them to leave
        log("Teller", tid, f"finishes {txn} transaction.", other)
        txn_done[tid].release()
        log("Teller", tid, "wait for customer to leave.", other)
        customer_left[tid].acquire()


# Customer thread
def customer(cid):
    transaction = random.choice(["deposit", "withdrawal"])
    log("Customer", cid, f"wants to perform a {transaction} transaction")

    # Wait a bit before showing up
    time.sleep(random.uniform(0, 0.1))

    # Wait for the bank to open
    bank_open.wait()

    # Go through the door
    log("Customer", cid, "going to bank.")
    door.acquire()
    log("Customer", cid, "entering bank.")
    door.release()

    # Wait in line until a teller is free then take it
    log("Customer", cid, "getting in line.")
    log("Customer", cid, "selecting a teller.")
    teller_free.acquire()
    with line_lock:
        tid = free_tellers.pop(0)
    other = f"Teller {tid}"
    log("Customer", cid, "selects teller", other)

    # Say who I am and wait to be asked
    teller_customer[tid] = cid
    log("Customer", cid, "introduces itself", other)
    customer_here[tid].release()
    ask_txn[tid].acquire()

    # Give the transaction and wait for it to be done
    teller_txn[tid] = transaction
    log("Customer", cid, f"asks for {transaction} transaction", other)
    gave_txn[tid].release()
    txn_done[tid].acquire()

    # Leave the teller then leave through the door
    log("Customer", cid, "leaves teller", other)
    customer_left[tid].release()
    log("Customer", cid, "goes to door")
    door.acquire()
    log("Customer", cid, "leaves the bank")
    door.release()


# Start tellers then customers then close the bank when they are all done
def main():
    global bank_closed
    tellers = []
    customers = []

    for tid in range(NUM_TELLERS):
        t = threading.Thread(target=teller, args=(tid,))
        tellers.append(t)
        t.start()

    for cid in range(NUM_CUSTOMERS):
        t = threading.Thread(target=customer, args=(cid,))
        customers.append(t)
        t.start()

    for t in customers:
        t.join()

    # Wake up the tellers so they can go home
    bank_closed = True
    for tid in range(NUM_TELLERS):
        customer_here[tid].release()

    for t in tellers:
        t.join()

    print("The bank closes for the day.")


if __name__ == "__main__":
    main()
