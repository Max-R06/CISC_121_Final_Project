import gradio as gr
import matplotlib.pyplot as plt
import asyncio
import random

# ============================================================
#  GLOBAL CONTROL
# ============================================================
control = {
    "cancel": False,
    "pause": False,
    "delay": 0.05,
    "step_mode": False,
    "step_once": False,
}

# ============================================================
#  INPUT GENERATION
# ============================================================
def random_permutation(n):
    arr = list(range(1, n + 1))
    random.shuffle(arr)
    return [i * (100 / n) for i in arr]


# ============================================================
#  BUBBLE SORT (EARLY EXIT)
# ============================================================
async def bubble_sort_generator(n):
    arr = random_permutation(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_ylim(0, 100)
    ax.set_title("Bubble Sort")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    bars = ax.bar(range(n), arr, color="blue")
    yield fig

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):

            if control["cancel"]:
                return

            # PAUSE / STEP HANDLING
            while (control["pause"] or control["step_mode"]) and not control["step_once"] and not control["cancel"]:
                await asyncio.sleep(0.05)
            control["step_once"] = False

            for k, b in enumerate(bars):
                if k == j or k == j + 1:
                    b.set_color("red")
                elif k >= n - i:
                    b.set_color("green")
                else:
                    b.set_color("blue")
                b.set_height(arr[k])

            yield fig
            await asyncio.sleep(control["delay"])

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                for k, b in enumerate(bars):
                    b.set_height(arr[k])
                yield fig
                await asyncio.sleep(control["delay"])
                swapped = True

        bars[n - 1 - i].set_color("green")
        yield fig

        if not swapped:
            break

    for b in bars:
        b.set_color("green")
    yield fig


# ============================================================
#  SELECTION SORT
# ============================================================
async def selection_sort_generator(n):
    arr = random_permutation(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_ylim(0, 100)
    ax.set_title("Selection Sort")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    bars = ax.bar(range(n), arr, color="blue")
    yield fig

    for i in range(n):

        if control["cancel"]:
            return

        min_idx = i

        for j in range(i + 1, n):

            # PAUSE / STEP HANDLING
            while (control["pause"] or control["step_mode"]) and not control["step_once"] and not control["cancel"]:
                await asyncio.sleep(0.05)
            control["step_once"] = False

            if control["cancel"]:
                return

            for k, b in enumerate(bars):
                if k == min_idx:
                    b.set_color("purple")
                elif k == j:
                    b.set_color("red")
                elif k < i:
                    b.set_color("green")
                else:
                    b.set_color("blue")
                b.set_height(arr[k])

            yield fig
            await asyncio.sleep(control["delay"])

            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        for k, b in enumerate(bars):
            b.set_height(arr[k])
        bars[i].set_color("green")
        yield fig
        await asyncio.sleep(control["delay"])

    for b in bars:
        b.set_color("green")
    yield fig


# ============================================================
#  INSERTION SORT
# ============================================================
async def insertion_sort_generator(n):
    arr = random_permutation(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_ylim(0, 100)
    ax.set_title("Insertion Sort")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    bars = ax.bar(range(n), arr, color="blue")
    yield fig

    for i in range(1, n):
        key = arr[i]
        key_height = key     # store the visual height
        j = i - 1

        # Draw initial key bar
        for k, b in enumerate(bars):
            if k == i:
                b.set_color("purple")
                b.set_height(key_height)
            else:
                b.set_color("blue")
                b.set_height(arr[k])
        yield fig
        await asyncio.sleep(control["delay"])

        # IMPORTANT FIX:
        # Make a copy of arr EXCEPT mark arr[i] as "locked"
        # So arr[i] CAN'T be overwritten by the shift.
        temp = arr.copy()

        while j >= 0 and temp[j] > key:

            # Pause / step handling
            while (control["pause"] or control["step_mode"]) and not control["step_once"] and not control["cancel"]:
                await asyncio.sleep(0.05)
            control["step_once"] = False
            if control["cancel"]:
                return

            # SHIFT INTO temp, NOT arr
            temp[j+1] = temp[j]   # key slot never touched now

            # Draw
            for k, b in enumerate(bars):
                if k == j:
                    b.set_color("red")
                    b.set_height(temp[k])
                elif k == j + 1:
                    b.set_color("blue")
                    b.set_height(temp[k])
                elif k == i:
                    b.set_color("purple")
                    b.set_height(key_height)   # ALWAYS DRAW FIXED HEIGHT
                else:
                    b.set_color("blue")
                    b.set_height(temp[k])

            yield fig
            await asyncio.sleep(control["delay"])
            j -= 1

        # Now temp holds correct shifted positions.
        # Insert the key back in.
        temp[j + 1] = key_height

        # Copy temp back INTO arr
        arr = temp.copy()

        # Draw final step of this insertion
        for k, b in enumerate(bars):
            b.set_height(arr[k])
            if k <= i:
                b.set_color("green")
            else:
                b.set_color("blue")

        bars[j+1].set_color("green")

        yield fig
        await asyncio.sleep(control["delay"])

    for b in bars:
        b.set_color("green")
    yield fig

# ============================================================
#  QUICK SORT 
# ============================================================
async def quick_sort_generator(n):
    arr = random_permutation(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_ylim(0, 100)
    ax.set_title("Quick Sort Animation (Pivot Highlight)")
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    bars = ax.bar(range(len(arr)), arr, color="blue")
    yield fig

    stack = [(0, len(arr) - 1)]
    finalized = set()

    while stack:
        if control["cancel"]:
            return

        low, high = stack.pop()

        # Single-element range → immediately finalized
        if low >= high:
            if low == high:
                finalized.add(low)
                bars[low].set_color("green")
                yield fig
            continue

        pivot_idx = high
        pivot_val = arr[pivot_idx]
        i = low - 1

        # Highlight pivot
        for k, b in enumerate(bars):
            b.set_color("purple" if k == pivot_idx else
                        "green" if k in finalized else "blue")
            b.set_height(arr[k])
        yield fig
        await asyncio.sleep(control["delay"])

        # Partition loop
        for j in range(low, high):

            # Pause / step control
            while (control["pause"] or control["step_mode"]) and not control["step_once"] and not control["cancel"]:
                await asyncio.sleep(0.05)
            control["step_once"] = False
            if control["cancel"]:
                return

            # Highlight current comparison
            for k, b in enumerate(bars):
                if k == j:
                    b.set_color("red")
                elif k == pivot_idx:
                    b.set_color("purple")
                elif k in finalized:
                    b.set_color("green")
                else:
                    b.set_color("blue")
                b.set_height(arr[k])
            yield fig
            await asyncio.sleep(control["delay"])

            # Swap if needed
            if arr[j] <= pivot_val:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    for k, b in enumerate(bars):
                        b.set_height(arr[k])
                    bars[i].set_color("red"); bars[j].set_color("red")
                    yield fig
                    await asyncio.sleep(control["delay"])
                else:
                    bars[i].set_color("red")
                    yield fig
                    await asyncio.sleep(min(control["delay"], 0.02))

        # Final pivot placement
        pi = i + 1
        if pi != pivot_idx:
            arr[pi], arr[pivot_idx] = arr[pivot_idx], arr[pi]
            for k, b in enumerate(bars):
                b.set_height(arr[k])
            for k, b in enumerate(bars):
                b.set_color("green" if k == pi or k in finalized else "blue")
            yield fig
            await asyncio.sleep(control["delay"])
        else:
            bars[pi].set_color("green")
            yield fig
            await asyncio.sleep(control["delay"])

        finalized.add(pi)

        # Refresh all bar colors
        for k, b in enumerate(bars):
            b.set_color("green" if k in finalized else "blue")
            b.set_height(arr[k])
        yield fig
        await asyncio.sleep(control["delay"])

        # Push subranges
        if pi + 1 < high:
            stack.append((pi + 1, high))
        if low < pi - 1:
            stack.append((low, pi - 1))

    # Finished — all sorted
    for b in bars:
        b.set_color("green")
    yield fig


# ============================================================
#  START SORT
# ============================================================
async def start_sort(n, algorithm):
    control["cancel"] = False
    control["pause"] = False

    g = {
        "Bubble Sort": bubble_sort_generator,
        "Selection Sort": selection_sort_generator,
        "Insertion Sort": insertion_sort_generator,
        "Quick Sort": quick_sort_generator,
    }[algorithm]

    async for frame in g(n):
        yield frame


# ============================================================
#  BUTTON CALLBACKS
# ============================================================
def pause_sort():
    control["pause"] = True
    control["step_mode"] = False
    return gr.update()

def resume_sort():
    control["pause"] = False
    control["step_mode"] = False
    return gr.update()

def stop_sort():
    control["cancel"] = True
    control["pause"] = False
    control["step_mode"] = False
    return gr.update(value=None)

def step_once():
    control["step_mode"] = True
    control["pause"] = False
    control["step_once"] = True
    return gr.update()


def update_delay(new_delay):
    control["delay"] = new_delay


# ============================================================
#  UI
# ============================================================

#fixes bug on hugging face where scroll bar jitters and makes the screen shake
css_style = """
.gradio-container {
    overflow-y: scroll !important;
}
"""

with gr.Blocks(css=css_style) as demo:

    gr.Markdown("## Sorting Visualizer — Bubble, Selection, Insertion, Quick Sort\n"
                "**Comparing = red, Finalized = green**")

    with gr.Row():
        n = gr.Slider(8, 100, value=20, step=1, label="Number of Elements")
        alg = gr.Dropdown(
            ["Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort"],
            value="Bubble Sort",
            label="Algorithm"
        )

    delay = gr.Slider(0.005, 0.5, value=0.05, step=0.005, label="Delay (seconds)", interactive=True)

    with gr.Row():
        start_btn = gr.Button("Start", variant="primary")
        step_btn = gr.Button("Step")
        pause_btn = gr.Button("Pause")
        resume_btn = gr.Button("Resume")
        stop_btn = gr.Button("Stop")

    plot = gr.Plot()

    start_btn.click(start_sort, [n, alg], plot)
    step_btn.click(step_once, outputs=plot)
    pause_btn.click(pause_sort, outputs=plot)
    resume_btn.click(resume_sort, outputs=plot)
    stop_btn.click(stop_sort, outputs=plot)

    delay.change(update_delay, delay, outputs=None)

demo.launch()
