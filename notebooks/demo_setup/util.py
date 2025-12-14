from collections.abc import Awaitable
import subprocess
from IPython.display import display, clear_output, SVG, HTML
from time import sleep
from collections.abc import Callable
from pathlib import Path
from minijinja import Environment
from textwrap import dedent
import numpy as np
import math
from base64 import b64encode
import itertools as it

ENVIRONMENT = Environment(
    templates={
        "image_grid": dedent(
            """
            {% for image_row in images -%}
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                {%- for image in image_row %}
                <img
                    src="{{ image }}"
                    style="width:{{ width }}px; height: {{ height }}px;"
                >
                {%- endfor %}
            </div>
            {% endfor -%}
            """
        ).strip()
    },
)


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


# def display_jpegs(
#     dir_path: str, column_count: int = 3, width: int = 250, height: int = 200
# ):
#     html = ENVIRONMENT.render_template(
#         "image_grid",
#         images=np.array_split(
#             (
#                 image_paths := [
#                     f"data:image/jpeg;base64,{b64encode(path.read_bytes()).decode('ascii')[0:30]}"
#                     for path in Path(dir_path).rglob("*.jpeg")
#                 ]
#             ),
#             math.ceil(len(image_paths) / column_count),
#         ),
#         width=width,
#         height=height,
#     )
#     return html
#     display(HTML(html))


def display_jpegs(
    dir_path: str, column_count: int = 3, width: int = 250, height: int = 200
):
    html = ENVIRONMENT.render_template(
        "image_grid",
        images=it.batched(
            (
                f"data:image/jpeg;base64,{b64encode(path.read_bytes()).decode('ascii')}"
                for path in Path(dir_path).rglob("*.jpeg")
            ),
            column_count,
        ),
        width=width,
        height=height,
    )
    # return html
    display(HTML(html))
