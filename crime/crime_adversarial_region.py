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

def execute():

	columns = Perturbation.readColumns('./crime/dataset/columns.csv')
	dataset = pd.read_csv('./crime/dataset/test-set.csv', header=None, skiprows=1)

	print ("\t- Tiers [CRIME]")
	tiers = Perturbation.readTiers(columns)
	Perturbation.saveTiers(tiers,'./crime/perturbation/crime-tier.dat')

	print("\t- Testing [CRIME][Top]")
	perturbation = Perturbation.top(columns)
	Perturbation.savePerturbation(perturbation, './crime/perturbation/crime-top-adversarial-region.dat')
	
	
	print("\t- Testing [CRIME][CAT]")
	perturbation = Perturbation.category(dataset, columns, ['state'])
	perturbation_path = base_dir + './perturbation/crime-cat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)

	
	print("\t- Testing [CRIME][NOISE]")
	noise_on = [c for c in columns if c.split('=', 2)[0] != 'state']
	perturbation = Perturbation.noise(dataset, columns, noise_on, 0.05)
	perturbation_path = base_dir + './perturbation/crime-noise-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)

	
	print("\t- Testing [CRIME][NOISE-CAT]")
	noise_on = [c for c in columns if c.split('=', 2)[0] != 'state']
	perturbation = Perturbation.noiseCat(dataset, columns, noise_on, 0.05, ['state'])
	perturbation_path = base_dir + './perturbation/crime-noisecat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)

	
if __name__ == '__main__':
	execute()
