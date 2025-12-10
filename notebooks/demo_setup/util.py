from collections.abc import Awaitable
import subprocess
import base64
from IPython.display import SVG
from IPython.display import display, clear_output, HTML
from time import sleep
from collections.abc import Callable
from pathlib import Path


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


def display_images(dir_path: str, per_row: int = 3, width: int = 250):
    dir_path = Path(dir_path)
    images = list(dir_path.rglob("*.jpeg"))
    
    html = ""

    for i in range(0, len(images), per_row):
        html += '<div style="display:flex; gap:10px;">'
        for img_path in images[i:i+per_row]:
            with open(img_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("ascii")
            html += (
                f'<img src="data:image/jpeg;base64,{encoded}" '
                f'style="width:{width}px; height:auto; margin-bottom:10px;">'
            )
        html += "</div>"

    display(HTML(html))
