import pymunk.shapes as pms
from pymunk.vec2d import Vec2d


class Camera():
    def __init__(self, scene, **kwargs):
        self.scene = scene

        self.zoom = kwargs.get("zoomFactor", 1)
        self.zoomAbout = Vec2d(self.scene.size)
        self.offset = Vec2d([0, 0])

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

                shapes.append(["segment", start, end, max(
                    [self.applyZoomRadius(shape.radius), 1])])

            if sType == pms.Circle:
                shapes.append(["circle", self.applyAll(self.scene.listflipy(
                    body.position)), self.applyZoomRadius(shape.radius), body.angle])

            if sType == pms.Poly:
                v = []
                for vertex in shape.get_vertices():
                    pos = self.applyAll(self.scene.listflipy(
                        vertex.rotated(shape.body.angle) + shape.body.position))
                    v.append(pos)
                shapes.append(["polygon", v, shape.body])

        return shapes

    def calculateOffset(self):
        center = self.zoomAbout / 2 * self.zoom
        offset = self.zoomAbout / 2 - center
        return offset

    def applyOffset(self, pos):
        return Vec2d(pos) + self.offset

    def applyZoom(self, pos):
        offset = self.calculateOffset()
        return Vec2d(pos) * self.zoom + offset

    def applyZoomRadius(self, radius):
        return radius * self.zoom

    def applyAll(self, pos):
        return self.applyOffset(self.applyZoom(pos))

    def trueMouse(self, pos):
        offset = self.calculateOffset()
        return (1 / self.zoom) * (Vec2d(pos) - offset - self.offset)
