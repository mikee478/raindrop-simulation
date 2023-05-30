import cv2
import numpy as np

class RaindropSimulation:

    AVG_ADJ_KERNEL = np.array([
            [0.125, 0.125, 0.125],
            [0.125, 0.000, 0.125],
            [0.125, 0.125, 0.125]
            ])

    def __init__(self, shape, drop_prob):
        self.shape = shape
        self.drop_prob = drop_prob
        self.prev = np.zeros(shape, dtype=float)
        self.cur = np.zeros(shape, dtype=float)
        self.next = np.zeros(shape, dtype=float)

    def update(self):
        # randomly add drops at some probability
        if np.random.sample() < self.drop_prob:
            sim.set_random_drop()

        # next = avg of adjacent cells + velocity
        # velocity = cur - prev
        cv2.filter2D(src=self.cur, dst=self.next, ddepth=-1, kernel=RaindropSimulation.AVG_ADJ_KERNEL)
        self.next += self.cur - self.prev # velocity
        self.next *= 0.88 # dampen so ripples lose energy
        np.copyto(self.prev, self.cur)
        np.copyto(self.cur, self.next)

    def set_drop(self, row, col):
        self.cur[row][col] = 255

    def set_random_drop(self):
        row = np.random.randint(0, self.shape[0])
        col = np.random.randint(0, self.shape[1])
        self.cur[row][col] = 255

    def get_image(self):
        # data is transformed and clipped so it looks more 
        # realisitic in the ocean color map
        img = np.clip(self.cur * 3 + 160, 150, 180).astype(np.uint8)
        img_colormap = cv2.applyColorMap(img, cv2.COLORMAP_OCEAN)
        return img_colormap

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        sim.set_drop(y,x)

sim = RaindropSimulation(shape=(200,200), drop_prob=0.05)
window_name = 'Raindrop Simulation'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, mouse_click)

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
