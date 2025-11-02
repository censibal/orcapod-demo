from collections.abc import Awaitable
import subprocess
from IPython.display import SVG
from IPython.display import display, clear_output
from time import sleep
from collections.abc import Callable


async def print_crash(long_task: Awaitable):
    try:
        return await long_task
    except Exception as exception:
        print(f"{long_task.__name__} CRASHED: {exception}")


def display_dot(dot_data: str):
    svg_bytes, _ = subprocess.Popen(
        ["dot", "-T", "svg"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate(dot_data.encode())

    return SVG(data=svg_bytes)


def animate_display(next_display_object: Callable):
    while display_object := next_display_object():
        clear_output()
        display_handle = display(display_id="current")
        display_handle.update(display_object)
        sleep(0.1)
