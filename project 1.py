# Project Entropy, done by Alireza Rashidi Laleh
# one of the river crossing puzzles solved by depth-limited search algorithm
# python 3.7.8


import numpy as np
import itertools
from tkinter import *
from tkinter import font
import threading


class River:
    def __init__(self):
        # variables used regarding the puzzle itself.
        self.names = {0: 'Father', 1: 'Mother', 2: 'Son #1', 3: 'Son #2', 4: 'Daughter #1', 5: 'Daughter #2', 6: 'Police', 7: 'Thief', 8: 'Boat'}
        self.indices = {value: key for key, value in self.names.items()}
        self.right_side = []
        self.left_side = []
        self.conflict = False

        # variables used regarding DLS.
        self.root_node = [0] * 9
        self.limit = 0
        self.key = 1
        self.nodes = {1: [[0, 0, 0, 0, 0, 0, 0, 0, 0]]}
        self.path = []
        self.won = False
        self.trigger = False
        for i in range(2, self.limit + 1):
            self.nodes[i] = []

        # variables used in our GUI.
        self.show_right_side = {}
        self.show_left_side = {}
        self.finished = False
        self.show_index = 1


    def handler_dls(self):
        '''
        our main method, does depth-limited search on the river-crossing puzzle.
        '''

        self.trigger = False
        while self.won == False:
            if self.key < self.limit:
                if self.nodes[self.key] == []:
                    if self.key == 1:
                        self.won = False
                        break
                    else:
                        self.trigger = True
                        self.key -= 1
                        continue

                if self.trigger == False:
                    self.root_node = self.nodes[self.key][0]
                    if self.is_valid() == False:
                        del self.nodes[self.key][0]
                        continue

                    #del self.nodes[self.key][0]
                    self.path.append(self.root_node)
                    if self.is_goal():
                        self.won = True
                        break

                    self.key += 1
                    self.generate_states()
                    self.trigger = False
                else:
                    del self.nodes[self.key][0]
                    self.trigger = False
                    self.path.pop()
                    continue

            if self.key == self.limit:
                while self.nodes[self.key] != []:
                    self.root_node = self.nodes[self.key][0]
                    if self.is_valid() == False:
                        del self.nodes[self.key][0]
                        continue

                    if self.is_goal():
                        self.path.append(self.root_node)
                        self.won = True

                    del self.nodes[self.key][0]

                if self.nodes[self.key] == []:
                    self.trigger = True

                self.key -= 1

        self.finished = True


    def generate_states(self):
        '''
        generates children of a given node. returns nothing. every child is saved in nodes.
        '''

        records = []
        new_nodes = []
        existing_nodes = []
        try:
            existing_nodes = self.nodes[self.key]
        except KeyError:
            pass

        self.nodes[self.key] = []
        temp = self.root_node.copy()
        for i in [0, 1, 6]:
            for j in range(0, len(self.root_node) - 1):
                if not i == j:
                    self.root_node = temp.copy()
                    if self.root_node[i] == 1:
                        if self.root_node[j] == 1:
                            if self.root_node[-1] == 1:
                                self.root_node[j] = 0
                                self.root_node[i] = 0
                                self.root_node[-1] = 0
                                records.append(self.root_node)

                    self.root_node = temp.copy()
                    if self.root_node[i] == 0:
                        if self.root_node[j] == 0:
                            if self.root_node[-1] == 0:
                                self.root_node[j] = 1
                                self.root_node[i] = 1
                                self.root_node[-1] = 1
                                records.append(self.root_node)

        for i in [0, 1, 6]:
            self.root_node = temp.copy()
            if self.root_node[i] == 1:
                if self.root_node[-1] == 1:
                    self.root_node[i] = 0
                    self.root_node[-1] = 0
                    records.append(self.root_node)

        for i in [0, 1, 6]:
            self.root_node = temp.copy()
            if self.root_node[i] == 0:
                if self.root_node[-1] == 0:
                    self.root_node[i] = 1
                    self.root_node[-1] = 1
                    records.append(self.root_node)

        for item in records:
            self.root_node = item.copy()
            self.is_valid()
            if self.conflict == False:
                new_nodes.append(self.root_node)

        self.root_node = temp.copy()

        for item in reversed(new_nodes):
            if not item == self.root_node:
                existing_nodes.insert(0, item)

        existing_nodes = list(k for k,_ in itertools.groupby(existing_nodes))
        self.nodes[self.key] = existing_nodes


    def is_goal(self):
        '''
        checks whether a state is the goal or not. returns either true or false...
        '''

        if self.root_node == [1] * 9:
            return True
        else:
            return False


    def is_valid(self):
        '''
        checks whether the state to be assigned has any conflict or not. returns nothing.
        '''

        self.conflict = False

        while True:
            if not self.root_node[self.indices['Police']] == self.root_node[self.indices['Thief']]:
                value = self.root_node[self.indices['Thief']]
                for i in [0, 1, 2, 3, 4, 5, 6]:
                    if value == self.root_node[i]:
                        self.conflict = True

            if self.root_node[self.indices['Son #1']] == self.root_node[self.indices['Mother']] != self.root_node[self.indices['Father']]:
                self.conflict = True

            if self.root_node[self.indices['Son #2']] == self.root_node[self.indices['Mother']] != self.root_node[self.indices['Father']]:
                self.conflict = True

            if self.root_node[self.indices['Daughter #1']] == self.root_node[self.indices['Father']] != self.root_node[self.indices['Mother']]:
                self.conflict = True

            if self.root_node[self.indices['Daughter #2']] == self.root_node[self.indices['Father']] != self.root_node[self.indices['Mother']]:
                self.conflict = True

            break

        if self.conflict == True:
            return False
        else:
            return True


    def path_show(self):
        '''
        if our main method, "handler_dls", found the goal state, it calls this method to process the path of sequences
        (or states or nodes) led to the goal state. returns nothing.
        '''

        num = 1
        for item in self.path:
            self.right_side = []
            self.left_side = []
            for i in range(0, 9):
                if item[i] == 0:
                    self.right_side.append(self.names[i])
                else:
                    self.left_side.append(self.names[i])

            self.show_right_side[num] = self.right_side
            self.show_left_side[num] = self.left_side
            num += 1


    def show_search(self, root, limit=None):
        '''
        our loading screen while the search is being done. but it doesn't work for now. maybe threads??
        '''

        root.destroy()

        if not limit == None:
            try:
                self.limit = int(limit)
            except ValueError:
                self.show_program()

        root = Tk()

        root.title('Searching')
        root.geometry('640x450')
        root.resizable(0, 0)

        text = Label(root, text='Please wait while the search is done.')
        text.config(font=('@Malgun Gothic', 16))
        text.place(x=320, y=100, anchor=CENTER)

        button = Button(root, height=25, width=25, text='Try Again', font=('Calibri 18'))
        button.place(x=200, y=250, width=150, height=100, anchor=CENTER)
        button['command'] = lambda button=button: self.show_program(root)

        button = Button(root, height=25, width=25, text='Quit', font=('Calibri 18'), command=root.destroy)
        button.place(x=400, y=250, width=150, height=100, anchor=CENTER)

        #root.update()
        #threading.Thread(target=self.handler_dls).start()
        self.handler_dls()

        if self.finished == True:
            if self.won == True:
                self.show_results(root)
            else:
                self.show_failure(root)

        root.mainloop()


    def show_results(self, root):
        '''
        it shows (in a "graphical" way) the states which were in the path which led to the goal state.
        '''

        root.destroy()
        self.path_show()

        root = Tk()

        def xasthur(forward):
            if forward == True:
                if self.show_index == len(self.path):
                    pass
                elif self.show_index < len(self.path):
                    for widget in frame.winfo_children():
                        if widget.winfo_name() != canvas.winfo_name():
                            widget.destroy()

                    self.show_index += 1
                    index_label.configure(text=f'{self.show_index} out of {len(self.path)}')
                    if self.show_left_side[self.show_index] == []:
                        pass
                    else:
                        initial_size = 0
                        for item in self.show_left_side[self.show_index]:
                            text = Label(frame, text=item)
                            text.config(font=('@Malgun Gothic', 22))
                            text.place(x=100, y=150+initial_size, anchor=CENTER)
                            initial_size += 60

                    if self.show_right_side[self.show_index] == []:
                        pass
                    else:
                        initial_size = 0
                        for item in self.show_right_side[self.show_index]:
                            text = Label(frame, text=item)
                            text.config(font=('@Malgun Gothic', 22))
                            text.place(x=880, y=150+initial_size, anchor=CENTER)
                            initial_size += 60
            else:
                if self.show_index == 1:
                    pass
                elif self.show_index > 1:
                    for widget in frame.winfo_children():
                        if widget.winfo_name() != canvas.winfo_name():
                            widget.destroy()

                    self.show_index -= 1
                    index_label.configure(text=f'{self.show_index} out of {len(self.path)}')
                    if self.show_left_side[self.show_index] == []:
                        pass
                    else:
                        initial_size = 0
                        for item in self.show_left_side[self.show_index]:
                            text = Label(frame, text=item)
                            text.config(font=('@Malgun Gothic', 22))
                            text.place(x=100, y=150+initial_size, anchor=CENTER)
                            initial_size += 60

                    if self.show_right_side[self.show_index] == []:
                        pass
                    else:
                        initial_size = 0
                        for item in self.show_right_side[self.show_index]:
                            text = Label(frame, text=item)
                            text.config(font=('@Malgun Gothic', 22))
                            text.place(x=880, y=150+initial_size, anchor=CENTER)
                            initial_size += 60


        root.title('Results')
        root.geometry('1280x900')
        root.resizable(0, 0)

        frame = Frame(root, width=1280, height=700)
        frame.pack()

        canvas = Canvas(frame, width=1280, height=700)
        canvas.pack()

        text = Label(root, text='Left side')
        text.config(font=('@Malgun Gothic', 36))
        text.place(x=270, y=50, anchor=CENTER)

        text = Label(root, text='Right side')
        text.config(font=('@Malgun Gothic', 36))
        text.place(x=1000, y=50, anchor=CENTER)

        initial_size = 0
        for item in self.show_right_side[self.show_index]:
            text = Label(frame, text=item)
            text.config(font=('@Malgun Gothic', 22))
            text.place(x=880, y=150+initial_size, anchor=CENTER)
            initial_size += 60

        if self.show_left_side != []:
            initial_size = 0
            for item in self.show_left_side[self.show_index]:
                text = Label(frame, text=item)
                text.config(font=('@Malgun Gothic', 22))
                text.place(x=100, y=150+initial_size, anchor=CENTER)
                initial_size += 60

        canvas.create_line(640, 0, 640, 700, fill='blue', width=200)
        canvas.create_line(0, 700, 1280, 700, fill='black', width=10)

        index_label = Label(root, text=f'{self.show_index} out of {len(self.path)}')
        index_label.config(font=('@Malgun Gothic', 14))
        index_label.place(x=640, y=850, anchor=CENTER)

        button = Button(root, height=25, width=25, text='Next State', font=('Calibri 14'))
        button.place(x=700, y=800, width=150, height=50, anchor=CENTER)
        button['command'] = lambda button=button: xasthur(True) # forward == True

        button = Button(root, height=25, width=25, text='Previous State', font=('Calibri 14'))
        button.place(x=550, y=800, width=150, height=50, anchor=CENTER)
        button['command'] = lambda button=button: xasthur(False) # forward == False

        button = Button(root, height=25, width=25, text='Try Again', font=('Calibri 18'))
        button.place(x=350, y=800, width=150, height=100, anchor=CENTER)
        button['command'] = lambda button=button: self.show_program(root)

        button = Button(root, height=25, width=25, text='Quit', font=('Calibri 18'), command=root.destroy)
        button.place(x=900, y=800, width=150, height=100, anchor=CENTER)

        root.mainloop()


    def show_failure(self, root):
        '''
        if the search wasn't successful, this method will be executed. it shows a window.
        '''

        root.destroy()

        root = Tk()

        root.title('No Results')
        root.geometry('640x450')
        root.resizable(0, 0)

        text = Label(root, text='Sorry... DLS couldn\'t find the solution within the given limit.')
        text.config(font=('@Malgun Gothic', 16))
        text.place(x=320, y=100, anchor=CENTER)

        text = Label(root, text='Do you wish to continue?')
        text.config(font=('@Malgun Gothic', 16))
        text.place(x=320, y=200, anchor=CENTER)

        button = Button(root, height=25, width=25, text='Try Again', font=('Calibri 18'))
        button.place(x=160, y=300, width=150, height=100, anchor=CENTER)
        button['command'] = lambda button=button: self.show_program(root)

        button = Button(root, height=25, width=25, text='Quit', font=('Calibri 18'), command=root.destroy)
        button.place(x=480, y=300, width=150, height=100, anchor=CENTER)

        root.mainloop()


    def custom_search_prep(self, root, *args):
        '''
        a supplementary method which preprocesses the input entry from show_custom_search method.
        '''

        list_args = list(args)
        root = root

        self.conflict = False
        self.limit = list_args[0]

        try:
            if self.limit == '':
                raise ValueError
            else:
                self.limit = int(list_args[0])
                del list_args[0]
                for i in range(0, len(list_args)):
                    if list_args[i] == '1' or list_args[i] == '0':
                        self.root_node[i] = int(list_args[i])
                        self.is_valid()
                        if self.conflict == False:
                            for i in range(1, self.limit + 1):
                                self.nodes[i] = []

                            self.nodes[1] = [self.root_node]
                        else:
                            raise Exception
                    else:
                        raise TypeError
        except (ValueError, TypeError):
            self.splash_screen(message='Your input was invalid. Please try again.')
            self.show_custom_search(root)
        except Exception:
            self.splash_screen(message='You didn\'t input a valid state. Please try again.')
            self.show_custom_search(root)

        self.show_search(root=root)


    def splash_screen(self, message):
        root = Tk()

        root.title('Important Message')
        root.geometry('640x450')
        root.resizable(0, 0)

        text = Label(root, text=message)
        text.config(font=('@Malgun Gothic', 14))
        text.place(x=320, y=225, anchor=CENTER)

        root.after(5000, root.destroy)



    def show_custom_search(self, root):
        '''
        the method for the users who want to enter their own initial root node in the tree, rather than letting the DLS start from
        the very first state.
        '''

        root.destroy()

        root = Tk()

        root.title('Custom Search')
        root.geometry('1280x900')
        root.resizable(0, 0)

        text = Label(root, text='Enter a number, whether 1 or 0, to determine the position of each person.\n1 means left side and 0 means right side.')
        text.config(font=('@Malgun Gothic', 24))
        text.place(x=640, y=100, anchor=CENTER)

        text = Label(root, text='Father:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=150, y=350, anchor=CENTER)

        entry_father = Entry(root, font=('Calibri 18'), justify='center')
        entry_father.place(x=250, y=350, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Mother:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=150, y=450, anchor=CENTER)

        entry_mother = Entry(root, font=('Calibri 18'), justify='center')
        entry_mother.place(x=250, y=450, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Son #1:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=150, y=550, anchor=CENTER)

        entry_son_one = Entry(root, font=('Calibri 18'), justify='center')
        entry_son_one.place(x=250, y=550, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Son #2:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=150, y=650, anchor=CENTER)

        entry_son_two = Entry(root, font=('Calibri 18'), justify='center')
        entry_son_two.place(x=250, y=650, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Daughter #1:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=150, y=750, anchor=CENTER)

        entry_daughter_one = Entry(root, font=('Calibri 18'), justify='center')
        entry_daughter_one.place(x=300, y=750, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Daughter #2:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=650, y=350, anchor=CENTER)

        entry_daughter_two = Entry(root, font=('Calibri 18'), justify='center')
        entry_daughter_two.place(x=800, y=350, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Police:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=650, y=450, anchor=CENTER)

        entry_police = Entry(root, font=('Calibri 18'), justify='center')
        entry_police.place(x=750, y=450, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Thief:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=650, y=550, anchor=CENTER)

        entry_thief = Entry(root, font=('Calibri 18'), justify='center')
        entry_thief.place(x=750, y=550, width=50, height=50, anchor=CENTER)

        text = Label(root, text='Boat:')
        text.config(font=('@Malgun Gothic', 22))
        text.place(x=650, y=650, anchor=CENTER)

        entry_boat = Entry(root, font=('Calibri 18'), justify='center')
        entry_boat.place(x=750, y=650, width=50, height=50, anchor=CENTER)

        label = Label(root, text='Please enter a number as depth or limit for our algorithm:\n(A number between preferably ONE and PLUS INFINITY)')
        label.config(font=('@Malgun Gothic', 14))
        label.place(x=640, y=750, anchor=CENTER)

        entry_limit = Entry(root, font=('Calibri 18'), justify='center')
        entry_limit.place(x=1000, y=750, width=150, height=50, anchor=CENTER)

        button = Button(root, height=25, width=25, text='Search', font=('Calibri 18'))
        button.place(x=1000, y=400, width=150, height=100, anchor=CENTER)
        button['command'] = lambda button=button: self.custom_search_prep(root, entry_limit.get(), entry_father.get(), entry_mother.get(), entry_son_one.get(), entry_son_two.get(), entry_daughter_one.get(), entry_daughter_two.get(), entry_police.get(), entry_thief.get(), entry_boat.get())

        button = Button(root, height=25, width=25, text='Quit', font=('Calibri 18'), command=root.destroy)
        button.place(x=1000, y=550, width=150, height=100, anchor=CENTER)

        root.mainloop()


    def show_program(self, root=None):
        '''
        the main method in our humble "graphical" user interface.
        '''

        self.__init__()

        if root == None:
            pass
        else:
            root.destroy()

        root = Tk()

        root.title('Depth-Limited Search Program for a River-Crossing Puzzle')
        root.geometry('1280x900')
        root.resizable(0, 0)

        text = Label(root, text='Solving a River-Crossing Puzzle Using Depth-Limited Search!')
        text.config(font=('@Malgun Gothic', 32))
        text.place(x=640, y=50, anchor=CENTER)

        text = Label(root, text='People present in this puzzle: Father, His Son #1, His Son #2, Mother, Her Daughter #1, Her Daughter #2, Police Officer, Thief')
        text.config(font=('@Malgun Gothic', 16))
        text.place(x=640, y=200, anchor=CENTER)

        text = Label(root, text='The goal is to transfer all of them from right side of the river, to the left.')
        text.config(font=('@Malgun Gothic', 16))
        text.place(x=640, y=250, anchor=CENTER)

        text = Label(root, text='Rules:')
        text.config(font=('@Malgun Gothic', 16))
        text.place(x=640, y=300, anchor=CENTER)

        text = Label(root, text='Each of two sons can\'t be alone with mother.\nEach of two daughters can\'t be alone with father.\nPolice must be with thief at all times, unless the thief is alone on that side of the river.\nOnly the father, the mother and the police officer can be the captain of our humble boat.\nOnly two people can get transferred at the time.\nThe captain can go to the other side, alone, too.')
        text.config(font=('@Malgun Gothic', 16))
        text.place(x=640, y=420, anchor=CENTER)

        label = Label(root, text='Please enter a number as depth or limit for our algorithm.\n(A number between preferably ONE and PLUS INFINITY)\n"Search" button searches with default values.\n"Custom Search" button searches with your inputs.')
        label.config(font=('@Malgun Gothic', 14))
        label.place(x=640, y=600, anchor=CENTER)

        entry_limit = Entry(root, font=('Calibri 18'), justify='center')
        entry_limit.place(x=640, y=750, width=150, height=50, anchor=CENTER)

        button = Button(root, height=25, width=25, text='Search', font=('Calibri 18'))
        button.place(x=450, y=750, width=150, height=100, anchor=CENTER)
        button['command'] = lambda button=button: self.show_search(root, entry_limit.get())


        button = Button(root, height=25, width=25, text='Quit', font=('Calibri 18'), command=root.destroy)
        button.place(x=850, y=750, width=150, height=100, anchor=CENTER)

        button = Button(root, height=25, width=25, text='Custom Search', font=('Calibri 18'))
        button.place(x=150, y=750, width=200, height=100, anchor=CENTER)
        button['command'] = lambda button=button: self.show_custom_search(root)

        root.mainloop()


user = River()
user.show_program()
