from PyQt4 import QtGui, QtCore

class QProgressIndicator(QtGui.QWidget):
    def __init__(self, parent=None, color = None):
        QtGui.QWidget.__init__(self, parent)

        self.angle = 0
        self.timerId = -1
        self.delay = 80
        self.displayedWhenStopped = True
        self.color = self.palette().color(QtGui.QPalette.Text) if not color else QtGui.QColor(color)

    def isAnimated(self):
        return not self.timerId == -1

    def setDisplayedWhenStopped(self, state):
        self.displayedWhenStopped = state
        self.update()

    def isDisplayedWhenStopped(self):
        return self.displayedWhenStopped

    def startAnimation(self):
        self.angle = 0
        if self.timerId == -1:
            self.timerId = self.startTimer(self.delay)

    def stopAnimation(self):
        if not self.timerId == -1:
            self.killTimer(self.timerId)
        self.timerId = -1
        self.update()

    def setAnimationDelay(self, delay):
        if not self.timerId == -1:
            self.killTimer(self.timerId)
        self.delay = delay
        if self.timerId == -1:
            self.timerId = self.startTime(self.delay)

    def setColor(self, color):
        self.color = color
        self.update()

    def sizeHint(self):
        return QtCore.QSize(20,20)

    def heightForWidth(self, width):
        return width

    def timerEvent(self, event):
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        if not self.displayedWhenStopped and not self.isAnimated():
            return

        width = min(self.width(), self.height())

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        outerRadius = (width-1) * 0.5
        innerRadius = (width-1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth  = capsuleHeight * 0.23 if width > 32 else capsuleHeight * 0.35
        capsuleRadius = capsuleWidth / 2

        for i in range(12):
            color = QtGui.QColor(self.color)
            color.setAlphaF(float(1.0 - float(i / 12.0)))
            p.setPen(QtCore.Qt.NoPen)
            p.setBrush(color)
            p.save()
            p.translate(self.rect().center())
            p.rotate(self.angle - float(i * 30.0))
            p.drawRoundedRect(-capsuleWidth * 0.5,\
                              -(innerRadius + capsuleHeight),\
                              capsuleWidth,\
                              capsuleHeight,\
                              capsuleRadius,\
                              capsuleRadius)
            p.restore()
