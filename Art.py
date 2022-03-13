import base64
import lzma
from PIL import Image, ImageDraw


class Art:
    seen = False
    smoothing = False

    __art_size_32x32 = (32, 32)
    __art_size_60x24 = (60, 24)

    __art_text_string: str = None
    __raw_art_data: list[int] = None
    __chunked_raw_art_data: list[list[int]] = None

    __chunked_big_art: list[list[int]] = None
    __chunked_small_art: list[list[int]] = None

    def __init__(
        self,
        art_text_string: str = None,
        raw_art_data: list[int] = None,
        chunked_raw_art_data: list[list[int]] = None,
    ):
        self.__art_text_string = art_text_string
        self.__raw_art_data = raw_art_data
        self.__chunked_raw_art_data = chunked_raw_art_data
        if art_text_string:
            self.__generate_raw_art_data()
            self.__generate_chunked_raw_art_data()
        elif raw_art_data:
            self.__generate_art_text_string()
            self.__generate_chunked_raw_art_data()
        elif chunked_raw_art_data:
            raise Exception("Not implemented.")
        else:
            raise Exception("Can't generate data without any given data.")
        self.__split_chunked_data()

    def __generate_raw_art_data(self):
        compressed_data_from_string = base64.b64decode(self.__art_text_string)

        compressed_data_from_string = (
            compressed_data_from_string[:5]
            + bytes([255] * 8)
            + compressed_data_from_string[13:]
        )
        data = decompress_lzma(compressed_data_from_string)

        length = len(data)
        if length != 1024:
            data = data[:1024]
            # raise ValueError(f"Data length mismatch ({length} != 1024)")

        signature = bytes([15, 4, 0, 2, 4])
        signature_line = signature*6

        if signature in data[2:32]+data[32*6+2:32*6+2+len(signature_line)*2]:
            self.seen = True
        if data[0] == 1:
            self.smoothing = True

        data = data[:2] + signature_line + data[32:32*6+2] + signature_line*2 + data[32*6+2+len(signature_line)*2:]
        self.__raw_art_data = list(data)

    def __generate_chunked_raw_art_data(self):
        self.__chunked_raw_art_data = [
            self.__raw_art_data[x : x + 32]
            for x in range(0, len(self.__raw_art_data), 32)
        ]

    def __generate_art_text_string(self):
        compressed = lzma.compress(bytes(self.__raw_art_data), format=lzma.FORMAT_ALONE)
        compressed = (
            compressed[:5]
            + len(self.__raw_art_data).to_bytes(8, "little")
            + compressed[13:]
        )
        self.__art_text_string = base64.b64encode(compressed).decode("ascii")

    def __split_chunked_data(self):
        self.__generate_chunked_raw_art_data()
        self.__chunked_big_art = self.__chunked_raw_art_data[8:]
        self.__chunked_big_art.reverse()
        self.__chunked_small_art = [
            row[3:-1] for row in self.__chunked_raw_art_data[1:6]
        ]
        self.__chunked_small_art.reverse()

    def make_art_image_32x32(self, scale: int = 1) -> Image:
        size = self.__art_size_32x32
        image = Image.new("RGB", size)
        image.putdata([RGB_COLOURS[c_id] for c_id in self.__raw_art_data])
        if scale > 1:
            image = image.resize(
                (size[0] * scale, size[1] * scale),
                resample=Image.BOX,
            )
        return image

    def make_art_image_60x24(self, scale: int = 1) -> Image:
        size = self.__art_size_60x24
        image = Image.new("RGBA", size)

        big_part = []
        for row in self.__chunked_big_art:
            big_part += row + [-1] * 28
        image.putdata([RGB_COLOURS[c_id] for c_id in big_part])

        small_image = Image.new("RGBA", size)
        small_part = [-1] * 60 * 19
        for row in self.__chunked_small_art:
            small_part += [-1] * 32 + row
        small_image.putdata([RGB_COLOURS[c_id] for c_id in small_part])

        image.paste(small_image, (0, 0), small_image)

        if scale > 1:
            image = image.resize(
                (size[0] * scale, size[1] * scale),
                resample=Image.BOX,
            )
        return image

    def make_art_with_overlay(self) -> Image:
        engine_color_1 = RGB_COLOURS[self.__chunked_raw_art_data[3][1]]
        engine_color_2 = RGB_COLOURS[self.__chunked_raw_art_data[4][1]]

        image = Image.new("RGBA", (984, 837))
        draw = ImageDraw.Draw(image)
        draw.rectangle(((0, 0), (150, 837)), fill=engine_color_1)
        draw.rectangle(((200, 0), (330, 837)), fill=engine_color_2)

        art_image_60x24_s13 = self.make_art_image_60x24(13)
        image.paste(art_image_60x24_s13, (130, 205), art_image_60x24_s13)

        overlay = Image.open("./overlay.png")
        image.paste(overlay, (0, 0), overlay)

        return image

    def stringify(self) -> str:
        pretty_string = ""
        chunks = list(self.__chunked_raw_art_data)
        # chunks.reverse()
        for row in chunks:
            for px in row:
                pretty_string += (f"{px:2d}" if px > 0 else "  ") + " "
            pretty_string += "\n"
        return pretty_string

    def get_art_text_string(self) -> str:
        self.__generate_art_text_string()
        return self.__art_text_string

    __str__ = get_art_text_string


def decompress_lzma(data: bytes) -> bytes:
    results = []
    while True:
        decomp = lzma.LZMADecompressor(lzma.FORMAT_AUTO, None, None)
        try:
            res = decomp.decompress(data)
        except lzma.LZMAError:
            if results:
                break  # Leftover data is not a valid LZMA/XZ stream; ignore it.
            else:
                raise  # Error on the first iteration; bail out.
        results.append(res)
        data = decomp.unused_data
        if not data:
            break
        if not decomp.eof:
            raise lzma.LZMAError(
                "Compressed data ended before the end-of-stream marker was reached"
            )
    return b"".join(results)


# hex_colours = [
#     '#20222E','#750DA1','#E3457E','#ECAE4C','#86A944','#417D7D','#4352A4','#532E7B','#FEFEFC','#C47EF5','#EC80CB','#FEF670','#C2FB90','#ADF7D6','#97CCF8','#A57EF7'
# ]
# rgb_colours = [tuple(int(h[i+1:i+3], 16) for i in (0, 2, 4)) for h in hex_colours]


RGB_COLOURS = {
    -1: (0, 0, 0, 0),
    0: (32, 34, 46),
    1: (117, 13, 161),
    2: (227, 69, 126),
    3: (236, 174, 76),
    4: (134, 169, 68),
    5: (65, 125, 125),
    6: (67, 82, 164),
    7: (83, 46, 123),
    8: (254, 254, 252),
    9: (196, 126, 245),
    10: (236, 128, 203),
    11: (254, 246, 112),
    12: (194, 251, 144),
    13: (173, 247, 214),
    14: (151, 204, 248),
    15: (165, 126, 247),
}
