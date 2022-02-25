import base64
import lzma
from PIL import Image


def main():
    art_text_string = "XQAAAQAABAAAAAAAAAAAbh5RhjiWQJWnRyI9rtRTFHEIieb8urxGUYiJiIyU9+KHoIwF9T1Sw5De5ZSC5Q1/8SR303lFL5nIhy6qnWmTZBIHvr2bdE2ud4vxFgA="
    art = Art(art_text_string=art_text_string)
    print(art)
    print(art.generate_art_text_string())

    art.generate_art_image_32x32(10).save("output/image.png")


class Art:
    __art_size = (32, 32)
    __art_text_string: str = None
    __raw_art_data: list[int] = None
    __chunked_raw_art_data: list[list[int]] = None

    def __init__(
        self,
        art_text_string: str = None,
        raw_art_data: list[int] = None,
        chunked_raw_art_data: list[list[int]] = None,
        auto_generate_data: bool = True,
    ):
        self.__art_text_string = art_text_string
        self.__raw_art_data = raw_art_data
        self.__chunked_raw_art_data = chunked_raw_art_data
        if auto_generate_data:
            if art_text_string:
                self.generate_raw_art_data()
                self.generate_chunked_raw_art_data()
            elif raw_art_data:
                raise Exception("Not implemented.")
            elif chunked_raw_art_data:
                raise Exception("Not implemented.")
            else:
                raise Exception("Can't generate data without any given data.")

    def generate_raw_art_data(self) -> list[int]:
        compressed_data_from_string = base64.b64decode(self.__art_text_string)
        data = lzma.decompress(compressed_data_from_string)
        length = len(data)
        if length != 1024:
            raise ValueError(f"Data length mismatch ({length} != 1024)")
        self.__raw_art_data = list(data)
        return self.__raw_art_data

    def generate_chunked_raw_art_data(self) -> list[list[int]]:
        self.__chunked_raw_art_data = [
            self.__raw_art_data[x : x + 32]
            for x in range(0, len(self.__raw_art_data), 32)
        ]
        return self.__chunked_raw_art_data

    def generate_art_text_string(self) -> str:
        compressed = lzma.compress(bytes(self.__raw_art_data), format=lzma.FORMAT_ALONE)
        compressed = (
            compressed[:5]
            + len(self.__raw_art_data).to_bytes(8, "little")
            + compressed[13:]
        )
        self.__art_text_string = base64.b64encode(compressed).decode("ascii")
        return self.__art_text_string

    def generate_art_image_32x32(self, scale: int = 1) -> Image:
        image = Image.new("RGB", self.__art_size)
        image.putdata([RGB_COLOURS[colour] for colour in self.__raw_art_data])
        if scale > 1:
            image = image.resize(
                (self.__art_size[0] * scale, self.__art_size[1] * scale), resample=Image.BOX
            )
        return image

    def __str__(self) -> str:
        pretty_string = ""
        chunks = self.__chunked_raw_art_data
        chunks.reverse()
        for row in chunks:
            for px in row:
                pretty_string += (f"{px:2d}" if px > 0 else "  ") + " "
            pretty_string += "\n"
        return pretty_string


# hex_colours = [
#     '#20222E','#750DA1','#E3457E','#ECAE4C','#86A944','#417D7D','#4352A4','#532E7B','#FEFEFC','#C47EF5','#EC80CB','#FEF670','#C2FB90','#ADF7D6','#97CCF8','#A57EF7'
# ]
# rgb_colours = [tuple(int(h[i+1:i+3], 16) for i in (0, 2, 4)) for h in hex_colours]


RGB_COLOURS = [
    (32, 34, 46),
    (117, 13, 161),
    (227, 69, 126),
    (236, 174, 76),
    (134, 169, 68),
    (65, 125, 125),
    (67, 82, 164),
    (83, 46, 123),
    (254, 254, 252),
    (196, 126, 245),
    (236, 128, 203),
    (254, 246, 112),
    (194, 251, 144),
    (173, 247, 214),
    (151, 204, 248),
    (165, 126, 247),
]


if __name__ == "__main__":
    main()
