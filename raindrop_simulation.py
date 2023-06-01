import cv2
import numpy as np

class RaindropSimulation:

    # Default kernel (0)
    AVG_ADJ_KERNEL = np.array([
            [1.0, 2.0, 1.0],
            [2.0, 0.0, 2.0],
            [1.0, 2.0, 1.0]
            ])/12

    # Wave kernel (1)
    WAVE_KERNEL = np.array([
            [2.0, 2.0, 1.0],
            [2.0, 0.0, 2.0],
            [1.0, 2.0, 0.0]
            ])/13

    # Art kernel (2)
    ART_KERNEL = np.array([
            [3.0, 2.0, 1.0],
            [2.0, 0.0, 2.0],
            [1.0, 2.0, 0.0]
            ])/14.25

    def __init__(self, shape, drop_prob=0.0):
        self.shape = shape
        self.drop_prob = drop_prob
        self.kernel = RaindropSimulation.AVG_ADJ_KERNEL
        self.prev = np.zeros(shape, dtype=float)
        self.cur = np.zeros(shape, dtype=float)
        self.next = np.zeros(shape, dtype=float)

    def update(self):
        # randomly add drops at some probability
        if np.random.sample() < self.drop_prob:
            sim.set_random_drop()

        # next = avg of adjacent cells + velocity
        # velocity = cur - prev
        cv2.filter2D(src=self.cur, dst=self.next, ddepth=-1, kernel=self.kernel)
        self.next += self.cur - self.prev # velocity
        self.next *= 0.99 # dampen so ripples lose energy

        np.clip(self.next, 0, 255, out=self.next)

        np.copyto(self.prev, self.cur)
        np.copyto(self.cur, self.next)

    def set_drop(self, row, col):
        # sampling from normal distribution looked a bit nicer
        # than sampling from uniform distribution
        self.cur[row][col] = np.random.normal(loc=100, scale=20)

    def set_random_drop(self):
        row = np.random.randint(0, self.shape[0])
        col = np.random.randint(0, self.shape[1])
        self.set_drop(row, col)

    def get_image(self):
        # data is transformed and clipped so it looks more 
        # realisitic in the ocean color map
        img = np.clip(self.cur * 0.5 + 160, 150, 190).astype(np.uint8)
        img_colormap = cv2.applyColorMap(img, cv2.COLORMAP_OCEAN)
        return img_colormap

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        sim.set_drop(y,x)

def on_prob_trackbar(val):
    # divide by 100 since trackbar value must be int
    sim.drop_prob = val / 100

def on_kernel_trackbar(val):
    if val == 0:
        sim.kernel = RaindropSimulation.AVG_ADJ_KERNEL
    elif val == 1:
        sim.kernel = RaindropSimulation.WAVE_KERNEL
    elif val == 2:
        sim.kernel = RaindropSimulation.ART_KERNEL

sim = RaindropSimulation(shape=(200,200))

window_name = 'Raindrop Simulation'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, mouse_click)

# Trackbar controls for drop_prob and kernel
cv2.createTrackbar('Drop Percent', window_name, 0, 100, on_prob_trackbar)
cv2.createTrackbar('Kernel Type', window_name, 0, 2, on_kernel_trackbar)

while True:
    sim.update()

    # resize the window to (600,600) otherwise 
    # its the same size as the small image
    cv2.resizeWindow(window_name, 600, 600)
    cv2.imshow(window_name, sim.get_image())

    # exit on escape key
    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()
