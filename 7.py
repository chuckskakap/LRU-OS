# Constants
MEMORY_CHIP_SIZE = 1024  # Size of each memory chip in bytes (1 kilobyte)
MEMORY_MODULE_SIZE = 1000  # Number of memory chips per module
TOTAL_MEMORY_SIZE = 1024 * 1024 * 1024  # Total memory size in bytes (1 gigabyte)

# Calculate the number of memory modules and chips
num_modules = TOTAL_MEMORY_SIZE // (MEMORY_CHIP_SIZE * MEMORY_MODULE_SIZE)
num_chips = num_modules * MEMORY_MODULE_SIZE

# Create the main memory array
memory_array = [[0] * MEMORY_MODULE_SIZE for _ in range(num_modules)]


# Function to read data from a specific memory address
def read_memory(address):
    module_index = address // MEMORY_MODULE_SIZE
    chip_index = address % MEMORY_MODULE_SIZE
    return memory_array[module_index][chip_index]


# Function to write data to a specific memory address
def write_memory(address, data):
    module_index = address // MEMORY_MODULE_SIZE
    chip_index = address % MEMORY_MODULE_SIZE
    memory_array[module_index][chip_index] = data


# Example usage
memory_address = 50000
data_to_write = 42

write_memory(memory_address, data_to_write)
read_data = read_memory(memory_address)

print(f"Read data: {read_data}")
