# By submitting this assignment, I agree to the following:
#  “Aggies do not lie, cheat, or steal, or tolerate those who do”
#  “I have not given or received any unauthorized aid on this assignment”
#
# Name:       Mason Medrano
# Section:    102-503
# Assignment:   population
# Date:           11/30/2018

import random
from math import ceil, floor
import matplotlib.pyplot as plt
import numpy as np


class Person:
    """

    This is a class used to represent individuals within a population
    and the actions they can perform.

    """

    def __init__(self, isSick = False):
        """
        The constructor for the Person class:

        Parameters:
            isSick (Boolean): Determines if an individual is sick or not upon creation.

        Object Attributes:
            resistance(integer): The likelihood for an individual to resist the disease
            recovery(integer): The number it takes an individual to recover from infection
            activity(integer): The number of people an individual interacts with daily
            transmission(integer): The likelihood for an individual to transmit the disease
            deathRisk(integer): The likelihood for an individual to die from the disease
            isSick(Boolean): The qualifier that tells if an individual is sick
            isImmune(Boolean): The qualifier that tells if an individual is immune
            isDead(Boolean):The qualifier that tells if an individual is dead
            numTransmissions(integer): The number of time a sick individual transmitted the disease
        """

        self.resistance = ceil(random.random() * 100)
        self.recovery = ceil(random.random() * 10)
        self.activity = ceil(random.random() * 10)
        self.transmission = ceil(random.random() * 100)
        self.deathRisk = ceil(random.random() * 1)
        self.isSick = isSick
        self.isImmune = False
        self.isDead = False
        self.numTransmissions = 0

    def __str__(self):
        """
        This is a special class used for printing the values of objects.

        """
        return("\nResistance = %d\nTransmission = %d\nActivity = %d\nRecovery = %d\nIs Sick = %s"
              % (self.resistance, self.transmission, self.activity, self.recovery, self.isSick))

    def makeSick(self):
        """
        makeSick changes an object's 'is sick' attribute to true and decreases the individuals activity level.
        """
        self.activity = ceil(self.activity / 2)
        self.isSick = True

    def makeContact(self, person2):
        """
        makeContact simulates an interaction between two individuals within the population.
        It compares the transmission values and resistance values to randomly generatated 'rolls'
        After making the interaction, the second individual has a chance to become sick.

        Parameters:
            person2: an object from the person class used to represent the person becoming infected
        """
        if not person2.isSick and self.isSick:
            transmit_chance = ceil(random.random() * 100)
            # print("Transmit_chance =", transmit_chance)
            resist_chance = ceil(random.random() * 100)
            # print("Resist_chance =", resist_chance)
            if transmit_chance <= self.transmission:
                # print("Transmitted!")
                self.numTransmissions += 1
                if resist_chance >= person2.resistance:
                    # print("Contracted!")
                    person2.makeSick()

    def recover(self):
        """
        recover simulates the recovery of an individual over a day. There is a chance every day for
        an individual to die of the illness, but if they survive the day their recovery value decreases.
        If an individual's recovery reaches zero, they become immune.
        """
        if self.isSick and not self.isDead:
            lethalChance = ceil(random.random() * 100)
            if lethalChance <= self.deathRisk:
                self.isDead = True
                self.recovery = 0
                self.resistance = 101
                self.isSick = False
            else:
                self.recovery -= 1
                if self.recovery == 0:
                    self.isSick = False
                    self.resistance = 101
                    # print("Recovered!")
                    self.isImmune = True

def checkDisease(population):
    """
    checkDisease checks to see if at least one individual in the population is still sick.

    Parameters:
        population(list): A list of Person class object that represent the entire population

    Returns:
        Boolean Value: True if at least one individual is sick, False if not
    """

    disease_present = False
    for person in population:
        if person.isSick == True:
            disease_present = True
            break
    return disease_present

def generatePopulation(popSize):
    """
    generatePopulation creates the population to be represented in the simulation.

    Parameters:
        popSize(integer): The size of the population

    Returns:
        population: a list of Person class objects
    """
    population = []
    population.append(Person(True))
    for i in range(1, popSize):
        population.append(Person())
    return population

def gatherStats(population):
    """
    gatherStats calculates the statistics of the population everyday throughout the simulation.

    Parameters:
        population: A list of Person class objects

    Returns:
        dailySick(integer): The number of sick people on that day
        dailyRecovery(float): The average recovery time for the sick population on that day
        recoveryTime(integer): The number of times an individual recovered a day from the disease
        immuneCount(integer): The number of immune individuals on that day
        dailyTransmission(integer): The number of transmissions on that day
        dailyDead(integer): The number of dead individuals on that day
    """
    dailySick = 0
    dailyRecovery = 0
    recoveryTime = 0
    immuneCount = 0
    dailyTransmissions = 0
    dailyDead = 0
    for people in population:
        if people.isDead:
            dailyDead += 1
        else:
            # Helps measure how many transmissions occurred in one day
            dailyTransmissions += people.numTransmissions
            # Measures the recovery values of the entire population per day
            dailyRecovery += people.recovery
            # Helps measure the daily number of sick people
            if people.isSick:
                dailySick += 1
                # Helps measure the TOTAL AVERAGE RECOVERY TIME
                recoveryTime += 1
            people.recover()
            # Helps measure the daily number of immune individuals; this value is also important for determining how many
            # people were infected overall
            if people.isImmune:
                immuneCount += 1

    return dailySick, dailyRecovery, recoveryTime, immuneCount, dailyTransmissions, dailyDead


# gathers the size of the population from the user
popSize = int(input("Please enter the desired population size: "))

# Generate a population of People objects as defined in the function module
population = generatePopulation(popSize)

# Start a counter of days
day = 1

# Generate some variables and lists that will be useful for statistic analysis
dailySickList = []
dailyImmuneList = []
dailyRecoveryList = []
dailyTransmissions = []
dailyDeadList = []
totalRecoveryTime = 0
recoveryTime = 0

# begin disease simulation and continue as long as at least one person is sick
while checkDisease(population):
    immuneCount = 0
    totalTransmissions = 0
    # Causes interactions between people
    for i in range(len(population)):
        individual = population.pop(0)
        for j in range(individual.activity):
            random_encounter = floor(random.random() * len(population))
            individual.makeContact(population[random_encounter])
        population.append(individual)


    # Measures statistical data and appends it to appropriate list

    dailyStats = gatherStats(population)

    dailySick = dailyStats[0]
    dailySickList.append(dailySick)

    dailyRecovery = dailyStats[1]
    dailyRecoveryList.append(dailyRecovery)

    totalRecoveryTime += dailyStats[2]

    dailyImmune = dailyStats[3]
    dailyImmuneList.append(dailyImmune)

    dailyTransmissions.append(dailyStats[4])
    totalTransmissions += dailyStats[4]

    dailyDead = dailyStats[5]
    dailyDeadList.append(dailyDead)


    # prints the relevant statistics of the population for each day throughout the simulation
    if dailySick == 1:
        print("Day", day, "-\n", dailySick, "person is sick today.")
    else:
        print("Day", day, "-\n", dailySick, "people are sick today.")

    if dailyImmune == 1:
        print("One person is immune to the disease at this time.")
    else:
        print(dailyImmune, "people are immune to the disease at this time.")
    if dailyDead == 1:
        print("One person is dead at this time.\n")
    else:
        print(dailyDead, "people are dead at this time.\n")
    print(round((dailyRecovery/len(population)), 2), "is the average recovery time for the sick population today.")
    day += 1


# prints the statistics of the population after the simulaton is complete
print("The disease was eradicated by day:", day)

maxSick = max(dailySickList)
maxImmune = max(dailyImmuneList)
maxDead = max(dailyDeadList)
totalInfected = maxImmune + maxDead
print(maxSick, "was the highest amount of people infected in one day!")
print(maxDead, " was the number of people killed due to this disease.")
print(totalInfected, "is the total number of people who got sick.")
print(round(totalInfected/popSize*100, 2), "\b% is the percentage of the population who was infected.")
print(round(totalRecoveryTime/maxImmune, 2), "is the average recovery time in days.")
print(round(totalTransmissions/maxImmune, 2), "is the average number of transmissions per infection.")


# plots the daily statistics of the population throughout the simulation in 4 graphs
days = np.linspace(0, len(dailySickList), len(dailySickList))
plt.subplot(2, 2, 1)
plt.title("Number of Individuals")
plt.xlabel("Day")
plt.ylabel("Number of Sick People")
plt.plot(days, dailySickList, ".")


plt.subplot(2, 2, 2)
plt.title("Average Recovery Per Day")
plt.xlabel("Day")
plt.ylabel("Average Recovery Days")
plt.plot(days, dailyRecoveryList, ".")

plt.subplot(2, 2, 3)
plt.title("Number of Individuals Immune and Dead")
plt.xlabel("Day")
plt.ylabel("Number of People")
plt.plot(days, dailyImmuneList, ".", color = "blue", label = "Number of Immune")
plt.plot(days, dailyDeadList, ".", color = "red", label = "Number of Dead")
plt.legend()

plt.subplot(2, 2, 4)
plt.title("Number of Transmissions Per Day")
plt.xlabel("Day")
plt.ylabel("Number of Transmissions")
plt.plot(days, dailyTransmissions, ".")

plt.show()