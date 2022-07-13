import sys
import os
from os import path
sys.path.append('.')
sys.path.append('..')
base_dir = path.dirname(path.realpath(__file__)) + '/'
import numpy as np
import pandas as pd
import Dataset
import Perturbation
import json

def execute(perturbType, features):
	if(features != []):
		executeCustom(perturbType,features)
		return
	columns = Perturbation.readColumns('./adult/dataset/columns.csv')
	dataset = pd.read_csv('./adult/dataset/test-set.csv', header=None, skiprows=1)

	print ("\t- Tiers [ADULT]")
	tiers = Perturbation.readTiers(columns, ['sex_male'])
	Perturbation.saveTiers(tiers,'./adult/perturbation/adult-tier.dat')

	print("\t- Testing [ADULT][Top]")
	perturbation = Perturbation.top(columns)
	Perturbation.savePerturbation(perturbation, './adult/perturbation/adult-top-adversarial-region.dat')
	
	print("\t- Testing [ADULT][CAT]")
	perturbation = Perturbation.category(dataset, columns, ['sex_male'])
	perturbation_path = base_dir + '/perturbation/adult-cat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	
	print("\t- Testing [ADULT][NOISE]")
	noise_on = ['age', 'fnlwgt', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week']
	perturbation = Perturbation.noise(dataset, columns, noise_on, 0.05)
	perturbation_path = base_dir + '/perturbation/adult-noise-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	
	print("\t- Testing [ADULT][NOISE-CAT]")
	noise_on = ['age', 'fnlwgt', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week']
	perturbation = Perturbation.noiseCat(dataset, columns, noise_on, 0.05, ['sex_male'])
	perturbation_path = base_dir + '/perturbation/adult-noisecat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)

def executeCustom(perturbType, features):
	columns = Perturbation.readColumns('./adult/dataset/columns.csv')
	dataset = pd.read_csv('./adult/dataset/test-set.csv', header=None, skiprows=1)

	print ("\t- Tiers [ADULT]")
	tiers = Perturbation.readTiers(columns, ['sex_male'])
	Perturbation.saveTiers(tiers,'./adult/perturbation/adult-tier.dat')

	
	print("\t- Testing [ADULT][CAT]")
	perturbation = Perturbation.category(dataset, columns, features)
	perturbation_path = base_dir + '/perturbation/adult-cat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	
	print("\t- Testing [ADULT][NOISE]")
	perturbation = Perturbation.noise(dataset, columns, features, 0.3)
	perturbation_path = base_dir + '/perturbation/adult-noise-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	
if __name__ == '__main__':
	execute()
