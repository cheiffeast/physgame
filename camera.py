import pymunk.shapes as pms


class Camera():
    def __init__(self, scene, **kwargs):
        self.scene = scene

        self.zoom = kwargs.get("zoomFactor", 1)
        self.zoomAbout = self.scene.size
        self.offset = [0, 0]

    def processData(self):
        if self.zoom < 0.1:
            self.zoom = 0.1

        shapes = []
        for shape in self.scene.space.shapes:
            sType = type(shape)
            body = shape.body

            if sType == pms.Segment:
                start = self.applyAll(self.scene.listflipy(
                    body.position + shape.a.rotated(body.angle)))
                end = self.applyAll(self.scene.listflipy(
                    body.position + shape.b.rotated(body.angle)))

                shapes.append([sType, start, end, max(
                    [self.applyZoomRadius(shape.radius), 1])])

            if sType == pms.Circle:
                shapes.append([sType, self.applyAll(self.scene.listflipy(
                    body.position)), self.applyZoomRadius(shape.radius), body.angle])

            if sType == pms.Poly:
                v = []
                for vertex in shape.get_vertices():
                    pos = self.applyAll(self.scene.listflipy(
                        vertex.rotated(shape.body.angle) + shape.body.position))
                    v.append(pos)
                shapes.append([sType, v, shape.body])

        return shapes

    def calculateOffset(self):
        center = [(self.zoomAbout[0] / 2) * self.zoom,
                  (self.zoomAbout[1] / 2) * self.zoom]
        offset = [(self.zoomAbout[0] / 2) - center[0],
                  (self.zoomAbout[1] / 2) - center[1]]
        return offset

    def applyOffset(self, pos):
        return pos[0] + self.offset[0], pos[1] + self.offset[1]

    def applyZoom(self, pos):
        offset = self.calculateOffset()
        return (pos[0] * self.zoom) + offset[0], (pos[1] * self.zoom) + offset[1]

    def applyZoomRadius(self, radius):
        return radius * self.zoom

    def applyAll(self, pos):
        return self.applyOffset(self.applyZoom(pos))

    def trueMouse(self, pos):
        offset = self.calculateOffset()
        return [(1 / self.zoom) * (pos[0] - offset[0] - self.offset[0]),
                (1 / self.zoom) * (pos[1] - offset[1] - self.offset[1])]
