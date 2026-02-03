from ui.step_template_ui import Ui_StepTemplate
from PySide6.QtWidgets import QWidget


class StepTemplate(QWidget, Ui_StepTemplate):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def loadStepLayout(self, step_index: int = 1):
        import importlib

        self.step_index = step_index

        step_module = importlib.import_module(f"steps.step{step_index}")
        step_class = getattr(step_module, "Step", None)

        if step_class:
            step_instance = step_class()
            self.stepTitleLabel.setText(f"Step {self.step_index}")
            self.stepSubtitleLabel.setText(step_instance.subtitle)
            self.stepFrame.setLayout(step_instance.layout())

        return self.layout()
