from skimage import io
from pyxelate import Pyx, Pal

# load image with 'skimage.io.imread()'
image = io.imread("047_Kawaii_1.png")

my_pal = Pal.from_hex(['#20222E', '#750DA1', '#E3457E', '#ECAE4C', '#86A944', '#417D7D', '#4352A4', '#532E7B', '#FEFEFC', '#C47EF5', '#EC80CB', '#FEF670', '#C2FB90', '#ADF7D6', '#97CCF8', '#A57EF7'])

# 1) Instantiate Pyx transformer
pyx = Pyx(height=24, width=32, palette=my_pal, dither="none")

# 2) fit an image, allow Pyxelate to learn the color palette
pyx.fit(image)

# 3) transform image to pixel art using the learned color palette
new_image = pyx.transform(image)

# save new image with 'skimage.io.imsave()'
io.imsave("pixel.png", new_image)
