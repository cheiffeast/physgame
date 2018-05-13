from pygame import draw

def simple(screen, shapes, color = [255, 255, 255]):
    for shape in shapes:
        if shape[0] == "segment":
            draw.line(screen, color, shape[1], shape[2], int(shape[3]))
        if shape[0] == "circle":
            draw.circle(screen, color, [int(shape[1][0]), int(shape[1][1])], int(shape[2]))
        if shape[0] == "polygon":
            draw.polygon(screen, color, shape[1])
