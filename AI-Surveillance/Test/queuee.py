from collections import deque
import random

# Create a deque with a maximum size of 100
max_queue_size = 100
my_queue = deque(maxlen=max_queue_size)

# Function to insert data into the queue
def enqueue(data):
    my_queue.append(data)

while(1):
    r = random.randint(1,100)
    enqueue(r)

    # Print the queue
    print("Queue:", my_queue)
