import argparse
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ProcessPoolExecutor

CONLIMIT = 50  # Limit that if exceeded defines a converging number
COUNTLIM = 100  # Max amount of iterations per calculation

COLORS = [
    "\033[34m",  # Blue
    "\033[31m",  # Red
    "\033[33m",  # Orange
    "\033[93m",  # Yellow
    "\033[90m",  # Grey
    "\033[97m"   # White
]

RESET = "\033[0m"

dimension = {}  # Dimensions of the coordinate system (x, -x, y, -y)


def set_dimension(scaling: float, x: float, mx: float, y: float, my: float):
    global dimension
    dimension = {
        "x": round(x / scaling),
        "-x": round(mx / scaling),
        "y": round(y / scaling),
        "-y": round(my / scaling),
    }


def to_full_width(text):
    full_width_text = ''
    for char in text:
        if '!' <= char <= '~':
            full_width_text += chr(ord(char) + 0xFEE0)
        else:
            full_width_text += char
    return full_width_text


def get_color(count: int) -> str:
    if count >= COUNTLIM:
        return "\033[30m" + to_full_width(chr(0x2588)) + RESET

    color_index = min(int(count / (COUNTLIM / len(COLORS))), len(COLORS) - 1)

    return COLORS[color_index] + to_full_width(chr(0x2588)) + RESET


def calc(x: float, y: float, exponent: int = 2):
    c = complex(x, y)
    z = 0
    count = 0

    while abs(z) < CONLIMIT and count < COUNTLIM:
        z = z ** exponent + c
        count += 1

    return int(count)


def main_p(is_export: bool, exponent: float, scaling: float) -> None:
    # If scaling is omitted, default scaling is used (0.005)
    if not scaling:
        scaling = 0.005

    set_dimension(scaling, 2, -2, 2, -2)

    x_coords = []
    y_coords = []
    colors = []

    for i in [x * scaling for x in range(dimension['-y'], dimension['y'], 1)]:
        for j in [y * scaling for y in range(dimension['-x'], dimension['x'], 1)]:
            # print(get_color(calc(x=j, y=i)), end=" ")
            # print(f"{calc(x = j, y = i):003}", end=" ")
            result = calc(x=j, y=i, exponent=exponent)
            if result < CONLIMIT:
                x_coords.append(j)
                y_coords.append(i)
                colors.append(result)
        # print()

    # Dimension already uses scaled values, but original values are needed here
    plt.xlim(round(dimension['-x'] * scaling), round(dimension['x'] * scaling))
    plt.ylim(round(dimension['-y'] * scaling), round(dimension['y'] * scaling))

    # plt.axhline(0, color='black', linewidth=0.5)
    # plt.axvline(0, color='black', linewidth=0.5)
    # plt.grid(False, which='both')

    plt.title(
        rf"A Mandelbrot set visualization using "
        rf"$z_{{n+1}} = z_n^{{{round(exponent, 2)}}} + c$"
    )

    plt.gca().set_facecolor('black')
    plt.scatter(x_coords, y_coords, marker="o", s=0.05, c=colors, cmap='magma')

    plt.xlabel("Real")
    plt.ylabel("Imaginary")

    plt.colorbar()

    if is_export:
        os.makedirs("output", exist_ok=True)
        filename = f"output-{round(exponent, 2)}.png"
        plt.savefig(os.path.join("output", filename))
    else:
        plt.show()

    plt.clf()


def main_t(scaling: float) -> None:
    # If scaling is omitted, automatic scaling is used
    if not scaling:
        width, _ = os.get_terminal_size()
        scaling = (85 * 0.094) / width

    set_dimension(scaling, 2, -2, 2, -2)

    for i in [x * scaling for x in range(dimension['-y'], dimension['y'] + 1, 1)]:
        for j in [y * scaling for y in range(dimension['-x'], dimension['x'], 1)]:
            print(get_color(calc(x=j, y=i)), end=" ")
            # print(f"{calc(x = j, y = i):003}", end=" ")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse optional command line arguments."
    )

    parser.add_argument(
        '-t', '--terminal',
        action='store_true',
        help='Show in terminal'
    )
    parser.add_argument(
        '-p', '--plot',
        action='store_true',
        help='Plot using matplotlib'
    )
    # Scaling refers to amount of rendered coordinates / coordinate density
    # Lower values -> higher density
    parser.add_argument(
        '-s', '--scaling',
        type=float,
        help='Set scaling'
    )
    parser.add_argument(
        '-e', '--export',
        action='store_true',
        help='Show in terminal'
    )

    args = parser.parse_args()

    try:
        if not args.terminal and not args.plot or args.plot:
            is_gif = False  # for now
            if is_gif:
                exponents = np.arange(2, 4.1, 0.05)  # for now
                with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                    futures = [
                        executor.submit(
                            main_p, is_export=args.export, exponent=exponent)
                        for exponent in exponents
                    ]

                    for future in futures:
                        future.result()

                ffmpeg_command = [
                    "ffmpeg",
                    "-framerate", "5",
                    "-pattern_type", "glob",
                    "-i", "output/output-*.png",
                    "-vf", "scale=iw:-1:flags=lanczos",
                    "-loop", "0",
                    "-y",
                    "output.gif"
                ]
                subprocess.call(ffmpeg_command)

            else:
                main_p(is_export=args.export, exponent=2, scaling=args.scaling)

        else:
            main_t(args.scaling)
    except KeyboardInterrupt:
        pass
