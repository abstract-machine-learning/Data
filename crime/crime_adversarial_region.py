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
	
	print("\t- Testing [CRIME][CAT]")
	perturbation = Perturbation.category(dataset, columns, ['state'])
	perturbation_path = base_dir + './perturbation/crime-cat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	#result = Experiment.test({'model': config, 'perturbation': perturbation_path})
	#results['crime']['cat'] = result
	
	print("\t- Testing [CRIME][NOISE]")
	noise_on = [c for c in columns if c != 'state']
	perturbation = Perturbation.noise(dataset, columns, noise_on, 0.3)
	perturbation_path = base_dir + './perturbation/crime-noise-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	#result = Experiment.test({'model': config, 'perturbation': perturbation_path})
	#results['crime']['noise'] = result
	
	print("\t- Testing [CRIME][NOISE-CAT]")
	noise_on = [c for c in columns if c != 'state']
	perturbation = Perturbation.noiseCat(dataset, columns, noise_on, 0.3, ['state'])
	perturbation_path = base_dir + './perturbation/crime-noisecat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	#result = Experiment.test({'model': config, 'perturbation': perturbation_path})
	#results['crime']['noise-cat'] = result
	
if __name__ == '__main__':
	execute()
