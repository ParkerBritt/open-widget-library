from qtpy.QtCore import Qt, QRect, QRectF, QPoint
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QMouseEvent
from qtpy.QtWidgets import QAbstractSlider, QApplication, QVBoxLayout, QWidget, QLabel
 
 
class Slider(QAbstractSlider):
    """A flat slider with a rounded-rect track and circular handle."""
 
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(parent)
        self.setOrientation(orientation)
        self.setRange(0, 100)
        self.setFocusPolicy(Qt.StrongFocus)
 
        # Geometry
        self._track_thickness = 6
        self._handle_radius = 9
 
        # Colors
        self._track_color = QColor("#151515")
        self._fill_color = QColor(220, 220, 220)
        self._handle_color = QColor(220, 220, 220)
        self._handle_border_color = QColor("#151515")
        self._handle_border_width = 2.0
 
        self._pressed = False
        self.setMinimumSize(self._handle_radius * 2, self._handle_radius * 2)
 
    def setTrackThickness(self, px: int):
        self._track_thickness = px
        self.update()
        return self
 
    def setHandleRadius(self, px: int):
        self._handle_radius = px
        self.setMinimumSize(px * 2, px * 2)
        self.update()
        return self
 
    def setTrackColor(self, color: QColor):
        self._track_color = QColor(color)
        self.update()
        return self
 
    def setFillColor(self, color: QColor):
        self._fill_color = QColor(color)
        self.update()
        return self
 
    def setHandleColor(self, color: QColor):
        self._handle_color = QColor(color)
        self.update()
        return self
 
    def setHandleBorderColor(self, color: QColor):
        self._handle_border_color = QColor(color)
        self.update()
        return self
 
    def setHandleBorderWidth(self, px: float):
        self._handle_border_width = px
        self.update()
        return self
 
    # -- Geometry helpers -------------------------------------
 
    def _is_horizontal(self) -> bool:
        return self.orientation() == Qt.Horizontal
 
    def _usable_span(self) -> float:
        """Pixel length available for the handle center to travel."""
        r = self._handle_radius
        return (self.width() if self._is_horizontal() else self.height()) - 2 * r
 
    def _ratio(self) -> float:
        """Current value mapped to 0.0–1.0."""
        span = self.maximum() - self.minimum()
        return (self.value() - self.minimum()) / span if span else 0.0
 
    def _handle_center(self) -> QPoint:
        r = self._handle_radius
        pos = r + self._ratio() * self._usable_span()
        if self._is_horizontal():
            return QPoint(int(pos), self.height() // 2)
        return QPoint(self.width() // 2, int(self.height() - pos))
 
    def _value_from_pos(self, pos: QPoint) -> int:
        r = self._handle_radius
        if self._is_horizontal():
            frac = (pos.x() - r) / max(self._usable_span(), 1)
        else:
            frac = (self.height() - pos.y() - r) / max(self._usable_span(), 1)
        frac = max(0.0, min(1.0, frac))
        return round(self.minimum() + frac * (self.maximum() - self.minimum()))
 
    # -- Painting -------------------------------------
 
    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
 
        horiz = self._is_horizontal()
        r = self._handle_radius
        t = self._track_thickness
        center = self._handle_center()
 
        # Track background
        if horiz:
            track = QRectF(r, (self.height() - t) / 2, self._usable_span(), t)
        else:
            track = QRectF((self.width() - t) / 2, r, t, self._usable_span())
        p.setPen(Qt.NoPen)
        p.setBrush(self._track_color)
        p.drawRoundedRect(track, t / 2, t / 2)
 
        # Filled portion
        if horiz:
            fill = QRectF(track.left(), track.top(), center.x() - track.left(), t)
        else:
            fill = QRectF(track.left(), center.y(), t, track.bottom() - center.y())
        p.setBrush(self._fill_color)
        p.drawRoundedRect(fill, t / 2, t / 2)
 
        # Handle
        p.setBrush(self._handle_color)
        p.setPen(QPen(self._handle_border_color, self._handle_border_width))
        p.drawEllipse(center, r, r)
 
        p.end()
 
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self.setSliderDown(True)
            self.setValue(self._value_from_pos(event.pos()))
 
    def mouseMoveEvent(self, event: QMouseEvent):
        if self._pressed:
            self.setValue(self._value_from_pos(event.pos()))
 
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._pressed = False
            self.setSliderDown(False)
 
    # -- Side hints -----------------------------
 
    def sizeHint(self):
        from qtpy.QtCore import QSize
 
        d = self._handle_radius * 2 + 2
        return QSize(200, d) if self._is_horizontal() else QSize(d, 200)
