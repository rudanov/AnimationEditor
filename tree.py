import tkinter.ttk

import command


class ProjectHierarchyView(tkinter.ttk.Treeview):
    def __init__(self, command_list):
        tkinter.ttk.Treeview.__init__(self)
        self.__command_list = command_list
        self.__items = dict()
        self.bind("<1>", self.select_item)
        self.__default_item = None

    def on_model_changed(self, model):
        self.delete(*self.get_children())
        self.__items.clear()
        self.__default_item = model

        animations = self.insert("", "end", text="Animations", open=True)
        skeletons = self.insert("", "end", text="Skeletons", open=True)

        for i in range(model.number_of_animations):
            animation = self.insert(
                animations, "end",
                iid=model.get_animation(i).name,
                text=model.get_animation(i).name,
                open=True
            )

            if model.get_animation(i) == model.active_element:
                self.focus(animation)
                self.selection_set(animation)
            self.__items[animation] = model.get_animation(i)

            for j in range(model.get_animation(i).number_of_states):
                state = self.insert(
                    animation, "end",
                    iid="{}_state_{}".format(model.get_animation(i).name, j),
                    text="{}_state_{}".format(model.get_animation(i).name, j),
                    open=True,
                )
                if model.get_animation(i).get_state(j) == model.active_element:
                    self.focus(state)
                    self.selection_set(state)
                self.__items[state] = model.get_animation(i).get_state(j)

        for i in range(model.number_of_skeletons):
            skeleton = self.insert(
                skeletons, "end",
                iid=model.get_skeleton(i).name,
                text=model.get_skeleton(i).name,
                open=True
            )

            if model.get_skeleton(i) == model.active_element:
                self.focus(skeleton)
                self.selection_set(skeleton)
            self.__items[skeleton] = model.get_skeleton(i)

            for j in range(model.get_skeleton(i).number_of_bones):
                bone = self.insert(
                    skeleton, "end",
                    iid='{}_bone_{}'.format(model.get_skeleton(i).name, j),
                    text=model.get_skeleton(i).get_bone(j).name,
                    open=True,
                )
                if model.get_skeleton(i).get_bone(j) == model.active_element:
                    self.focus(bone)
                    self.selection_set(bone)
                self.__items[bone] = model.get_skeleton(i).get_bone(j)

    def select_item(self, event):
        iid = self.identify("item", event.x, event.y)
        self.__command_list.add_command(command.SelectCommand(self.__items.get(iid, self.__default_item)))
