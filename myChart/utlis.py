colorPallete = ["#55efc4", "#81ecec", "#a29bfe",
                "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPallete[0], colorPallete[5]


def generate_color_palette(amount):
    palette = []
    i = 0
    while i < len(colorPallete) and len(palette) < amount:
        palette.append(colorPallete[i])
        i += 1
        if i == len(colorPallete) and len(palette) < amount:
            i = 0

    return palette
