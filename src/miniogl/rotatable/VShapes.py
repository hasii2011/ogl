"""
This is a suite of small classes used to draw RotatableShapes.
Each one represent a simple shape (line, rectangle, circle, ellipse...)
or abstract command (color change).
"""
from abc import ABC
from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass

from wx import DC


@dataclass(kw_only=True)
class VShapePosition:
    x: int = 0
    y: int = 0


@dataclass(kw_only=True)
class VShapeSize:
    width:  int = 99
    height: int = 49

@dataclass
class VBasicDetails(VShapePosition, VShapeSize):
    pass


@dataclass
class VRectangleDetails( VBasicDetails):
    pass


@dataclass
class VEllipseDetails(VBasicDetails):
    pass


@dataclass
class ShapeData:
    start:  int = 0
    end:    int = 0
    radius: int = 0


class VShape(ABC):
    """
    Base VShape class.

    """
    def __init__(self):
        self._data: ShapeData = ShapeData()

    @classmethod
    def convert(cls, angle, x, y):
        T = [
            [1, 0, 0, 1], [0, -1, 1, 0], [-1, 0, 0, -1], [0, 1, -1, 0]
        ]
        nx = T[angle][0] * x + T[angle][1] * y
        ny = T[angle][2] * x + T[angle][3] * y
        return nx, ny

    @abstractmethod
    def SetAngle(self, angle):
        pass

    def Scale(self, factor, data):
        return map(lambda x: x * factor, data)


class VBasicShape(VShape, ABC):
    def __init__(self, vBasicDetails: VBasicDetails):
        super().__init__()

        self._vBasicDetails: vBasicDetails = vBasicDetails

    def scale(self, factor: int) -> VBasicDetails:

        if factor == 1:
            x: int = self._vBasicDetails.x
            y: int = self._vBasicDetails.y
            w: int = self._vBasicDetails.width
            h: int = self._vBasicDetails.height
        else:
            x: int = self._vBasicDetails.x * factor
            y: int = self._vBasicDetails.y * factor
            w: int = self._vBasicDetails.width  * factor
            h: int = self._vBasicDetails.height * factor

        return VBasicDetails(x=x, y=y, width=w, height=h)


class VRectangle(VBasicShape):
    def __init__(self, vRectangleDetails: VRectangleDetails):
        """

        Args:
            vRectangleDetails
        """
        super().__init__(vBasicDetails=vRectangleDetails)

    def SetAngle(self, angle):
        x: int = self._vBasicDetails.x
        y: int = self._vBasicDetails.y
        w: int = self._vBasicDetails.width
        h: int = self._vBasicDetails.height

        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        self._vBasicDetails = VRectangleDetails(x=x, y=y, width=w, height=h)

    def Draw(self, dc: DC, ox, oy, scale):

        scaledDetails: VBasicDetails = self.scale(scale)
        dc.DrawRectangle(ox + scaledDetails.x, oy + scaledDetails.y, scaledDetails.width, scaledDetails.height)


class VEllipse(VBasicShape):
    def __init__(self, vEllipseDetails: VEllipseDetails):
        super().__init__(vBasicDetails=vEllipseDetails)

    def SetAngle(self, angle):
        x: int = self._vBasicDetails.x
        y: int = self._vBasicDetails.y
        w: int = self._vBasicDetails.width
        h: int = self._vBasicDetails.height

        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        self._vBasicDetails = VRectangleDetails(x=x, y=y, width=w, height=h)

    def Draw(self, dc, ox, oy, scale):

        scaledDetails: VBasicDetails = self.scale(scale)
        dc.DrawEllipse(ox + scaledDetails.x, oy + scaledDetails.y, scaledDetails.width, scaledDetails.height)


class VCircle(VShape):
    def __init__(self, x, y, r):
        super().__init__()
        self._data = ShapeData(x=x, y=y, radius=r)

    def SetAngle(self, angle):
        x, y, r = self._data
        x, y = self.convert(angle, x, y)
        self._data = (x, y, r)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, r = self._data
        else:
            x, y, r = self.Scale(scale, self._data)
        dc.DrawCircle(ox + x, oy + y, r)


class VArc(VShape):
    def __init__(self, x1, y1, x2, y2, xc, yc):
        super().__init__()
        self._data = (x1, y1, x2, y2, xc, yc)

    def SetAngle(self, angle):
        x1, y1, x2, y2, xc, yc = self._data
        x1, y1 = self.convert(angle, x1, y1)
        x2, y2 = self.convert(angle, x2, y2)
        xc, yc = self.convert(angle, xc, yc)
        self._data = (x1, y1, x2, y2, xc, yc)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x1, y1, x2, y2, xc, yc = self._data
        else:
            x1, y1, x2, y2, xc, yc = self.Scale(scale, self._data)
        dc.DrawArc(ox + x1, oy + y1, ox + x2, oy + y2, ox + xc, oy + yc)


class VEllipticArc(VShape):
    def __init__(self, x: int, y: int, w: int, h: int, start: int, end: int):
        super().__init__()
        self._data = ShapeData(x=x, y=y, width=w, height=h, start=start, end=end)

    def SetAngle(self, angle):
        x, y, w, h, start, end  = self._data
        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        start -= angle * 90
        end -= angle * 90
        self._data = (x, y, w, h, start, end)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h, start, end  = self._data
        else:
            x, y, w, h = self.Scale(scale, self._data[0:4])
            start, end = self._data[4:]
        dc.DrawEllipticArc(ox + x, oy + y, w, h, start, end)


class VLineLength(VShape):
    def __init__(self, x, y, w, h):
        super().__init__()
        self._data = ShapeData(x, y, w, h)

    def SetAngle(self, angle):
        x, y, w, h = self._data
        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        self._data = (x, y, w, h)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h = self._data
        else:
            x, y, w, h = self.Scale(scale, self._data)
        x, y = ox + x, oy + y
        dc.DrawLine(x, y, x + w, y + h)


class VLineDest(VShape):
    def __init__(self, sx, sy, dx, dy):
        super().__init__()
        self._data = (sx, sy, dx, dy)

    def SetAngle(self, angle):
        sx, sy, dx, dy = self._data
        sx, sy = self.convert(angle, sx, sy)
        dx, dy = self.convert(angle, dx, dy)
        self._data = (sx, sy, dx, dy)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            sx, sy, dx, dy = self._data
        else:
            sx, sy, dx, dy = self.Scale(scale, self._data)
        dc.DrawLine(ox + sx, oy + sy, ox + dx, oy + dy)


class VPolygon(VShape):
    def __init__(self, points):
        super().__init__()
        self._data = points

    def SetAngle(self, angle):
        new = []
        for x, y in self._data:
            x, y = self.convert(angle, x, y)
            new.append((x, y))
        self._data = tuple(new)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            points = self._data
        else:
            points = []
            for x, y in self._data:
                points.append(tuple(self.Scale(scale, (x, y))))
        dc.DrawPolygon(points, ox, oy)


class VPen(VShape):
    def __init__(self, pen):
        super().__init__()
        self._pen = pen

    def SetAngle(self, angle):
        pass

    # noinspection PyUnusedLocal
    def Draw(self, dc, x, y, scale=1):
        dc.SetPen(self._pen)


class VBrush(VShape):
    def __init__(self, brush):
        super().__init__()
        self._brush = brush

    def SetAngle(self, angle):
        pass

    # noinspection PyUnusedLocal
    def Draw(self, dc, x, y, scale=1):
        dc.SetBrush(self._brush)
