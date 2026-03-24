from PIL import Image
import cmath


def pil_to_cartesian(x, y, width, height, scale):
    cx = (x - width / 2) / (width / 2) * scale
    cy = -(y - height / 2) / (height / 2) * scale
    return cx, cy


def cartesian_to_pil(x, y, width, height, scale):
    px = int((x / scale) * (width / 2) + width / 2)
    py = int((-y / scale) * (height / 2) + height / 2)
    return px, py


def main():
    input_img = Image.open("input.jpg")
    width, height = input_img.size

    output_img = Image.new("RGB", (width, height))
    input_pixels = input_img.load()
    output_pixels = output_img.load()

    scale = 2.0  # zoom level

    for x in range(width):
        for y in range(height):
            wx, wy = pil_to_cartesian(x, y, width, height, scale)
            w = complex(wx, wy)

            # avoid singularity at 0
            if abs(w) < 1e-8:
                continue

            z = cmath.tanh(w)

            src_x, src_y = cartesian_to_pil(z.real, z.imag, width, height, scale)

            if 0 <= src_x < width and 0 <= src_y < height:
                output_pixels[x, y] = input_pixels[src_x, src_y]

    output_img.save("output.png")


if __name__ == "__main__":
    main()
