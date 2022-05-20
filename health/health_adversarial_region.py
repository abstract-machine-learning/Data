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

	columns = Perturbation.readColumns('./health/dataset/columns.csv')
	dataset = pd.read_csv('./health/dataset/test-set.csv', header=None, skiprows=1)
	
	print("\t- Testing [HEALTH][CAT]")
	perturbation = Perturbation.category(dataset, columns, ['AgeAtFirstClaim', 'Sex'])
	perturbation_path = base_dir + '/output/health-cat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	print("\t- Testing [HEALTH][NOISE]")
	noise_on = ['LabCount_total', 'LabCount_months', 'DrugCount_total', 'DrugCount_months', 'Vendor', 'PCP', 'PayDelay', 'max_PayDelay', 'min_PayDelay']
	perturbation = Perturbation.noise(dataset, columns, noise_on, 0.3)
	perturbation_path = base_dir + '/output/health-noise-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)
	
	print("\t- Testing [HEALTH][NOISE-CAT]")
	noise_on = ['LabCount_total', 'LabCount_months', 'DrugCount_total', 'DrugCount_months', 'Vendor', 'PCP', 'PayDelay', 'max_PayDelay', 'min_PayDelay']
	perturbation = Perturbation.noiseCat(dataset, columns, noise_on, 0.3, ['AgeAtFirstClaim', 'Sex'])
	perturbation_path = base_dir + '/output/health-noisecat-adversarial-region.dat'
	Perturbation.savePerturbation(perturbation, perturbation_path)

	
if __name__ == '__main__':
	execute()
