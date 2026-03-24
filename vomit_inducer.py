from PIL import Image
import cmath
import math
import os


def pil_to_cartesian(x, y, width, height, scale):
    cx = (x - width / 2) / (width / 2) * scale
    cy = -(y - height / 2) / (height / 2) * scale
    return cx, cy


def cartesian_to_pil(x, y, width, height, scale):
    px = int((x / scale) * (width / 2) + width / 2)
    py = int((-y / scale) * (height / 2) + height / 2)
    return px, py


def transform(z, t):
    return z + 0.25 * cmath.sinh(0.5 * z * cmath.exp(1j * t))


def render_frame(input_pixels, width, height, scale, t):
    output_img = Image.new("RGB", (width, height))
    output_pixels = output_img.load()

    for x in range(width):
        for y in range(height):
            wx, wy = pil_to_cartesian(x, y, width, height, scale)
            w = complex(wx, wy)

            z = transform(w, t)

            src_x, src_y = cartesian_to_pil(z.real, z.imag, width, height, scale)

            if 0 <= src_x < width and 0 <= src_y < height:
                output_pixels[x, y] = input_pixels[src_x, src_y]

    return output_img


def make_gif():
    frames = [Image.open(f"frames/frame_{i:03d}.png") for i in range(60)]
    frames[0].save(
        "animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=40,
        loop=0
    )


def main():
    input_img = Image.open("input.jpg")
    width, height = input_img.size
    input_pixels = input_img.load()

    scale = 2.0
    frames = 60

    os.makedirs("frames", exist_ok=True)

    for i in range(frames):
        t = 2 * math.pi * i / frames
        frame = render_frame(input_pixels, width, height, scale, t)
        frame.save(f"frames/frame_{i:03d}.png")


if __name__ == "__main__":
    # main()
    make_gif()
