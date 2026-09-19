#!/usr/bin/env python3

"""
This code is adapted by Ken Brown from code provided by Wolfgang Hoenig, 
Jiaoyang Li and Sven Koenig, University of Southern California.
"""

from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib as mpl

Colors = ['aqua', 'blue', 'blueviolet']
Heatcolors = ['white', 'beige', 'papayawhip', 'bisque', 'orange', ]
cmap = mpl.colormaps['Reds']
heatcolors = cmap(np.linspace(0,1,41))
print("Length of the colorlist is", len(heatcolors))


class Animation:
    def __init__(self, my_map, start, finish, path):
        self.my_map = np.flip(np.transpose(my_map), 1)
        self.start = (start[1], len(self.my_map[0]) - 1 - start[0])
        self.finish = (finish[1], len(self.my_map[0]) - 1 - finish[0])
        self.path = []
        for loc in path:
            self.path.append((loc[1], len(self.my_map[0]) - 1 - loc[0]))

        aspect = len(self.my_map) / len(self.my_map[0])

        self.fig = plt.figure(frameon=False, figsize=(8 * aspect, 8))
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=None, hspace=None)
        # self.ax.set_frame_on(False)

        self.patches = []
        self.artists = []
        self.agent = None
        self.trail = []
        self.footprint = None
        
        # create boundary patch

        x_min = -0.5
        y_min = -0.5
        x_max = len(self.my_map) - 0.5
        y_max = len(self.my_map[0]) - 0.5
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        self.patches.append(Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, facecolor='none', edgecolor='gray'))
        for i in range(len(self.my_map)):
            for j in range(len(self.my_map[0])):
                if self.my_map[i][j] in ['X','X\n']:
                    self.patches.append(Rectangle((i - 0.5, j - 0.5), 1, 1, 
                                                  facecolor='black', 
                                                  edgecolor='gray'))
                else:
                    if self.my_map[i][j] == 'S' or self.my_map[i][j] == 'F':
                        self.my_map[i][j] = 0
                    self.patches.append(Rectangle((i - 0.5, j - 0.5), 1, 1, 
                                                  facecolor=heatcolors[(int)(self.my_map[i][j])], 
                                                  edgecolor='gray'))

        # create agent:
        # draw start and finish  first
        self.patches.append(Rectangle((self.start[0] - 0.25, self.start[1] - 0.25), 0.5, 0.5, 
                                          facecolor=Colors[0],
                                          edgecolor='black', alpha=0.5))
        self.patches.append(Rectangle((self.finish[0] - 0.25, self.finish[1] - 0.25), 0.5, 0.5, 
                                          facecolor=Colors[1],
                                          edgecolor='black', alpha=0.5))
        self.agent = Circle((start[0], start[1]), 0.3, facecolor=Colors[i % len(Colors)],
                                    edgecolor='black')
        self.agent.original_face_color = Colors[2]
        self.patches.append(self.agent)
        self.T = len(path) - 1

        self.animation = animation.FuncAnimation(self.fig, self.animate_func,
                                                 init_func=self.init_func,
                                                 frames=int(self.T + 1) * 2,  # was *10
                                                 interval=1,# was 100
                                                 cache_frame_data = False,
                                                 blit=True)

    def save(self, file_name, speed):
        self.animation.save(
            file_name,
            fps=100 * speed,  # was 10*
            dpi=200,
            savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

    @staticmethod
    def show():
        plt.show()

    def init_func(self):
        for p in self.patches:
            self.ax.add_patch(p)
        for a in self.artists:
            self.ax.add_artist(a)
        return self.patches + self.artists

    def animate_func(self, t):
        pos = self.get_state(t / 2, self.path)   # was /10
        self.agent.center = (pos[0], pos[1])
        # add this location as part of the trace of the path
        p = Circle((pos[0],pos[1]), 0.3, facecolor=Colors[1],edgecolor='black')
        self.patches.append(p)
        self.ax.add_patch(p)
        
        # reset all colors
        self.agent.set_facecolor(self.agent.original_face_color)

        return self.patches + self.artists

    @staticmethod
    def get_state(t, path):
        if int(t) <= 0:
            return np.array(path[0])
        elif int(t) >= len(path):
            return np.array(path[-1])
        else:
            pos_last = np.array(path[int(t) - 1])
            pos_next = np.array(path[int(t)])
            pos = (pos_next - pos_last) * (t - int(t)) + pos_last
            return pos
