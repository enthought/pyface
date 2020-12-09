from pyface.api import GUI
from pyface.tasks.action.api import (
    MenuBarSchema, MenuSchema, TaskAction, ToolBarSchema,
)
from pyface.tasks.api import Task, TaskWindow, EditorAreaPane
from traits.api import Str


class BlankTask(Task):

    # The task's identifier.
    id = Str("example.blank_task")

    # The task's user-visible name.
    name = Str("Blank")

    def create_central_pane(self):
        """ Create and return the central pane. """
        self.editor_area = EditorAreaPane()
        return self.editor_area

    def exit(self):
        self.window.destroy()

    def _menu_bar_default(self):
        return MenuBarSchema(
            MenuSchema(
                MenuSchema(
                    id="open_database",
                    name="&Open Database",
                ),
                TaskAction(
                    id="close_application",
                    name="&Close application",
                    method="exit",
                ),
                id="file",
                name="&File",
            ),
            MenuSchema(
                id="view",
                name="&View",
            ),
        )

    def _tool_bars_default(self):
        return [
            ToolBarSchema(
                MenuSchema(
                    id="do_something",
                    name="&Do something",
                ),
            )
        ]


def main():
    gui = GUI()

    task = BlankTask()
    window = TaskWindow(size=(800, 600))
    window.add_task(task)

    window.open()
    gui.start_event_loop()


if __name__ == "__main__":
    main()
