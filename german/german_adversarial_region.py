import sys
from os import path
import numpy as np
import pandas as pd
import Dataset
import Perturbation
import json
import time


def execute(perturbType, features, epsilon):
	if(features != []):
		executeCustom(perturbType,features,epsilon)
		return
	columns = Perturbation.readColumns('./german/dataset/columns.csv')
	dataset = pd.read_csv('./german/dataset/test-set.csv', header=None, skiprows=1)
	

	print ("\t- Tiers [GERMAN]")
	tiers = Perturbation.readTiers(columns,['sex_male'])
	Perturbation.saveTiers(tiers,'./german/perturbation/german-tier.dat')

	if("top" in perturbType):
		print("\t- Testing [GERMAN][Top]")
		perturbation = Perturbation.top(columns)
		Perturbation.savePerturbation(perturbation, './german/perturbation/german-top-adversarial-region.dat')
	
	if("cat" in perturbType):
		print("\t- Testing [GERMAN][CAT]")
		perturbation = Perturbation.category(dataset, columns, ['sex_male'])
		Perturbation.savePerturbation(perturbation, './german/perturbation/german-cat-adversarial-region.dat')
	
	if("noise" in perturbType):
		print("\t- Testing [GERMAN][NOISE]")
		noise_on = ['months', 'credit_amount', 'investment_as_income_percentage', 'residence_since', 'age', 'number_of_credits', 'people_liable_for', 'telephone_A192', 'foreign_worker_A202']
		perturbation = Perturbation.noise(dataset, columns, noise_on, 0.05)
		Perturbation.savePerturbation(perturbation, './german/perturbation/german-noise-adversarial-region.dat')
	
	if("noisecat" in perturbType):
		print("\t- Testing [GERMAN][NOISE-CAT]")
		noise_on = ['months', 'credit_amount', 'investment_as_income_percentage', 'residence_since', 'age', 'number_of_credits', 'people_liable_for', 'telephone_A192', 'foreign_worker_A202']
		perturbation = Perturbation.noiseCat(dataset, columns, noise_on, 0.05, ['sex_male'])
		Perturbation.savePerturbation(perturbation, './german/perturbation/german-noisecat-adversarial-region.dat')

def executeCustom(perturbType, features,epsilon = 0.3):
	columns = Perturbation.readColumns('./german/dataset/columns.csv')
	dataset = pd.read_csv('./german/dataset/test-set.csv', header=None, skiprows=1)

	print ("\t- Tiers [GERMAN]")
	tiers = Perturbation.readTiers(columns,['sex_male'])
	Perturbation.saveTiers(tiers,'./german/perturbation/german-tier.dat')
	
	if("cat" in perturbType):
		print("\t- Testing [GERMAN][CAT]")
		perturbation = Perturbation.category(dataset, columns, features)
		Perturbation.savePerturbation(perturbation, './german/perturbation/german-cat-adversarial-region.dat')
	
	elif("noise" in perturbType):
		print("\t- Testing [GERMAN][NOISE]")
		perturbation = Perturbation.noise(dataset, columns, features, epsilon)
		Perturbation.savePerturbation(perturbation, './german/perturbation/german-noise-adversarial-region.dat')

if __name__ == '__main__':
	execute()
