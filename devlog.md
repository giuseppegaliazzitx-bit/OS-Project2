# Devlog - CS4348 Project 2 (Bank Simulation)

## Session 1

### Nov 12, 2:05pm - Plan
This project is a bank with 3 tellers and 50 customers, and I have to use
threads and semaphores. Before I start coding I want to figure out what parts
need to be shared and locked:
- The safe can only hold 2 tellers, so I think a semaphore set to 2.
- The manager can only talk to 1 teller at a time, so a semaphore set to 1.
- The door only lets 2 customers in at a time, so a semaphore set to 2.
- Customers can't come in until all 3 tellers are ready.
- The customer and teller have to go back and forth. For example, hi, what do you want, ok
  wait,then done, so I'll probably need a few semaphores for each teller and a
  variable to hold the transaction.

For today I just want to get the threads to run and print in the format the
assignment wants: `TYPE ID [OTHER ID]: MSG`. I'll start with only 3 customers
so the output is small, and add the real syncing later.

### Nov 12, 3:24pm - Reflection
Got it running. bank.py starts 3 teller threads and 3 customer threads. The
tellers say they are ready and waiting, and the customers say what transaction
they want. At first the lines were printing over each other, so I added a lock
around print to fix that. Nothing is actually synced yet, the customers just
talk whenever, but that's fine for now. Next time I'll make the customers wait
for the bank to open and add the door.
