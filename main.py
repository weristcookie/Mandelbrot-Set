import argparse
import os
import matplotlib.pyplot as plt
import numpy as np

CONLIMIT = 50  # Limit that if exceeded defines a converging number
COUNTLIM = 100  # Max amount of iterations per calculation
SCALE = 0.005  # Scaling factor
DIM_FACTOR = 1 / SCALE  # Dimension factor

DIMENSION = {  # Dimensions of the coordinate system (-x, x, -y, y)
    "-x": -2,
    "x": 2,
    "-y": -2,
    "y": 2,
    "-xf": round(-2 * DIM_FACTOR),
    "xf": round(2 * DIM_FACTOR),
    "-yf": round(-2 * DIM_FACTOR),
    "yf": round(2 * DIM_FACTOR),
}

COLORS = [
    "\033[34m",  # Blue
    "\033[31m",  # Red
    "\033[33m",  # Orange
    "\033[93m",  # Yellow
    "\033[90m",  # Grey
    "\033[97m"   # White
]

RESET = "\033[0m"


def setDimension(factor: float, x: float, mx: float, y: float, my: float):  # TODO
    DIMENSION = {
        "x": round(x * 1/factor),
        "-x": round(mx * 1/factor),
        "y": round(y * 1/factor),
        "-y": round(my * 1/factor),
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

    color_index = int(count / (COUNTLIM / len(COLORS)))

    color_index = min(color_index, len(COLORS) - 1)

    return COLORS[color_index] + to_full_width(chr(0x2588)) + RESET


def calc(x: float, y: float, exponent: int = 2):
    c = complex(x, y)
    z = 0
    count = 0

    while abs(z) < CONLIMIT and count < COUNTLIM:
        z = z ** exponent + c
        count += 1

    return int(count)


def main_p(is_export: bool, exponent: float) -> None:
    x_coords = []
    y_coords = []
    colors = []

    for i in [x * SCALE for x in range(DIMENSION['-yf'], DIMENSION['yf'], 1)]:
        for j in [y * SCALE for y in range(DIMENSION['-xf'], DIMENSION['xf'], 1)]:
            # print(get_color(calc(x=j, y=i)), end=" ")
            # print(f"{calc(x = j, y = i):003}", end=" ")
            result = calc(x=j, y=i, exponent=exponent)
            if result < CONLIMIT:
                x_coords.append(j)
                y_coords.append(i)
                colors.append(result)
        # print()

    plt.xlim(DIMENSION['-x'], DIMENSION['x'])
    plt.ylim(DIMENSION['-y'], DIMENSION['y'])

    # plt.axhline(0, color='black', linewidth=0.5)
    # plt.axvline(0, color='black', linewidth=0.5)
    # plt.grid(False, which='both')

    plt.title(
        rf"A Mandelbrot set visualization using "
        rf"$z_{{n+1}} = z_n^{{{round(exponent, 1)}}} + c$"
    )

    plt.gca().set_facecolor('black')
    plt.scatter(x_coords, y_coords, marker="o", s=0.05, c=colors, cmap='magma')

    plt.xlabel("Real")
    plt.ylabel("Imaginary")

    plt.colorbar()

    if is_export:
        os.makedirs("output", exist_ok=True)
        filename = f"output-{round(exponent, 1)}.png"
        plt.savefig(os.path.join("output", filename))
        # ffmpeg -framerate 10 -pattern_type glob -i "output-*.png" -vf "scale=iw:-1:flags=lanczos" -loop 0 output.gif
    else:
        plt.show()

    plt.clf()


def main_t(scaling: float) -> None:
    if not scaling:
        width, height = os.get_terminal_size()
        scaling = (85 * 0.094) / width

    for i in [x * scaling for x in range(int(DIMENSION['-y'] * 1/scaling), int(DIMENSION['y'] * 1/scaling) + 1, 1)]:
        for j in [y * scaling for y in range(int(DIMENSION['-x'] * 1/scaling), int(DIMENSION['x'] * 1/scaling), 1)]:
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
            is_gif = True  # for now
            if is_gif:
                for exponent in np.arange(2, 8.1, 0.1):  # for now
                    # pass as par
                    filename = f"output-{round(exponent, 1)}.png"
                    print(f"Processing {filename}...")
                    main_p(is_export=args.export, exponent=exponent)
            main_p(is_export=args.export, exponent=2)
        else:
            main_t(args.scaling)
    except KeyboardInterrupt:
        pass
