import sys
from os import path
import numpy as np
import pandas as pd
import Dataset
import Perturbation
import json

def execute():
	columns = Perturbation.readColumns('./german/dataset/columns.csv')
	dataset = pd.read_csv('./german/dataset/test-set.csv', header=None, skiprows=1)

	print ("\t- Tiers [GERMAN]")
	tiers = Perturbation.readTiers(columns)
	Perturbation.saveTiers(tiers,'./german/perturbation/german-tier.dat')
	
	print("\t- Testing [GERMAN][CAT]")
	perturbation = Perturbation.category(dataset, columns, ['sex_male'])
	Perturbation.savePerturbation(perturbation, './german/perturbation/german-cat-adversarial-region.dat')
	
	print("\t- Testing [GERMAN][NOISE]")
	noise_on = ['months', 'credit_amount', 'investment_as_income_percentage', 'residence_since', 'age', 'number_of_credits', 'people_liable_for', 'telephone_A192', 'foreign_worker_A202']
	perturbation = Perturbation.noise(dataset, columns, noise_on, 0.9)
	Perturbation.savePerturbation(perturbation, './german/perturbation/german-noise-adversarial-region.dat')
	
	
	print("\t- Testing [GERMAN][NOISE-CAT]")
	noise_on = ['months', 'credit_amount', 'investment_as_income_percentage', 'residence_since', 'age', 'number_of_credits', 'people_liable_for', 'telephone_A192', 'foreign_worker_A202']
	perturbation = Perturbation.noiseCat(dataset, columns, noise_on, 0.9, ['sex_male'])
	Perturbation.savePerturbation(perturbation, './german/perturbation/german-noisecat-adversarial-region.dat')

if __name__ == '__main__':
	execute()
