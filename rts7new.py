import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from random import randint, random, choice
import math
import pdb


class GeneticAlgorithm:
    def __init__(self, a: int, b: int, c: int, d: int, y: int, population_num=100):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.y = y
        self.population = []
        self.deltas = []
        self.m = population_num
        self.iteration = 0
        self.num_mutations = 0

    def find_solution(self):
        self.generate_random_population()
        while True:
            self.find_deltas()
            if 0 in self.deltas:
                return self.population[self.deltas.index(0)]
            else:
                surv_probs = self.find_survival_likelyhood()

                pdb.set_trace()
                # sort all parents by likelyhood
                for i in range(1, self.m): 
                    key1 = self.population[i]
                    key2 = surv_probs[i]
                    j = i-1
                    while j >= 0 and key2 > surv_probs[j]: 
                        surv_probs[j+1] = surv_probs[j] 
                        self.population[j+1] = self.population[j]
                        j -= 1

                    surv_probs[j+1] = key2
                    self.population[j+1] = key1

                pdb.set_trace()
                new_generation = []
                for i in range(self.m):
                    # creating new population
                    parent1 = self.get_random_parent(surv_probs)
                    parent2 = self.get_random_parent(surv_probs)
                    
                    cut = random()
                    if cut < 0.3333:
                        child_1var = parent1[:1] + parent2[1:]
                        child_2var = parent2[:1] + parent1[1:]
                    elif cut < 0.6666:
                        child_1var = parent1[:2] + parent2[2:]
                        child_2var = parent2[:2] + parent1[2:]
                    else:
                        child_1var = parent1[:3] + parent2[3:]
                        child_2var = parent2[:3] + parent1[3:]
                    
                    new_generation.append(choice([child_1var, child_2var]))
                    self.iteration += 1
                self.population = new_generation


    def generate_random_population(self):
        highest = self.y // 2
        for i in range(self.m):
            self.population.append([randint(0, highest), randint(0, highest), \
                                    randint(0, highest), randint(0, highest)])

    def fitness_function(self, x: list):
        assert (len(x) == 4)
        return self.a * x[0] + self.b * x[1] + self.c * x[2] + self.d * x[3]
    
    def find_deltas(self):
        self.deltas = []
        for x in self.population:
            self.deltas.append(abs(self.fitness_function(x) - self.y))

    def find_survival_likelyhood(self):
        sv = []
        sum_prob = .0
        for d in self.deltas:
            sum_prob += 1 / d
        for d in self.deltas:
            sv.append(1 / d / sum_prob)
        return sv
    
    def get_random_parent(self, surv_probs):
        score = random()
        for i in range(self.m):
            if score <= surv_probs[i]:
                return self.population[i]
            else:
                score -= surv_probs[i]
        raise Exception("Parent was not found.")

    def apply_mutation(self, x):
        # Apply mutation with mut_prob probability
        if (random() <= self.mut_prob):
            mut_ind = choice([0, 1, 2, 3])  # random pos of mutation
            new_num = randint(0, self.y // 2)  # new mutation value
            x[mut_ind] = new_num  # replace old num with new value
            self.num_mutations += 1

        return x
        

class SimpleApp(kivy.app.App):
    def build(self): 
        self.label = Label(text="Choose parameters for your genetic algorithm.")
        
        self.label_a = Label(text="Write integer for a:")
        self.input_a = TextInput() 
        
        self.label_b = Label(text="Write integer for b:")
        self.input_b = TextInput()
        
        self.label_c = Label(text="Write integer for c:")
        self.input_c = TextInput()

        self.label_d = Label(text="Write integer for d:")
        self.input_d = TextInput()

        self.label_y = Label(text="Write integer for y:")
        self.input_y = TextInput()

        self.label_population = Label(text="Write size of the population:")
        self.input_population = TextInput()

        self.button = Button(text="Evolution")
        self.button.bind(on_press=self.displayMessage)

        self.boxLayout = kivy.uix.boxlayout.BoxLayout(orientation="vertical")
        self.boxLayout.add_widget(self.label)
        self.boxLayout.add_widget(self.label_a)
        self.boxLayout.add_widget(self.input_a)
        self.boxLayout.add_widget(self.label_b)
        self.boxLayout.add_widget(self.input_b)
        self.boxLayout.add_widget(self.label_c)
        self.boxLayout.add_widget(self.input_c)
        self.boxLayout.add_widget(self.label_d)
        self.boxLayout.add_widget(self.input_d)
        self.boxLayout.add_widget(self.label_y)
        self.boxLayout.add_widget(self.input_y)
        self.boxLayout.add_widget(self.label_population)
        self.boxLayout.add_widget(self.input_population)
        self.boxLayout.add_widget(self.button)

        return self.boxLayout

    def displayMessage(self, btn):
        try:
            a = int(self.input_a.text)
            b = int(self.input_b.text)
            c = int(self.input_c.text)
            d = int(self.input_d.text)
            y = int(self.input_y.text)
            m = int(self.input_population.text)
        except Exception:
            self.label.text = "Wrong arguments were given. Check all of them"

        genalg = GeneticAlgorithm(a=a, b=b, c=c, d=d, y=y, population_num=m)
        result = genalg.find_solution()
        self.label.text = "Result is {}.\n" \
                          "Number of mutations is {}".format(result, genalg.num_mutations)


if __name__ == "__main__":
    #genalg = GeneticAlgorithm(a=1, b=2, c=3, d=4, y=24)
    #result = genalg.find_solution()
    #print(result)
    app = SimpleApp()
    app.run()
