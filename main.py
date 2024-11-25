import matplotlib.pyplot as plt

CONLIMIT = 100  # Limit that if exceeded defines a converging number
COUNTLIM = 100  # Max amount of iterations per calculation
SCALE = 0.005  # Scaling factor

DIMENSION = {  # Dimensions of the coordinate system (-x, x, -y, y)
    "-x": int(-2 * 1/SCALE),
    "x": int(2 * 1/SCALE),
    "-y": int(-2 * 1/SCALE),
    "y": int(2 * 1/SCALE)
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
        return "\033[30m" + to_full_width("█") + RESET

    color_index = int(count / (COUNTLIM / len(COLORS)))

    color_index = min(color_index, len(COLORS) - 1)

    return COLORS[color_index] + to_full_width("█") + RESET


def calc(x: float, y: float):
    c = complex(x, y)
    z = 0
    count = 0

    while abs(z) < CONLIMIT and count < COUNTLIM:
        z = z ** 2 + c
        count += 1

    return int(count)


def main():
    x_coords = []
    y_coords = []
    for i in [x * SCALE for x in range(DIMENSION["-y"], DIMENSION["y"], 1)]:
        for j in [y * SCALE for y in range(DIMENSION["-x"], DIMENSION["x"], 1)]:
            # print(get_color(calc(x=j, y=i)), end=" ")
            # print(f"{calc(x = j, y = i):003}", end=" ")
            result = calc(x=j, y=i)
            if result < CONLIMIT:
                x_coords.append(j)
                y_coords.append(i)
        # print()

    plt.xlim(-2, 2)
    plt.ylim(-2, 2)

    # plt.axhline(0, color='black', linewidth=0.5)
    # plt.axvline(0, color='black', linewidth=0.5)
    # plt.grid(False, which='both')

    plt.title("A Mandelbrot set visualization")
    plt.scatter(x_coords, y_coords, color='red', s=3, marker="s")

    plt.show()


main()
