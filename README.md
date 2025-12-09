---
title: Final Project
emoji: 📊
colorFrom: red
colorTo: gray
sdk: gradio
sdk_version: 6.0.2
app_file: app.py
pinned: false
license: mit
short_description: Sorting Visualizer for CISC 121 final project
---
# Sorting Visualizer

A real-time, interactive visualization of sorting algorithms, designed to demonstrate the efficiency differences between $O(n \log n)$ and $O(n^2)$ algorithms.

** Hugging Face:** [Final Project - Hugging Face Space](https://huggingface.co/spaces/MaxwellR/Final_Project)

---

## Algorithm Choices

### Quick Sort (Primary Focus)
I chose to visualize **Quick Sort** because visualizing an $O(n \log n)$ time complexity sort offers an interesting contrast to simpler methods. Unlike Merge Sort, which is typically an out-of-place algorithm, Quick Sort is done in-place, making the visualization of elements swapping within the array much clearer and aesthetically pleasing.

* **Implementation Details:** This project uses a **2-partition Quick Sort** (Lomuto partition scheme) with a **last-element pivot**.

### Quadratic Sorts
I have also implemented quadratic sorts (e.g., Bubble, Selection, Insertion) to better demonstrate the comparative advantage and speed superiority of logarithmic sorts like Quick Sort, especially on larger datasets.

---

## Computational Thinking Breakdown

### 1. Decomposition
* **User Interface (UI):**
    * Controls allow the user to pause, play, terminate, and generate a new sort.
    * Sliders allow adjustment of sorting speed and array size.
* **UI Logic:**
    * **State Management:** The system checks the state after every chart update to handle user inputs (pause, play, step) responsively.
    * **Speed Control:** A "delay" variable governs the speed of the sort, dynamically updated by the slider input.
* **Visualization Update:**
    * **Efficiency:** Instead of redrawing the entire graph for each frame, the program only updates the bars that are actively changing.
    * **Color Coding:**
        * **Purple:** Key elements (Pivot in Quick Sort, Min value in Selection Sort, Key in Insertion Sort).
        * **Red:** Active comparisons.
        * **Green:** Sorted elements.

### 2. Pattern Recognition
* **Sorting Algorithms:**
    * All algorithms share the same control logic for speed and user inputs.
    * Standard sorting logic is maintained, with the addition of graph updates and asynchronous pauses.
    * All algorithms are **in-place**, simplifying the visualization logic.
* **Visual Consistency:**
    * Colors are consistent across all algorithms so the user does not need to relearn the visual language.
    * The array bar representation remains constant for all modes.

### 3. Abstraction
* **Data Representation:** The project abstracts away specific numerical values. The user focuses on the "shape" of the data (bar height) rather than the numbers, which is clearer for large input sizes.
* **Control Logic:** The sorting algorithms do not interact directly with complex UI event listeners. They simply check boolean flags (e.g., `paused == True`) to determine behavior.

### 4. Algorithm Design
* **Flow:**
    * A random array is generated (using a shuffle method to create a perfect "staircase" of values).
    * The user interacts via the UI to Sort, Pause, Resume, Step, or Adjust Speed.
    * The visualization updates in real-time until the array is fully sorted.
* **Generator Implementation:**
    * Algorithms are designed as **generators** that yield control at each step. This allows the function to pause or terminate on command without freezing the application.

___
```text
       +-------------------------+
       |      START PROGRAM      |
       +-----------+-------------+
                   |
                   v
       +-------------------------+
       |    Initialize Globals   |
       | control: pause=False... |
       +-----------+-------------+
                   |
                   v
       +-------------------------+
       |     SETUP GRADIO UI     |
       | Buttons, Sliders, Plot  |
       +-----------+-------------+
                   |
                   v
       +-------------------------+      +-------------------------+
+----->|   WAIT FOR USER INPUT   |<-----|     Update Settings     |<----+
|      +-----------+-------------+      +-------------------------+     |
|                  |                                                    |
|                  +----(User adjusts sliders)--------------------------+
|                  |                                                    |
|                  +----(User clicks Pause/Stop)---+                    |
|                  |                               |                    |
|                  v                               v                    |
|          (User Clicks Start)          +-------------------------+     |
|                  |                    |       Update Flags      |-----+
|                  |                    +-------------------------+
|                  v
|      +-------------------------+
|      |       RESET FLAGS       |
|      | cancel=False, pause=False|
|      +-----------+-------------+
|                  |
|                  v
|      +-------------------------+
|      |    SELECT ALGORITHM     |
|      +----+------+-------------+
|           |      |      |
|           |      |      +----------> [ Bubble Sort Generator ]
|           |      +-----------------> [ Quick Sort Generator  ]
|           +------------------------> [ Insertion/Selection   ]
|                  |
|                  v
|      +-------------------------+
|      |  GENERATOR LOOP STARTS  |<----------------------------------+
|      +-----------+-------------+                                   |
|                  |                                                 |
|                  v                                                 |
|      +-------------------------+                                   |
|      |   CHECK CONTROL FLAGS   |                                   |
|      +----+------+-------------+                                   |
|           |      |                                                 |
|           |      +---(Paused?)-----> +---------------------+       |
|           |                          |      Async Wait     |-------+
|           +---(Canceled?)----------> +---------------------+
|           |
|           v
|      +-------------------------+
|      |  PERFORM SORTING LOGIC  |
|      | Compare Elements/Swap   |
|      +-----------+-------------+
|                  |
|                  v
|      +-------------------------+
|      |     UPDATE VISUALS      |
|      | Set Heights & Colors    |
|      +-----------+-------------+
|                  |
|                  v
|      +-------------------------+
|      |    YIELD FIGURE TO UI   |
|      |     (Screen Update)     |
|      +-----------+-------------+
|                  |
|                  v
|      +-------------------------+
|      |       ASYNC SLEEP       |
|      |   Wait 'delay' seconds  |
|      +-----------+-------------+
|                  |
+------------------+
                   |
                   v
       +-------------------------+
       |      SORT COMPLETE      |
       +-----------+-------------+
                   |
                   v
       +-------------------------+
       |         FINISH          |
       |    (Color All Green)    |
       +-------------------------+
```
---
## Steps to Run Locally
* **1. Prerequisites**
    * Ensure you have Python 3.7+ installed on your system.
* **2. Download the Project**
    * Download the project files to a folder on your computer
* **3. Set Up a Virtual Environment (Recommended)**
    * It is best practice to use a virtual environment to manage dependencies.
* **4. Install Dependencies**
    * Install the required libraries using the requirements file.
    * In terminal:
    * pip install -r requirements.txt
 
* **5. Run the Application**
    * In terminal:
    * python app.py

* **6. Open in Browser**
    * A private link should appear to open in a browser

---

## Testing & Robustness
 [**Demo Video**](https://drive.google.com/file/d/1yrT-Po8ZkXcQFXLWL6onbVXIPtFYbVb6/view?usp=sharing)\
 
*The application (CICS_121_Final_demo) has been tested against the following criteria:

* **Input Spamming:** Rapid clicking of buttons does not cause crashes or logic errors.
* **Bistable Logic:** Clicking "Pause" while already paused (or Play while playing) has no adverse effect.
* **Live Adjustments:** The delay slider can be adjusted rapidly during execution without breaking the sort loop.
* **Scalability:** All algorithms function correctly across the full range of input sizes and delay times (though quadratic sorts naturally take longer on large inputs).
* **Stepping:** The "Step" button correctly advances the algorithm by exactly one frame/operation.

---

## Author & Acknowledgements

**Author:** Maxwell Roemer

### AI Acknowledgement (Level 4)
**Level 4: Code Generation & Significant Assistance**

I acknowledge the use of Artificial Intelligence tools (Google Gemini) to assist in the development of this project. AI was utilized at Level 4, contributing to:

* **Code Generation:** Generating the basic structure for the sorting algorithms and Gradio UI components.
* **Debugging:** Identifying errors and inefficiencies in the code, as well as problem-solving with directories, paths, and environment configuration.
* **FlowChart** Used AI to create text based flow chart from physical writen version
