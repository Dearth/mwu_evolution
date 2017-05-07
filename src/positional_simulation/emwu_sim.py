import random


class Simulation:
    def __init__(self, output="output", max_steps=5000):
        self.fitness = [[2, 5.1, 5.1], [4.9, 3, 5.9], [4.9, 6.1, 3]]
        self.weights = [[(1/3), (1/3), (1/3)], [(1/3), (1/3), (1/3)]]
        self.output = output
        self.learning_rate = 0.01
        self.max_steps = max_steps
        self.converged=False

        random.seed()

    def generate_child(self):
        child = []

        for i in range(2):
            r = random.random()
            index = 0
            
            for w in self.weights[i]:
                r -= w

                if r <= 0:
                    child.append(index)
                    break

                index += 1
        
        return child

    def update(self):
        child = self.generate_child()
        fitness = self.fitness[child[0]][child[1]]
        
        w1_previous = self.weights[0][child[0]]
        w2_previous = self.weights[1][child[1]]

        self.weights[0][child[0]] = (1 + self.learning_rate*fitness)*self.weights[0][child[0]]
        self.weights[1][child[1]] = (1 + self.learning_rate*fitness)*self.weights[1][child[1]]

        for i in range(len(self.weights)):
            s = sum(self.weights[i])
            for j in range(len(self.weights[i])):
                self.weights[i][j] = self.weights[i][j] / s
                
        w1_current = self.weights[0][child[0]]
        w2_current = self.weights[1][child[1]]

        if abs(w1_current - w1_previous) <= 0.0001 and abs(w2_current - w2_previous) <= 0.0001:
            self.converged=True

    def print_weights(self):
        with open(self.output, mode="a") as ofile:
            ofile.write(str(self.weights) +"\n")

    def run(self):
        for step in range(self.max_steps):
            self.print_weights()
            self.update()

            if self.converged:
                return

if __name__ == "__main__":
    sim = Simulation()

    sim.run()
