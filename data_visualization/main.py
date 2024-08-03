import matplotlib.pyplot as plt

from random import choice


class RandomWalk:
    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        while len(self.x_values) < self.num_points:
            x_direction = choice([1, -1])
            x_distance = choice([0, 1, 2, 3, 4])
            x_step = x_direction * x_distance

            y_direction = choice([1, -1])
            y_distance = choice([0, 1, 2, 3, 4])
            y_step = y_direction * y_distance

            if x_step == 0 or y_step == 0:
                continue

            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step

            self.x_values.append(x)
            self.y_values.append(y)


def main():
    values = [i for i in range(2, 1000)]
    squares = [i**2 for i in values]

    _, ax = plt.subplots()

    ax.plot(values, squares, linewidth=3)
    ax.set_title("Squares")
    ax.set_xlabel("Value")
    ax.set_ylabel("Square")

    ax.scatter(4, 16, c="red", s=200)
    ax.tick_params(axis="both", labelsize=8)

    plt.show()


if __name__ == "__main__":
    main()
