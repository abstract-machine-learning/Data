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
	columns = Perturbation.readColumns('./compas/dataset/columns.csv')
	dataset = pd.read_csv('./compas/dataset/test-set.csv', header=None, skiprows=1)

	print ("\t- Tiers [COMPAS]")
	tiers = Perturbation.readTiers(columns, ['race_caucasian'])
	Perturbation.saveTiers(tiers,'./compas/perturbation/compas-tier.dat')

	print("\t- Testing [COMPAS][Top]")
	perturbation = Perturbation.top(columns)
	Perturbation.savePerturbation(perturbation, './compas/perturbation/compas-top-adversarial-region.dat')
	
	print("\t- Testing [COMPAS][CAT]")
	perturbation = Perturbation.category(dataset, columns, ['race_caucasian'])
	perturbation_path = base_dir + '/perturbation/compas-cat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	print("\t- Testing [COMPAS][NOISE")
	noise_on = ['age', 'diff_custody', 'diff_jail', 'priors_count', 'juv_fel_count', 'v_score_text', 'sex_male', 'c_charge_degree_m']
	perturbation = Perturbation.noise(dataset, columns, noise_on, 0.05)
	perturbation_path = base_dir + '/perturbation/compas-noise-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	print("\t- Testing [COMPAS][NOISE-CAT]")
	noise_on = ['age', 'diff_custody', 'diff_jail', 'priors_count', 'juv_fel_count', 'v_score_text', 'sex_male', 'c_charge_degree_m']
	perturbation = Perturbation.noiseCat(dataset, columns, noise_on, 0.05, ['race_caucasian'])
	perturbation_path = base_dir + '/perturbation/compas-noisecat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)


def executeCustom(perturbType, features):

	columns = Perturbation.readColumns('./compas/dataset/columns.csv')
	dataset = pd.read_csv('./compas/dataset/test-set.csv', header=None, skiprows=1)

	print ("\t- Tiers [COMPAS]")
	tiers = Perturbation.readTiers(columns, ['race_caucasian'])
	Perturbation.saveTiers(tiers,'./compas/perturbation/compas-tier.dat')
	
	if("cat" in perturbType):
		print("\t- Testing [COMPAS][CAT]")
		perturbation = Perturbation.category(dataset, columns, features)
		perturbation_path = base_dir + '/perturbation/compas-cat-adversarial-region.dat'
		Perturbation.savePerturbation(perturbation, perturbation_path)
	
	elif("noise" in perturbType):
		print("\t- Testing [COMPAS][NOISE]")
		perturbation = Perturbation.noise(dataset, columns, features, 0.3)
		perturbation_path = base_dir + '/perturbation/compas-noise-adversarial-region.dat'
		Perturbation.savePerturbation(perturbation, perturbation_path)
	

	
if __name__ == '__main__':
	execute()
