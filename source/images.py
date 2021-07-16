from typing import List

import numpy as np
import PIL.Image


class Image:
    """Class taking care of image conversion and processing."""

    def __init__(
        self,
        file: str,
        cols: int = 80,
        scale: float = 0.43,
        resolution: int = 0,
        shade_str: str = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\()1{}[]?-_+~<>i!lI;:,\"^`'.",
        shade_min: str = "@#+-."
    ):
        """Convert an image file into ASCII art.

        :param file: The image file path, accepts `.jpg`, `.jpeg`, `.png` or any other image format.
        :param cols: Number of columns in the ascii image, defaults to 80
        :param scale: defines the adjusted aspect ratio for the ascii image, defaults to 0.43
        :param resolution: defines resolution, takes in values as percentage of the highest resolution possible with
               characters from shade_str
               Special value: 0 (default) is interpreted as mode switch to minimalistic output with characters from
               shade_min
        :param shade_str: defaults to a well known pattern of 69 characters used to define the greyscale
        :param shade_min: defaults to a minimalistic pattern of 5 characters used to define the greyscale
        """
        self.file = file
        self.image = PIL.Image.open(file).convert("L")
        if not (cols and scale):
            raise ValueError("Columns and Scale value can not be 0")
        else:
            self.cols = cols
            self.scale = scale
        self.shade = {
            "str": shade_str,
            "str_len": len(shade_str),
            "min": shade_min,
            "min_len": len(shade_min),
            "length": 0,
            "resolution": max(0, min(resolution, 100))  # Clamp resolution
        }

    def __repr__(self) -> str:
        return f'<Image file={self.file} image={self.image}>'

    def __str__(self) -> str:
        return '\n'.join(self.generate_ascii)

    def g_scale(self, resolution: int = 0) -> str:
        """
        Helper function to determine the character set based on the resolution

        :return: a string of characters which corresponds to the luminance in descending order
        """
        if resolution == 0:
            self.shade["length"] = self.shade["min_len"]
            return self.shade["min"]
        else:
            resolution = resolution * self.shade["str_len"] // 100
            # get evenly spaced indices and return them as a string
            indices = np.linspace(0, self.shade["str_len"] - 1, resolution, dtype=int)
            self.shade["length"] = len(indices)

            return ''.join(self.shade["str"][i] for i in indices)

    @staticmethod
    def get_average(image: PIL.Image) -> float:
        """Given a PIL Image, return an average value of luminance for the whole image."""
        im = np.array(image)
        w, h = im.shape
        return np.average(im.reshape(w * h))

    @property
    def generate_ascii(self) -> List[str]:
        """
        Convert the opened image into ASCII art

        :return: A list of strings each representing a row of the image.
        """
        horizontal, vertical = self.image.size
        self.cols = min(self.cols, horizontal)  # clamps the number of cols
        # compute tile dimensions based on aspect ratio and scale
        w = horizontal // self.cols
        h = int(w / self.scale)
        rows = vertical // h
        rows = min(rows, vertical)  # clamps the number of rows

        aimg = []
        # generate list of dimensions
        for i in range(rows):
            y1 = i * h
            y2 = (i + 1) * h
            aimg.append("")

            for j in range(self.cols):
                # crop image to tile
                x1 = int(j * w)
                x2 = int((j + 1) * w)

                # crop image to extract tile
                img = self.image.crop((x1, y1, x2, y2))
                # get average luminance
                avg = int(self.get_average(img))
                # look up ascii char
                scale = self.g_scale(resolution=self.shade["resolution"])
                # append ascii char to string
                aimg[i] += scale[(avg * (self.shade["length"] - 1)) // 255]

        return aimg
