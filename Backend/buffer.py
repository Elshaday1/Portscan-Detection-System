# Initialize an empty list to act as the buffer memory
buffer_memory = []


def add_to_buffer(number):
    buffer_memory.append(number)
    
    # If the buffer memory exceeds three elements, remove the oldest number
    if len(buffer_memory) > 3:
        buffer_memory.pop(0)


add_to_buffer(5)
add_to_buffer(10)
add_to_buffer(15)

print(buffer_memory)
