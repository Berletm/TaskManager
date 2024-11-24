import PIL.Image
import ctypes
from rbt import RBTree
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

SCALE = 2.

ctk.set_appearance_mode("light")
ctk.set_widget_scaling(SCALE)
ctk.set_window_scaling(SCALE)

myappid = "mycompany.myproduct.subproduct.version"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Button(ctk.CTkButton):
    def __init__(self, master, text):
        super().__init__(master=master, text=text, font=("Open Sans", 14), corner_radius=0)
        if ctk.get_appearance_mode() == "Dark":
            self.configure(fg_color="#343638")
        else:
            self.configure(fg_color="#F9F9FA")


class AddButton(Button):
    def __init__(self, master):
        super(AddButton, self).__init__(master=master, text="")
        self.img = PIL.Image.open("../icons/plus.png").convert("RGBA")
        self.ico = ctk.CTkImage(self.img)
        self.configure(command=self.add_task_action, image=self.ico, width=10, height=10)
        self.parent = master

    def add_task_action(self):
        priority = self.parent.priority_entry.get()
        description = self.parent.description_entry.get()

        if not priority:
            self.parent.priority_entry.configure(placeholder_text=self.parent.priority_entry.error_output)
            return
        if not description:
            self.parent.description_entry.configure(placeholder_text=self.parent.description_entry.invalid_input)
            return

        self.parent.priority_entry.delete(0, ctk.END)
        self.parent.description_entry.delete(0, ctk.END)

        collision_check = self.parent.parent.parent.data.search(int(priority))

        if collision_check == RBTree.TNULL:
            self.parent.parent.parent.data.insert(int(priority), description)
            self.parent.description_entry.configure(placeholder_text=self.parent.description_entry.add_success)
        else:
            collision_check.task = description
            self.parent.description_entry.configure(placeholder_text=self.parent.description_entry.change_success)


class DeleteButton(Button):
    def __init__(self, master):
        super(DeleteButton, self).__init__(master=master, text="")
        self.img = PIL.Image.open("../icons/minus.png").convert("RGBA")
        self.ico = ctk.CTkImage(self.img)
        self.configure(command=self.delete_task_action, image=self.ico, width=10, height=10)
        self.parent = master

    def delete_task_action(self):
        if self.parent.description_entry.get():
            self.parent.description_entry.delete(0, ctk.END)

        priority = self.parent.priority_entry.get()

        if not priority:
            return

        res = self.parent.parent.parent.data.search(int(priority))

        if res == RBTree.TNULL:
            self.parent.description_entry.configure(placeholder_text=self.parent.description_entry.error_output)
            return

        self.parent.parent.parent.data.delete(int(priority))
        self.parent.description_entry.configure(placeholder_text=self.parent.description_entry.delete_success)


class FindButton(Button):
    def __init__(self, master):
        super(FindButton, self).__init__(master=master, text="")
        self.img = PIL.Image.open("../icons/find.png").convert("RGBA")
        self.ico = ctk.CTkImage(self.img)
        self.configure(command=self.find_task_action, image=self.ico, width=10, height=10)
        self.parent = master

    def find_task_action(self):
        priority = self.parent.priority_entry.get()

        if not priority:
            return

        self.parent.description_entry.delete(0, ctk.END)

        res = self.parent.parent.parent.data.search(int(priority))
        if res != RBTree.TNULL:
            self.parent.description_entry.insert(0, res)
        else:
            self.parent.description_entry.configure(placeholder_text=self.parent.description_entry.error_output)


class UpdateButton(Button):
    def __init__(self, master):
        super(UpdateButton, self).__init__(master=master, text="")
        self.img = PIL.Image.open("../icons/update.png").convert("RGBA")
        self.ico = ctk.CTkImage(self.img)
        self.configure(command=self.update_button_action, image=self.ico, width=10, height=10)
        self.parent = master

    def update_button_action(self):
        self.parent.parent.display_tree.draw_graph()
        self.parent.priority_entry.configure(placeholder_text=self.parent.priority_entry.placeholder_text)
        self.parent.description_entry.configure(placeholder_text=self.parent.description_entry.placeholder_text)


class PriorityEntry(ctk.CTkEntry):
    def __init__(self, master):
        super(PriorityEntry, self).__init__(master)

        self.error_output = "Invalid"
        self.placeholder_text = "priority"
        self.configure(placeholder_text=self.placeholder_text, width=55, height=26, corner_radius=0, border_width=0,
                       validate="key", validatecommand=(self.register(self.input_validation), '%S'))

    def input_validation(self, char):
        return True if (char == self.placeholder_text or char == self.error_output) else (char.isdigit() or char == "")


class DescriptionEntry(ctk.CTkEntry):
    def __init__(self, master):
        super(DescriptionEntry, self).__init__(master)
        self.placeholder_text = "description"
        self.error_output = "Task not found"
        self.invalid_input = "Invalid input"
        self.add_success = "Successfully added"
        self.change_success = "Successfully changed"
        self.delete_success = "Successfully deleted"
        self.configure(placeholder_text=self.placeholder_text, height=26, corner_radius=0, border_width=0)

    def input_validate(self, char):
        return True if (char == self.placeholder_text) else char == ""


class ToolBar(ctk.CTkFrame):
    def __init__(self, master):
        self.parent = master
        super(ToolBar, self).__init__(master)

        self.add_button = AddButton(self)
        self.add_button.pack(side="left")

        self.delete_button = DeleteButton(self)
        self.delete_button.pack(side="left")

        self.find_button = FindButton(self)
        self.find_button.pack(side="left")

        self.priority_entry = PriorityEntry(self)
        self.priority_entry.pack(side="left")

        self.description_entry = DescriptionEntry(self)
        self.description_entry.pack(side="left")

        self.update_button = UpdateButton(self)
        self.update_button.pack(side="left")


class DisplayTree(ctk.CTkFrame):
    def __init__(self, master):
        super(DisplayTree, self).__init__(master)
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

        self.ax.axis("off")

        self.parent = master
        self.graph = nx.Graph()
        self.coords = {}
        self.labels = {}

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    def RBT_to_graph(self, node, pos_x, pos_y, level=0, x_offset=2):
        if node == RBTree.TNULL:
            return
        self.graph.add_node(node.value, color=node.color)
        self.coords[node.value] = (pos_x, pos_y)
        self.labels[node.value] = node.task

        if node.left != RBTree.TNULL:
            self.graph.add_edge(node.value, node.left.value)
            self.RBT_to_graph(node.left, pos_x - x_offset, pos_y - 1, level + 1, x_offset / 2)
        if node.right != RBTree.TNULL:
            self.graph.add_edge(node.value, node.right.value)
            self.RBT_to_graph(node.right, pos_x + x_offset, pos_y - 1, level + 1, x_offset / 2)

    def draw_graph(self):
        self.graph.clear()
        self.ax.clear()
        self.coords = {}
        self.labels = {}
        self.RBT_to_graph(self.parent.parent.data.root, 0, 0)

        colors = [nx.get_node_attributes(self.graph, 'color').get(node) for node in self.graph.nodes()]
        nx.draw(self.graph, self.coords, with_labels=True, labels=self.labels, node_size=1000, node_color=colors,
                font_size=10, font_color="gray", font_weight="bold", edge_color='gray', ax=self.ax)
        self.canvas.draw()


class MainMenu(ctk.CTkFrame):
    def __init__(self, master):
        self.parent = master
        super().__init__(master=master)

        self.tool_bar = ToolBar(self)
        self.tool_bar.pack(fill="x", side="top")

        self.display_tree = DisplayTree(self)
        self.display_tree.pack(fill="both")


class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super(TaskManagerApp, self).__init__()

        self.title("Task Manager")
        self.resizable(False, False)
        self.iconbitmap("icons/icon1.ico")

        self.data = RBTree()

        self.menu = MainMenu(self)
        self.menu.pack(padx=0, pady=0)


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
