import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.colors import ListedColormap


def fun_fifo(processes):
    """First-In-First-Out scheduling algorithm."""
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    execution_order = []
    current_time = 0

    for process_name, arrival_time, burst_time in processes:
        if current_time < arrival_time:
            current_time = arrival_time
        start_time = current_time
        current_time += burst_time
        end_time = current_time
        execution_order.append((process_name, start_time, end_time))

    return execution_order


def fun_sjf(processes):
    """Shortest Job First scheduling algorithm."""
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    execution_order = []
    current_time = 0
    remaining_processes = processes[:]

    while remaining_processes:
        available_processes = [proc for proc in remaining_processes if proc[1] <= current_time]
        if available_processes:
            available_processes.sort(key=lambda x: x[2])
            shortest_process = available_processes[0]
            remaining_processes.remove(shortest_process)

            start_time = current_time
            current_time += shortest_process[2]
            end_time = current_time
            execution_order.append((shortest_process[0], start_time, end_time))
        else:
            current_time += 1

    return execution_order


def fun_round_robin(processes, quantum):
    """Round Robin scheduling algorithm."""
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    execution_order = []
    current_time = 0
    remaining_processes = processes[:]

    while remaining_processes:
        found_process = False
        for index, (process_name, arrival_time, burst_time) in enumerate(remaining_processes):
            if arrival_time <= current_time:
                found_process = True
                start_time = current_time
                if burst_time <= quantum:
                    current_time += burst_time
                    end_time = current_time
                    execution_order.append((process_name, start_time, end_time))
                    remaining_processes[index] = (process_name, arrival_time, 0)
                else:
                    current_time += quantum
                    end_time = current_time
                    execution_order.append((process_name, start_time, end_time))
                    remaining_processes[index] = (process_name, arrival_time, burst_time - quantum)

        remaining_processes = [proc for proc in remaining_processes if proc[2] > 0]
        if not found_process:
            current_time += 1

    return execution_order


def display_gantt_chart(execution_order, fig, ax):
    """Display the Gantt chart using matplotlib with unique colors for each process."""
    y_ticks = []
    y_labels = []
    max_time = 0

    # Generate a color map for unique processes
    unique_processes = list(set([proc[0] for proc in execution_order]))
    colors = plt.cm.tab20.colors  # Use a colormap with 20 distinct colors
    color_map = {proc: colors[i % len(colors)] for i, proc in enumerate(unique_processes)}

    for index, (process, start, end) in enumerate(execution_order):
        ax.barh(y=index, width=(end - start), left=start, align='center', height=1, color=color_map[process])
        ax.text((start + end) / 2, index, process, ha='center', va='center', color='black')
        y_ticks.append(index)
        y_labels.append(process)
        max_time = max(end, max_time)

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xticks(np.arange(0, max_time + 1, 1))
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(axis='x')


def run_scheduling(processes_entries, input_text, output_text, chart_frame, data_frame, selected_algorithm, quantum_entry):
    """Run the selected scheduling algorithm and display results."""
    processes = []
    input_text.config(state=tk.NORMAL)
    output_text.config(state=tk.NORMAL)
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

    try:
        for process_entry in processes_entries:
            name = process_entry["name"].get()
            arrival_time = int(process_entry["arrival"].get())
            burst_time = int(process_entry["burst"].get())

            if arrival_time < 0 or burst_time < 0:
                raise ValueError("Arrival and burst times must be non-negative.")

            processes.append((name, arrival_time, burst_time))

        if not processes:
            messagebox.showerror("Error", "Please add at least one process.")
            return

        # Display Input
        for proc in processes:
            input_text.insert(tk.END, f"Process: {proc[0]}, Arrival: {proc[1]}, Burst: {proc[2]}\n")
        input_text.config(state=tk.DISABLED)

        # Execute selected algorithm
        if selected_algorithm == "FIFO":
            execution_order = fun_fifo(processes)
        elif selected_algorithm == "Plus court d'abord":
            execution_order = fun_sjf(processes)
        elif selected_algorithm == "Round Robin":
            try:
                quantum = int(quantum_entry.get())
                if quantum <= 0:
                    raise ValueError("Quantum must be a positive integer.")
                execution_order = fun_round_robin(processes, quantum)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

        # Display Output
        for proc in execution_order:
            output_text.insert(tk.END, f"Process: {proc[0]}, Start: {proc[1]}, End: {proc[2]}\n")
        output_text.config(state=tk.DISABLED)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    # Clear old chart if it exists
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Create a matplotlib figure and axes
    fig, ax = plt.subplots(figsize=(8, 4))
    display_gantt_chart(execution_order, fig, ax)

    # Embed the Matplotlib figure into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Show the frame, label and text widget when run scheduler
    data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


def add_process_entry(process_frame, processes_entries):
    """Add a new process entry to the GUI."""
    process_num = len(processes_entries) + 1

    process_entry_frame = ttk.Frame(process_frame)
    process_entry_frame.pack(pady=5, fill=tk.X)

    name_label = ttk.Label(process_entry_frame, text=f"Process {process_num} Name:")
    name_label.pack(side=tk.LEFT)
    name_entry = ttk.Entry(process_entry_frame, width=10)
    name_entry.pack(side=tk.LEFT, padx=5)

    arrival_label = ttk.Label(process_entry_frame, text="Arrival Time:")
    arrival_label.pack(side=tk.LEFT)
    arrival_entry = ttk.Entry(process_entry_frame, width=5)
    arrival_entry.pack(side=tk.LEFT, padx=5)

    burst_label = ttk.Label(process_entry_frame, text="Burst Time:")
    burst_label.pack(side=tk.LEFT)
    burst_entry = ttk.Entry(process_entry_frame, width=5)
    burst_entry.pack(side=tk.LEFT, padx=5)

    processes_entries.append({"name": name_entry, "arrival": arrival_entry, "burst": burst_entry})


def clear_entries(processes_entries, input_text, output_text, chart_frame):
    """Clear all input fields and results."""
    for entry in processes_entries:
        entry["name"].delete(0, tk.END)
        entry["arrival"].delete(0, tk.END)
        entry["burst"].delete(0, tk.END)
    processes_entries.clear()
    input_text.config(state=tk.NORMAL)
    output_text.config(state=tk.NORMAL)
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    input_text.config(state=tk.DISABLED)
    output_text.config(state=tk.DISABLED)
    for widget in chart_frame.winfo_children():
        widget.destroy()


def toggle_quantum_entry(selected_algorithm, quantum_entry):
    """Toggle visibility of the quantum entry based on the selected algorithm."""
    if selected_algorithm == "Round Robin":
        quantum_entry.pack(side=tk.LEFT, padx=5)
    else:
        quantum_entry.pack_forget()


def create_gui():
    """Create the main GUI for the scheduling algorithms."""
    root = tk.Tk()
    root.title("Scheduling Algorithms")

    # Frame for algorithm selection
    algo_frame = ttk.Frame(root)
    algo_frame.pack(fill=tk.X, padx=10, pady=5)

    selected_algorithm = tk.StringVar(value="FIFO")

    fifo_radio = ttk.Radiobutton(algo_frame, text="FIFO", variable=selected_algorithm, value="FIFO",
                                 command=lambda: toggle_quantum_entry(selected_algorithm.get(), quantum_entry))
    fifo_radio.pack(side=tk.LEFT, padx=5)
    sjf_radio = ttk.Radiobutton(algo_frame, text="Plus court d'abord", variable=selected_algorithm, value="Plus court d'abord",
                                command=lambda: toggle_quantum_entry(selected_algorithm.get(), quantum_entry))
    sjf_radio.pack(side=tk.LEFT, padx=5)
    rr_radio = ttk.Radiobutton(algo_frame, text="Round Robin", variable=selected_algorithm, value="Round Robin",
                               command=lambda: toggle_quantum_entry(selected_algorithm.get(), quantum_entry))
    rr_radio.pack(side=tk.LEFT, padx=5)

    # Quantum Label and Entry
    quantum_label = ttk.Label(algo_frame, text="Quantum:")
    quantum_label.pack(side=tk.LEFT, padx=5)
    quantum_entry = ttk.Entry(algo_frame, width=5)
    quantum_entry.pack(side=tk.LEFT, padx=5)
    quantum_entry.pack_forget()  # Initially hidden

    # Frame for process entry
    process_entry_area = ttk.Frame(root)
    process_entry_area.pack(fill=tk.X, padx=10, pady=5)

    # Frame for text output
    data_frame = ttk.Frame(root)

    # Text widget for input process details
    input_label = ttk.Label(data_frame, text="Input Processes:")
    input_label.pack(anchor=tk.NW)
    input_text = tk.Text(data_frame, height=5, width=40)
    input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

    # Text widget for output execution order
    output_label = ttk.Label(data_frame, text="Execution Order:")
    output_label.pack(anchor=tk.NW)
    output_text = tk.Text(data_frame, height=5, width=40)
    output_text.pack(fill=tk.BOTH, expand=True)

    # Frame for chart output
    chart_frame = ttk.Frame(root)
    chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Keep track of process entries
    processes_entries = []

    # Create initial add process button
    add_button = ttk.Button(process_entry_area, text="Add",
                            command=lambda: add_process_entry(process_entry_area, processes_entries))
    add_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create run scheduler button
    run_button = ttk.Button(process_entry_area, text="Run",
                            command=lambda: run_scheduling(processes_entries, input_text, output_text, chart_frame, data_frame, selected_algorithm.get(), quantum_entry))
    run_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create clear button
    clear_button = ttk.Button(process_entry_area, text="Clear",
                              command=lambda: clear_entries(processes_entries, input_text, output_text, chart_frame))
    clear_button.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_gui()