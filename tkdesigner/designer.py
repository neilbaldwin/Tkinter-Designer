import tkdesigner.figma.endpoints as endpoints
from tkdesigner.figma.frame import Frame

from tkdesigner.template import GUI_TEMPLATE, APP_TEMPLATE
from jinja2 import Template

from pathlib import Path


GUI_FILE_NAME = "gui.py"
APP_FILE_NAME = "app.py"


class Designer:
    def __init__(self, token, file_key, output_path: Path):
        self.output_path = output_path
        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()

    def to_code(self) -> str:
        """Return main code.
        """
        window_data = self.file_data["document"]["children"][0]["children"][0]

        frame = Frame(window_data, self.figma_file, self.output_path)
        self.buttonCount = frame.buttonCount
        return frame.to_code(GUI_TEMPLATE)

    def design(self):
        """Write code and assets to the specified directories.
        """
        code = self.to_code()
        self.output_path.joinpath(GUI_FILE_NAME).write_text(code)

        """Write app.py code based on number of buttons
        """
        app_template = Template(APP_TEMPLATE)
        app_code = app_template.render(buttonCount = self.buttonCount)
        self.output_path.joinpath(APP_FILE_NAME).write_text(app_code)
