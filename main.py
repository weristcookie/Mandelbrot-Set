conlim = 100 # Limit that if exceeded defines a converging number
countlim = 100 # Max amount of iterations per calculation
count = 0

scale = 0.1 # Scaling factor

DIMENSION = { # Dimensions of the coordinate system (-x, x, -y, y)
    "-x" : int(-2 * 1/scale),
    "x" : int(2 * 1/scale),
    "-y" : int(-2 * 1/scale),
    "y" : int(2 * 1/scale)
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
        if '!' <= char <= '~':  # Check if the character is in the ASCII printable range
            full_width_text += chr(ord(char) + 0xFEE0)  # Convert to full-width by adding offset
        else:
            full_width_text += char  # Keep non-ASCII characters unchanged
    return full_width_text


def get_color(count: int) -> str:
    if count >= countlim:
        return "\033[30m" + to_full_width("█") + RESET

    color_index = int(count / (countlim / len(COLORS)))

    color_index = min(color_index, len(COLORS) - 1)

    return COLORS[color_index] + to_full_width("█") + RESET


def calc(x: float, y: float):
    c = complex(x, y)
    z = 0
    count = 0

    while abs(z) < conlim and count < countlim:
        z_new = z ** 2 + c
        z = z_new
        count += 1

    return int(count)


def main():
    for i in [x * scale for x in range(DIMENSION["-y"], DIMENSION["y"], 1)]:
        for j in [y * scale for y in range(DIMENSION["-x"], DIMENSION["x"], 1)]:
            print(get_color(calc(x = j, y = i)), end=" ")
            #print(f"{calc(x = j, y = i):003}", end=" ")
        print()

main()