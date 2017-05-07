import random
import enum
import matplotlib.pyplot as plt
from matplotlib import animation, colors

class Genotype(enum.Enum):
	R = 0
	T = 1
	S = 2
	G = 3
	Q = 4
	RT = 5
	RS = 6
	RG = 7
	RP = 8
	TS = 9
	TG = 10
	TP = 11
	SG = 12
	SP = 13
	GP = 14
	RTS = 15
	RTG = 16
	RTP = 17
	RSG = 18
	RSP = 19
	RRGP = 20
	TSG = 21
	TSP = 22
	TGP = 23
	SGP = 24
	RTSG = 25
	RTSP = 26
	RTGP = 27
	RSGP = 28
	TSGP = 29
	RTSGP = 30

class Simulation:
	def __init__(self, output="output", max_steps=5000):
		self.fitness = [1.012, 1.142, 1.105, 1.027, 1.000, 1.103, 1.118, 1.047, 1.022, 1.205, 1.149, 1.193,
						1.124, 1.185, 1.075, 1.197, 1.158, 1.189, 1.124, 1.204, 1.126, 1.201, 1.280, 1.216, 1.186, 1.228, 1.277,
						1.190, 1.212, 1.300, 1.328]
		self.output = output
		self.learning_rate = 0.001
		self.max_steps = max_steps
		self.converged=False
		self.weights = []

		for g in Genotype:
			self.weights.append(1/len(Genotype))

		self.fig, self.ax = plt.subplots()
		self.line, = self.ax.plot(self.weights)
		self.ax.set_ylim(0, 1)
		
		random.seed()

	def generate_child(self):	
		r = random.random()

		for i in range(len(self.weights)):
			r = r - self.weights[i]

			if r <= 0:
				return i
			

	def update(self):
		child = self.generate_child()
		print(Genotype(child))
		fitness = self.fitness[child]
		
		w_previous = self.weights[child]

		self.weights[child] = (1 + self.learning_rate*fitness)*self.weights[child]

		s = sum(self.weights)
		for w in range(len(self.weights)):
			self.weights[w] = self.weights[w] / s
				
		w_current = self.weights[child]

		if abs(w_current - w_previous) <= 0.0001:
			self.converged=True


	def print_weights(self):
		with open(self.output, mode="a") as ofile:
			for row in self.weights:
				for col in row:
					ofile.write(str(col) +",")

			ofile.write("\n")
	
	def animate(self, i):
		self.line.set_data(self.weights)
		self.update()


	def run(self):
		with open(self.output, mode="w") as ofile:
			for i in range(self.max_steps):
				ofile.write(str(self.weights)+"\n")
				self.update()


if __name__ == "__main__":
	sim = Simulation(max_steps=100000)
	
	sim.run()
