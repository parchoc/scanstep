from PySide6.QtGui import QResizeEvent, QTransform
from PySide6.QtWidgets import QGraphicsView


class InteractiveView(QGraphicsView):
    """QGraphicsView subclass, which allows automatic scaling on resize."""

    SCALE_MODIFIER: float = .01  # modifier to avoid scrolls

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.scaleScene()
        event.accept()

    def scaleScene(self) -> None:
        """
        Scale the scene so that the entire scene is displayed.

        Keep ratio between scene width and height.
        """
        if self.scene():
            scale = min(self.width() / self.scene().width(),
                        self.height() / self.scene().height())
            scale -= scale * self.SCALE_MODIFIER
            transform = QTransform.fromScale(scale, scale)
            self.setTransform(transform)
