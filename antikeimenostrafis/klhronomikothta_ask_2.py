# multi-levels inheritance child -> parent -> grandparent

class Organism:
    alive = True

class Animal(Organism):

    def eat(self):
        print("This animal is eating")

class Dog(Animal):
    def bark(self):
        print("This dog is barking")

dog = Dog()

dog.eat()
dog.bark()

# ------------------------------------------------------------------------------

# mutliple inheritance

class Prey:
    def flee(self):
        print("This animal flees")

class Predator:
    def hunt(self):
        print("this animal is hunting")

class Rabbit(Prey):
    pass

class Eagle(Predator):
    pass

class Fish(Predator,Prey):
    pass

rabbit = Rabbit()
eagle = Eagle()
fish = Fish()

rabbit.flee()
eagle.hunt()

fish.hunt()
fish.flee()