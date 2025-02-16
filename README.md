# **Scheduling Algorithms - Gantt Chart Visualizer**

This project is a **Graphical User Interface (GUI)** application built with **Tkinter** and **Matplotlib** that allows users to simulate and visualize various **CPU scheduling algorithms** with an interactive **Gantt chart**.

## **Features 🚀**
✅ Supports **FIFO (First In First Out)**, **SJF (Shortest Job First)**, and **Round Robin** scheduling algorithms.  
✅ User-friendly interface for adding processes dynamically.  
✅ **Gantt chart visualization** for better understanding of process execution.  
✅ Input validation and error handling for smooth user experience.  

## **Technologies Used 🛠️**  
- **Python** (Tkinter for GUI)  
- **Matplotlib** (for Gantt Chart visualization)  
- **NumPy** (for handling numerical data)  

## **How to Use 📌**  
1. Select the scheduling algorithm (**FIFO, SJF, or Round Robin**).  
2. Enter process details (**Name, Arrival Time, Burst Time**).  
3. Click **"Run"** to see the scheduling execution order and **Gantt chart**.  
4. If using **Round Robin**, enter the quantum value.  

## **Installation & Run 🏃**  
```bash
git clone https://github.com/ElouakfaouiYassine/scheduling-algorithms.git
cd scheduling-algorithms
pip install matplotlib numpy
python main.py
