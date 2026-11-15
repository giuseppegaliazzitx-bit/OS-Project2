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

## Session 2

### Nov 12, 3:56pm - Plan
Last time the customers just entered whenever, which is wrong because the bank
should not be open until all 3 tellers are ready. So this session I want to:
- Make the tellers count themselves as ready, and have the last one open the bank.
- Make the customers wait for that before they do anything.
- Add the door so only 2 customers can go through at a time.
I think I can use an Event for the bank opening (set it once all tellers are
ready) and a Semaphore with 2 permits for the door.

### Nov 12, 10:39pm - Reflection
Finished session 2 plan after 2 days since i got tired. The tellers now add 
themselves to a counter (with a lock so two tellers don't update it at the same
time) and the last one to get ready sets the bank_open event. The customers 
call bank_open.wait() so none of them enter until the bank is actually open, which
I checked by seeing all the "ready" lines print before any "entered" line. The door
is a Semaphore(2) that each customer acquires and releases so only 2 are in the
doorway at once. Still no talking to the tellers yet which i left for the next session.

## Session 3

### Nov 13, 10:48am - Plan
Right now the customers get into the bank but they never actually talk to a
teller so the plan for this session is to allow them to talk to each other.
- A customer waits for any teller that is free, then picks that teller.
- The customer tells the teller its ID then the teller asks what it wants.
- The customer gives the transaction and the teller says it is done.
- Then the customer leaves and the teller goes back to waiting.
So what i believe i ened is to make a semaphore for free tellers plus a few 
semaphores for each teller so they can take turns and a variable to hold the 
customer ID and the transaction.

### Nov 13, 1:02pm - Reflection
Got the customers and tellers talking to eahcother, when a teller is free it puts itself in
a list and adds to a teller_free semaphore then a customer waits on that, takes the
first teller in the list and then they take turns with a few semaphores for
each teller. The customer ID and the transaction go in a list spot for that
teller so the teller can read them. Each teller now loops and serves more than
one customer. I also needed a way to end the program because the tellers were
stuck waiting forever after the last customer left so wha ti did is  main sets a closed flag
and wakes up each teller so it can leave. I ran it a bunch of times with 5 and
with 50 customers and it never got stuck.

## Session 4

### Nov 13, 1:41pm - Plan
Now that customers and tellers can talk, this session I want to add the safe
and the manager. The safe only fits 2 tellers at a time so it will be a
semaphore that starts at 2, and the manager only talks to 1 teller at a time
so that one starts at 1. If the customer wants a withdrawal the teller has to
go get the manager's permission first, which takes 5 to 30ms. Then for every
transaction the teller goes into the safe, which takes 10 to 50ms. I need to
print before and after each of these so you can tell who is waiting and who
is using it. I also want to double check that the manager and safe never have
too many tellers at once.

### Nov 14, 11:07am - Reflection
Added the safe and the manager. The safe is a semaphore that starts at 2 and
the manager is one that starts at 1. After the teller gets the transaction, if
it is a withdrawal it goes to the manager first and sleeps 5 to 30ms, then for
every transaction it goes in the safe and sleeps 10 to 50ms. Each one prints
going, using and done so you can see who is waiting. I ran it a bunch of times
with 5 and 50 customers and checked the output, the safe never had more than 2
tellers and the manager never had more than 1 and it still never got stuck.
Next session is running it with all 50 customers and cleaning up the output.

## Session 5

### Nov 15, 11:17am - Plan
The safe and the manager work now so this should be the last session. I want
to switch to the full 50 customers and make the output match the sample run.
Some of my messages are worded a little different from the sample like
"going to the door to enter" when the sample says "going to bank." so I will
go through the sample and fix those. I also want to run it a lot of times with
50 customers to make sure it always ends and never gets stuck, and that every
customer leaves the bank.

### Nov 15, 12:58pm - Reflection
Changed it to 50 customers and went through the sample output line by line to
fix my messages. The customer now says "going to bank.", "entering bank.",
"getting in line." and "selecting a teller." and the teller messages that had
periods in the sample have them now too. I ran it a couple of times with 50
customers and every time all 50 left the bank, the safe never had more than 2
tellers, the manager never had more than 1 and it always printed that the bank
closes at the end.
