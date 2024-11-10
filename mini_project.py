import PySimpleGUI as sg

# Memory Module
number_of_chips = 4
size_of_chips = 8
memoryChips = []
for i in range(number_of_chips):
    data = [""] * size_of_chips
    memoryChips.append([str(i), data])


def main():
    while True:
        menu_event, menu_values = menu_window.read()
        if menu_event == sg.WINDOW_CLOSED or menu_event == "Exit":
            break

        if menu_event == "-Button-":
            option = str(menu_values["-OPTION-"])
            if option == "1":
                menu_window.hide()
                read_memory_layout()
                menu_window.un_hide()
                menu_window["-OPTION-"].update("")

            elif option == "2":
                menu_window.hide()
                write_memory_layout()
                menu_window.un_hide()
                menu_window["-OPTION-"].update("")

            elif option == "3":
                menu_window.hide()
                # print_memory_layout()
                menu_window.un_hide()
                display_memory_layout()
                menu_window["-OPTION-"].update("")
            else:
                sg.popup("Please select the correct option")
                menu_window["-OPTION-"].update("")

        elif menu_event == "Import Memory Content":
            menu_window.hide()
            load_file_layout()
            menu_window.un_hide()
    menu_window.close()


def read_memory(address):
    # Read data from a specific address in the main memory
    return memoryChips[address // size_of_chips][1][address % size_of_chips]


def write_memory(address, data):
    # Write data to specific address in the main memory.
    # If the data is more than one character. Place it to the next address.
    # If the data is bigger than the available space, wrap around.
    for _ in range(len(data)):
        memoryChips[address // size_of_chips][1][address % size_of_chips] = data[_]
        # print(f" {address} , {data[_],}, end")
        address += 1
        if address >= size_of_chips * number_of_chips:
            address = 0


################################### GUI Coding ###################################
def read_memory_layout():
    read = [
        [sg.Text("Enter your memory address to read:", size=(30, 1))],
        [sg.Input(key="-ReadMemory-")],
        [sg.Button("Submit", key="-SUBMIT-"), sg.Button("Back", key="-BACK-")],
    ]
    read_window = sg.Window("Read Memory", read)
    while True:
        read_event, read_values = read_window.read()
        if read_event == "-BACK-" or read_event == sg.WINDOW_CLOSED:
            break
        if read_event == "-SUBMIT-":
            address = read_values["-ReadMemory-"]
            if address == "" or not address.isnumeric():
                sg.popup(
                    f"Please enter the address between 0 and {size_of_chips*number_of_chips - 1}"
                )
            else:
                address = int(address)
                if address < 0 or address > (size_of_chips * number_of_chips - 1):
                    sg.popup(
                        f"Please select the address between 0 and {size_of_chips*number_of_chips - 1}"
                    )
                else:
                    data = read_memory(address)
                    sg.popup("Data at address " + str(address) + " is: " + str(data))
                    # read_window['-ReadMemory-'].update('')
            read_window["-ReadMemory-"].update("")
    read_window.close()


##################################################################################################
def write_memory_layout():
    write = [
        [
            sg.Text("Enter address to write:"),
            sg.Input(key="-Write_address-", size=(10, 1)),
        ],
        [sg.Text("Enter data to write:"), sg.Input(key="-Write_data-", size=(10, 1))],
        [sg.Button("Submit", key="-SUBMIT-"), sg.Button("Back", key="-BACK-")],
    ]
    write_window = sg.Window("Write Memory", write)

    while True:
        write_event, write_values = write_window.read()
        if write_event == "-BACK-" or write_event == sg.WINDOW_CLOSED:
            break
        if write_event == "-SUBMIT-":
            address = write_values["-Write_address-"]
            if address == "" or not address.isnumeric():
                sg.popup(
                    f"Please enter the address between 0 and {size_of_chips*number_of_chips - 1}"
                )
            else:
                address = int(address)
                if address < 0 or address > (size_of_chips * number_of_chips - 1):
                    sg.popup(
                        f"Please select the address between 0 and {size_of_chips*number_of_chips - 1}"
                    )
                else:
                    data = write_values["-Write_data-"]
                    write_memory(address, data)
                    display_multiple_message_line(address, data)
                write_window["-Write_address-"].update("")
                write_window["-Write_data-"].update("")
            write_window["-Write_address-"].update("")
            write_window["-Write_data-"].update("")
    write_window.close()


##################################################################################################
def display_multiple_message_line(address, data):
    count = data
    data_message = []

    for _ in range(len(data)):
        data_message.append(f"Data {data[_]} written to the address {address}")
        address += 1
        if address >= (size_of_chips * number_of_chips):
            address = 0

    if len(data) == 0:
        data_message.append("No data written to the memory.")

    data_message_layout = [
        [sg.Multiline("\n".join(data_message), size=(40, 20))],
        [sg.Button("OK", button_color="green")],
    ]

    data_message_window = sg.Window("Data input message", data_message_layout)

    while True:
        data_message_event, data_message_values = data_message_window.read()
        if data_message_event == sg.WINDOW_CLOSED or data_message_event == "OK":
            break

    data_message_window.close()


####################################################################################################


def display_memory_layout():  ###change
    print_memory_layout = []
    for i in range(number_of_chips):
        initial_address = i * size_of_chips
        data = []
        for address in range(size_of_chips):
            chip_memory = memoryChips[i][1][address]
            data.append([str(initial_address + address), chip_memory])

        print_memory_address = [
            [
                sg.Text(
                    f"Chip {i}", justification="center", font=("Helvetica", 16, "bold")
                )
            ],
            [sg.Table(data, headings=["Address", "Content"], justification="center")],
        ]
        print_memory_layout.extend(print_memory_address)
    frame = [[sg.Frame("Memory Contents", print_memory_layout)]]

    # Main Layout
    window_layout = [
        [
            sg.Button("Close", button_color="red"),
            sg.Button("Export", button_color="green"),
            sg.Button("Refresh", button_color="green"),
        ],
        [
            sg.Column(
                frame, size=(400, 300), scrollable=True, vertical_scroll_only=True
            ),
            sg.VerticalSeparator(),
        ],
    ]

    window = sg.Window("Memory Contents", window_layout)
    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WINDOW_CLOSED:
            break

        elif event == "Export":
            while True:
                f = sg.popup_get_file(
                    "Save Memory Contents",
                    save_as=True,
                    file_types=(("Text Files", "*.txt"),),
                )
                if f:
                    file = open(f, "w")
                    for m, n in enumerate(memoryChips):
                        file.write(f"Chip{m} \n")
                        file.write("Address\tContent\n")
                        for i, j in enumerate(n[1]):
                            address_of_chip = m * size_of_chips + i
                            if address_of_chip <= (size_of_chips * number_of_chips - 1):
                                file.write(f"{address_of_chip}\t{j}\n")
                        file.write(
                            "################################################################################################### \n"
                        )
                    file.close()
                    sg.popup("Data Exported successfully.")
                    break
                elif f == "":
                    sg.popup("Please insert a location to write a file")
                else:
                    break
        elif event == "Refresh":
            clear_memory()
            window.close()
    window.close()


def clear_memory():  ###add
    counter = 0
    for counter in range(size_of_chips * number_of_chips):
        data = read_memory(counter)
        if counter < (size_of_chips * number_of_chips):
            if data != "":
                data_new = [""] * size_of_chips
                write_memory(counter, data_new)
            counter += 1
    display_memory_layout()


##################################################################################################
def load_file_layout():  ###change
    contents = []
    counter = 0
    load_file_layout = [
        [sg.Text("Select a text file:"), sg.Input(key="-file-"), sg.FileBrowse()],
        [
            sg.Button("Import", button_color="green", key="Import"),
            sg.Button("Cancel", button_color="red", key="Cancel"),
        ],
    ]

    load_file_window = sg.Window("Import file", load_file_layout)
    while True:
        load_file_event, load_file_values = load_file_window.read()

        if load_file_event == sg.WINDOW_CLOSED or load_file_event == "Cancel":
            break

        if load_file_event == "Import":
            while True:
                try:
                    file = load_file_values["-file-"]
                    f = open(file, "r")
                    f_cleared_newline = f.read().replace("\n", "")
                    for x in f_cleared_newline:
                        if counter < (size_of_chips * number_of_chips):
                            if (
                                memoryChips[counter // size_of_chips][1][
                                    counter % size_of_chips
                                ]
                                == ""
                            ):
                                contents = x
                                write_memory(counter, contents)
                            counter += 1
                    f.close()
                    sg.popup("The contents succesfully loaded to the address")
                    load_file_window["-file-"].update("")
                    load_file_window.close()
                    break
                except:
                    sg.popup("Please import a valid file")
                    break

    # Close the window
    load_file_window.close()


########################################################################################################################
menu_bar = [["File", ["Import Memory Content"]]]
menu = [
    # [sg.ButtonMenu(['Menu'], menu_def=menu_bar, button_color='green', key='menu_bar')],
    [sg.Text("1. Read Memory", size=(20, 1))],
    [sg.Text("2. Write Memory", size=(20, 1))],
    [sg.Text("3. Print Memory Content", size=(20, 1))],
    [sg.Text("Enter your option:"), sg.Input(key="-OPTION-", size=(20, 1))],
    [
        sg.Button("OK", key="-Button-", button_color="green"),
        sg.Button("Exit", button_color="red"),
    ],
]

menu_frame = [[sg.Menu(menu_bar, key="menu_bar")], [sg.Frame("Option choosing", menu)]]

menu_window = sg.Window("Memory", menu_frame)

main()
