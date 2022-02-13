from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QResizeEvent, QPaintEvent, QMouseEvent, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDesktopWidget, QPushButton, QGroupBox, QSlider
import sys
from colorsys import rgb_to_hsv, hsv_to_rgb


class MainWindow(QMainWindow):
    def __init__(self, size, parent=None):
        super().__init__(parent)

        self.setWindowTitle('NeuralGartic')
        self.setWindowIcon(QIcon("neuralGarticFull.png"))

        self.windowSize = size
        self.setFixedSize(size[0], size[1])
        self.center()

        self.init_image_widget()
        self.init_tools()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print('aaa')

    def center(self):
        rect = self.frameGeometry()
        rect_center = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(rect_center)
        self.move(rect.topLeft())

    def init_image_widget(self):
        img_size = (int(0.7 * self.windowSize[0]), int(self.windowSize[1]))
        img = ImageWidget(img_size, self)
        img.setGeometry(0, 0, img_size[0], img_size[1])

        self.drawing_widget = img

    def init_tools(self):
        self.tools = QGroupBox(self)
        self.tools.setGeometry(int(0.7 * self.windowSize[0]), 0, int(0.3 * self.windowSize[0]), self.windowSize[1])

        palette_pos = (int(0.73 * self.windowSize[0]), int(0.01 * self.windowSize[1]))
        palette_size = (int(0.25 * self.windowSize[0]), int(0.25 * self.windowSize[1]))

        self.color_palette_hs_widget = ColorPaletteHSWidget(palette_size, self)
        self.color_palette_hs_widget.setGeometry(palette_pos[0], palette_pos[1], palette_size[0], palette_size[1])
        self.color_palette_hs_widget.image_widget = self.drawing_widget

        self.color_palette_v_widget = ColorPaletteVWidget((palette_size[0], int(0.05 * self.windowSize[1])), self)
        self.color_palette_v_widget.setGeometry(palette_pos[0], palette_pos[1] + int(0.25 * self.windowSize[1]), palette_size[0], int(0.05 * self.windowSize[1]))
        self.color_palette_v_widget.paletteWidget = self.color_palette_hs_widget

        self.size_slider = QSlider(self)
        self.size_slider.setMinimum(2)
        self.size_slider.setMaximum(20)
        self.size_slider.setSingleStep(1)
        self.size_slider.setGeometry(int(0.73 * self.windowSize[0]), int(0.5 * self.windowSize[1]), int(0.25 * self.windowSize[0]), int(0.05 * self.windowSize[1]))
        self.size_slider.setOrientation(Qt.Horizontal)
        self.size_slider.valueChanged.connect(self.drawing_widget.size_changed)

        self.eraser = QPushButton(self)
        self.eraser.setGeometry(int(0.84 * self.windowSize[0]), int(0.75 * self.windowSize[1]), int(0.05 * self.windowSize[0]), int(0.04 * self.windowSize[1]))
        self.eraser.setText("Eraser")
        self.eraser.clicked.connect(self.drawing_widget.pick_eraser)

        self.clear_button = QPushButton(self)
        self.clear_button.setGeometry(int(0.84 * self.windowSize[0]), int(0.8 * self.windowSize[1]), int(0.05 * self.windowSize[0]), int(0.04 * self.windowSize[1]))
        self.clear_button.setText("Clear")
        self.clear_button.clicked.connect(self.drawing_widget.clear)

        self.save_button = QPushButton(self)
        self.save_button.setGeometry(int(0.84 * self.windowSize[0]), int(0.9 * self.windowSize[1]), int(0.1 * self.windowSize[0]), int(0.04 * self.windowSize[1]))
        self.save_button.setText("Save to png")
        self.save_button.clicked.connect(self.drawing_widget.save_img)


class ImageWidget(QWidget):
    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.image = QPixmap(size[0], size[1])
        self.image.fill(Qt.white)

        self.drawing = False
        self.lastPoint = None

        self.color = Qt.black
        self.radius = 2

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        painter = QPainter(self.image)
        if event.buttons() and Qt.LeftButton:
            if self.lastPoint is None:
                self.lastPoint = event.pos()
                return

            #painter = QPainter(self.image)
            painter.setPen(QPen(self.color, 1, Qt.SolidLine))
            painter.setBrush(QBrush(self.color, Qt.SolidPattern))

            x0 = self.lastPoint.x()
            y0 = self.lastPoint.y()

            x1 = event.pos().x()
            y1 = event.pos().y()

            x_diff = x1 - x0
            y_diff = y1 - y0

            if x_diff == 0:
                if y_diff > 0:
                    for j in range(y_diff + 1):
                        painter.drawEllipse(self.lastPoint.x(), self.lastPoint.y() + j, self.radius, self.radius)
                else:
                    for j in range(0, y_diff, -1):
                        painter.drawEllipse(self.lastPoint.x(), self.lastPoint.y() + j, self.radius, self.radius)
            elif y_diff == 0:
                if x_diff > 0:
                    for i in range(x_diff):
                        painter.drawEllipse(self.lastPoint.x() + i, self.lastPoint.y(), self.radius, self.radius)
                else:
                    for i in range(0, x_diff, -1):
                        painter.drawEllipse(self.lastPoint.x() + i, self.lastPoint.y(), self.radius, self.radius)
            else:
                a = y_diff / x_diff

                if abs(a) > 1:
                    if y1 < y0:
                        tmp = y1
                        y1 = y0
                        y0 = tmp

                        tmp = x1
                        x1 = x0
                        x0 = tmp

                    x = x0
                    for y in range(y0, y1 + 1, 1):
                        painter.drawEllipse(int(x), int(y), self.radius, self.radius)
                        x += 1 / a
                else:
                    if x1 < x0:
                        tmp = x1
                        x1 = x0
                        x0 = tmp

                        tmp = y1
                        y1 = y0
                        y0 = tmp

                    y = y0
                    for x in range(x0, x1 + 1, 1):
                        painter.drawEllipse(int(x), int(y), self.radius, self.radius)
                        y += a

            self.lastPoint = event.pos()
            self.update()
        else:
            pass
            #painter = QPainter(self)
            #imgCopy = self.image.copy()
            #painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
            #painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            #painter.drawEllipse(event.pos().x(), event.pos().y(), 5, 5)

            #self.update()

            #self.image.swap(imgCopy)
            #print('sss')

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def fill_with_color(self, color: QColor):
        self.image.fill(color)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def pick_eraser(self):
        self.color = Qt.white

    def size_changed(self, val):
        print(val)
        self.radius = val

    def save_img(self):
        self.image.save("NeuralGarticDrawing.png", "PNG")


class ColorPaletteHSWidget(QWidget):
    def __init__(self, palette_size, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.paletteSize = palette_size

        self.image_widget: ImageWidget = None
        self.last_mouse_pos = None

        self.v = 0.5

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)

        for i in range(self.paletteSize[0]):
            h = (i / self.paletteSize[0])
            for j in range(self.paletteSize[1]):
                s = ((self.paletteSize[1] - j) / self.paletteSize[1])
                color = hsv_to_rgb(h, s, self.v)
                painter.setPen(QColor(int(color[0] * 255.0), int(color[1] * 255.0), int(color[2] * 255.0)))

                painter.drawPoint(i, j)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        h = event.pos().x() / self.paletteSize[0]
        s = (self.paletteSize[1] - event.pos().y()) / self.paletteSize[1]

        color = hsv_to_rgb(h, s, self.v)
        self.image_widget.color = QColor(int(color[0] * 255.0), int(color[1] * 255.0), int(color[2] * 255.0))

        self.last_mouse_pos = event.pos()


class ColorPaletteVWidget(QWidget):
    def __init__(self, palette_size, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.paletteSize = palette_size

        self.paletteWidget: ColorPaletteHSWidget = None
        self.last_mouse_pos = None

        self.isPressed = False

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)

        for i in range(self.paletteSize[0]):
            v = i / self.paletteSize[0]
            for j in range(self.paletteSize[1]):
                color = hsv_to_rgb(0.0, 0.0, v)

                painter.setPen(QColor(int(color[0] * 255.0), int(color[1] * 255.0), int(color[2] * 255.0)))
                painter.drawPoint(i, j)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.paletteWidget.v = event.pos().x() / self.paletteSize[0]
        self.paletteWidget.update()
        self.last_mouse_pos = event.pos()

        self.isPressed = True

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() and Qt.LeftButton and self.isPressed:
            self.paletteWidget.v = event.pos().x() / self.paletteSize[0]
            self.paletteWidget.update()
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.isPressed = False

def main():
    app = QApplication(sys.argv)
    window = MainWindow((800, 600))
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
