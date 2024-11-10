def lru(capacity, pages, order):
    data = [int(x) for x in order.split()[:pages]]
    result = []
    ref = []  # store index to be used next
    num_fault = 0  # count the number of page fault

    for i in data:
        if i not in result:
            if len(result) < capacity:
                # directly load the data to page frame
                result.append(i)
                # append index of element in "result" to "ref"
                ref.append(len(result) - 1)

            else:
                # if greater than capacity, pop out the index from ref and
                # assign the result[index] to the data to be added to ref
                index = ref.pop(0)  # pop out the least recently used element
                result[index] = i  # replace that index with new data
                # add back the index to ref list -> recently used
                ref.append(index)

            num_fault += 1
            status = "Page Fault"

        else:
            # index of data in ref will be pop out to be appended into ref again -> recently used
            ref.append(ref.pop(ref.index(result.index(i))))
            status = "Page Hit"

        # display
        print("  %d\t\t" % i, end=" ")
        for y in result:
            print(y, end=" ")

        for k in range(capacity - len(result)):
            print(" ", end=" ")

        print("   %s" % status)

    print(
        "\nTotal Request: %d\nTotal Page Faults: %d\nTotal Page Hit: %d"
        % (pages, num_fault, (pages - num_fault))
    )
    failure_rate = (num_fault / pages) * 100
    print(f"Failure Rate: {failure_rate:.2f}%")


print("Least Recently Used (LRU)")
page_frame = int(input("Enter the no. of page frames available: "))
num_pages = int(input("Enter the no. of pages to execute: "))
exec_order = input("Please enter your loading data: ")
print()
lru(page_frame, num_pages, exec_order)
# 7 0 1 2 0 3 0 4 2 3 0 3 1 2 0
