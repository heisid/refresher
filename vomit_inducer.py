import imageio
from PIL import Image
import numpy as np
import os


def render_frame_numpy(input_array, width, height, scale, t, n):
    xs = np.linspace(-scale, scale, width)
    ys = np.linspace(scale, -scale, height)
    wx, wy = np.meshgrid(xs, ys)
    w = wx + 1j * wy

    r = t / n
    z = (1 - r) * w + r * np.log(w)

    src_x = ((z.real / scale) * (width / 2) + width / 2).astype(int)
    src_y = ((-z.imag / scale) * (height / 2) + height / 2).astype(int)

    valid = (src_x >= 0) & (src_x < width) & (src_y >= 0) & (src_y < height)

    output = np.zeros((height, width, 3), dtype=np.uint8)
    output[valid] = input_array[src_y[valid], src_x[valid]]

    return Image.fromarray(output)


def make_gif():
    frames = [Image.open(f"frames/frame_{i:03d}.jpg") for i in range(60)]
    frames[0].save("animation.gif", save_all=True, append_images=frames[1:], duration=40, loop=0)


def make_mp4(fps=25):
    writer = imageio.v2.get_writer("animation.mp4", fps=fps)
    for i in range(60):
        frame = imageio.v2.imread(f"frames/frame_{i:03d}.jpg")
        writer.append_data(frame)
    writer.close()


def main():
    input_img = Image.open("input.jpg")
    width, height = input_img.size
    input_array = np.array(input_img)

    scale = 2.0
    frames = 60
    os.makedirs("frames", exist_ok=True)

    for t in range(frames):
        frame = render_frame_numpy(input_array, width, height, scale, t, frames)
        frame.save(f"frames/frame_{t:03d}.jpg")


if __name__ == "__main__":
    main()
    make_mp4()
