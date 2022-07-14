import subprocess
import os
import csv
import shutil
import dataset_mapper
import classifier_mapper
import svm
import statistics
from collections import defaultdict
import crime.crime_adversarial_region
import adult.adult_adversarial_region
import compas.compas_adversarial_region
import german.german_adversarial_region
import health.health_adversarial_region
import matplotlib.pyplot as plt
import numpy as np
import time



training_name = "dataset/training-set.csv"
test_name = "dataset/test-set.csv"
adversarial_name = "adversarial-region.dat"

svm_loc = "./domains/{data_folder}/model/"


exceptions = []

def test_SVM(model,data_folder):
	from sklearn import metrics
	dataset_path = f"./{data_folder}/{test_name}"
	dataset_mapper1 = dataset_mapper.DatasetMapper()
	x, y = dataset_mapper1.read(dataset_path)
	y_pred = model.predict(x)
	print("Accuracy:",metrics.accuracy_score(y, y_pred))
	print("Balanced Accuracy:",metrics.balanced_accuracy_score(y, y_pred))

def mlxtrendPrint(svm,data_folder,features):
	from mlxtend.evaluate import feature_importance_permutation
	dataset_path = f"./{data_folder}/{test_name}"
	dataset_mapper1 = dataset_mapper.DatasetMapper()
	x, y = dataset_mapper1.read(dataset_path)
	with open(f"./{data_folder}/dataset/columns.csv", 'r') as f:
		columns = [line for line in csv.reader(f)][0]
	
	imp_vals, imp_all = feature_importance_permutation(
    	predict_method=svm.predict, 
    	X=np.array(x),
    	y=np.array(y),
    	metric='accuracy',
    	num_rounds=10,
    	seed=1)
	
	mlxScore = defaultdict(float)
	for col_id in range(1,len(columns)):
		mlxScore[columns[col_id]] = imp_vals[col_id-1]
	mlxGrade,mlxScore = score_to_grade(mlxScore, canBeZero = True)
	print(f"{mlxScore}")
	if(features == []):
		print(f"{ dict(sorted(mlxGrade.items(), key = lambda kv:abs(float(kv[1]))))} \n")
	else:
		for k,v in mlxScore.items():
			if k in features:
				print(f"mlxScore: {k} -> {v}")


	

def create_model(kernel_name,reg_param = 1,gamma = 1,degree = 1, coef0 = 0,data_folder = "",PerturbFeature = []):	
	
	#s = subprocess.check_call(f"python3 {data_folder}-get.py", shell = True)

	dataset_path = f"./{data_folder}/{training_name}"
	output_path = f"./{data_folder}/svm/{data_folder}-svm_{kernel_name}_g{gamma}_d{degree}_c{coef0}_C{reg_param}.dat"

	#if(os.path.isfile(output_path)==False):
	if(True):
		print(f"Creating SVM: {output_path}")
		# Trains model
		dataset_mapper1 = dataset_mapper.DatasetMapper()
		x, y = dataset_mapper1.read(dataset_path)
		
		trainer = svm.SVM(kernel_name, gamma, degree, coef0, reg_param)
		model = trainer.train(x, y)
		
		classifier_mapper1 = classifier_mapper.ClassifierMapper()
		classifier_mapper1.create(model, output_path)
		test_SVM(model,data_folder)
		start = time.time()
		mlxtrendPrint(model,data_folder,PerturbFeature)
		end = time.time()
		print(f"Time mlx: {end-start}")
		
	else:
		print(f"SVM Already present: {output_path}")

	return output_path


def run_saver(svm_addr,abstraction,perturbation,data_folder,is_OH, get_CE, if_part):
	os.chdir("../saver")
	print(f"\n")
	#os.system("ls")
	print(f"\n")

	perturbation_file = f"../Data/{data_folder}/perturbation/{data_folder}-{perturbation}-{adversarial_name}"
	rel_svm_loc = f"../Data/{svm_addr}"
	rel_dataset_loc = f"../Data/{data_folder}/{test_name}"
	tier_file = f"../Data/{data_folder}/perturbation/{data_folder}-tier.dat"
	is_binary = "1"
	is_top =  1 if (perturbation == "top") else 0
	
	print(f"Start Analysis")
	print(f"bin/saver {rel_svm_loc} {rel_dataset_loc} {abstraction} from_file {perturbation_file} {tier_file} {is_binary} {is_top} {is_OH} {get_CE} {if_part}")
	s = subprocess.check_call(f"bin/saver {rel_svm_loc} {rel_dataset_loc} {abstraction} from_file {perturbation_file} {tier_file} {is_binary} {is_top} {is_OH} {get_CE} {if_part}", shell = True)
	os.chdir(f"../Data/")
	print(f"Finished Analysis")

# Loop over reg parameters
def loop_model2(kernel_name,reg_params,gammas,degrees,coef0s,abstractions,perturbations,data_folder,is_OH, get_CE, if_part):
	for reg in reg_params:
		if kernel_name == 'linear':
			svm_addr = create_model(kernel_name,reg,data_folder = data_folder)
			loop_saver(svm_addr,abstractions,perturbations,data_folder,is_OH, get_CE, if_part)
		
		if kernel_name == 'rbf':
			for gamma in gammas:
				svm_addr = create_model(kernel_name,reg, gamma = gamma,data_folder = data_folder)
				loop_saver(svm_addr,abstractions,perturbations,data_folder,is_OH, get_CE, if_part)
		
		if kernel_name == 'poly':
			for degree in degrees:
				for coef0 in coef0s:
					try:
						svm_addr = create_model(kernel_name,reg, degree = degree, coef0 = coef0,data_folder = data_folder)
						loop_saver(svm_addr,abstractions,perturbations,data_folder,is_OH, get_CE, if_part)
					except:
						print(f"\t-----Exception Occured for (degree= {degree},coeff = {coef0})--------")
						exceptions.append((degree,coef0))

# Each reg parameter is for a variable.
def loop_model(kernel_name,reg_params,gammas,degrees,coef0s,abstractions,perturbations,data_folder,is_OH, get_CE, if_part,PerturbFeature):
	#for reg in reg_params:
		#for kernel_name in kernel_names:
	if kernel_name == 'linear':
		svm_addr = create_model(kernel_name,reg_params[0],data_folder = data_folder,PerturbFeature = PerturbFeature)
		loop_saver(svm_addr,abstractions,perturbations,data_folder,is_OH, get_CE, if_part)
	
	if kernel_name == 'rbf':
		for gamma in gammas:
			svm_addr = create_model(kernel_name,reg_params[1], gamma = gamma,data_folder = data_folder, PerturbFeature = PerturbFeature)
			loop_saver(svm_addr,abstractions,perturbations,data_folder,is_OH, get_CE, if_part)
	
	if kernel_name == 'poly':
		for degree in degrees:
			for coef0 in coef0s:
				try:
					svm_addr = create_model(kernel_name,reg_params[2], degree = degree, coef0 = coef0,data_folder = data_folder, PerturbFeature= PerturbFeature)
					loop_saver(svm_addr,abstractions,perturbations,data_folder,is_OH, get_CE, if_part)
				except:
					print(f"\t-----Exception Occured for (degree= {degree},coeff = {coef0})--------")
					exceptions.append((degree,coef0))

def loop_saver(svm_addr,abstractions,perturbations,data_folder,is_OH, get_CE, if_part):
	for abstraction in abstractions:
		for perturbation in perturbations:
			start = time.time()

			run_saver(svm_addr,abstraction,perturbation,data_folder,is_OH, get_CE, if_part)
			end = time.time()
			print(f"Time Saver: {end-start}")
			

def get_avg(rawPath,kernel_types,reg_params,gammas,degrees,coef0s,abstractions,perturbations):
	kernel = kernel_types[0]
	file1 = open(rawPath,"r+") 
	lines = file1.readlines()
	lineNo = 0
	Bac,Rob = [],[]
	if kernel == "linear":
		print(f"reg \t Acc. \t\t B. Acc. \t Robustness")
		for reg in reg_params:
			average = [0,0,0]
			c = 0
			for i in range(len(perturbations)*len(abstractions)):
				line = lines[lineNo]
				line = line.split()
				for i in range(3):
					average[i] += float(line[i])
				c+=1
				lineNo += 1
			for i in range(3):
				average[i] /= c
			Bac.append(average[1])
			Rob.append(average[2])
			print(f"{reg} \t {average[0]} \t {average[1]} \t {average[2]}")
	if kernel == "poly":
		print(f"reg \t deg. \t coef0 \t Acc. \t\t B. Acc. \t Robustness")
		for reg in reg_params:
			for degree in degrees:
				for coef0 in coef0s:
					if (degree,coef0) in exceptions:
						print(f"{reg}	{degree}	{coef0}	  exception")
						continue
					average = [0,0,0]
					c = 0
					for i in range(len(perturbations)*len(abstractions)):
						line = lines[lineNo]
						line = line.split()
						for i in range(3):
							average[i] += float(line[i])
						c+=1
						lineNo += 1
					for i in range(3):
						average[i] /= c
					Bac.append(average[1])
					Rob.append(average[2])
					print(f"{reg}	{degree}	{coef0}	  {average[0]}	{average[1]}  {average[2]}")
	if kernel == "rbf":
		print(f"reg \t gamma \t\t Acc. \t\t B. Acc. \t Robustness")
		for reg in reg_params:
			for gamma in gammas:
				average = [0,0,0]
				c = 0
				for i in range(len(perturbations)*len(abstractions)):
					line = lines[lineNo]
					line = line.split()
					for i in range(3):
						average[i] += float(line[i])
					c+=1
					lineNo += 1
				for i in range(3):
					average[i] /= c
				Bac.append(average[1])
				Rob.append(average[2])
				print(f"{reg} \t {gamma} \t {average[0]} \t {average[1]} \t {average[2]}")

	print()
	file1.close()
	return(Bac,Rob)

def boxplotCrime(Bac,Rob,is_OH,kernel_types,abstractions):
	txt = "with OH" if is_OH else ""
	title = f"Kernel: {kernel_types[0]}; Abs. Domain: {abstractions[0]} {txt}"
	boxplotter(Bac,Rob,title)

def boxplotDatasets(Bac,Rob,data_folder):
	title = data_folder
	boxplotter(Bac,Rob,title)	

def boxplotter(Bac,Rob,title):
	fig = plt.figure(figsize =(10, 7))
	ax = fig.add_axes([0.1, 0.1, 0.9, 0.9])
	bp = ax.boxplot([Bac,Rob])
	ax.set_xticklabels(['B. Acc', 'Robust.'])
	plt.title(title)
	plt.show()

def ThreeDpolyPlotter(Bac,Rob,degrees,coef0s):
	x = []
	y = []
	for degree in degrees:
		for coef0 in coef0s:
			x.append(degree)
			y.append(coef0)
	fig = plt.figure()
	ax = plt.axes(projection ='3d')
	ax.plot_surface(np.array(x), np.array(y), np.array(Bac), cmap ='viridis', edgecolor ='red', alpha=0.5)
	ax.plot_surface(np.array(x), np.array(y), np.array(Rob), cmap ='viridis', edgecolor ='blue', alpha=0.5)
	ax.set_title('Dataset: Crime, Kernel: Poly ')
	plt.show()

def raw_print(rawPath):
	Bac = []
	Rob = []
	print(f"Acc. \t B. Acc. \t Robustness") 
	file1 = open(rawPath,"r+") 
	average = [0,0,0]
	c = 0
	for line in file1.readlines():
		line = line.split()
		print(f"{line[0]}\t{line[1]}\t{line[2]}")
		Bac.append(float(line[1]))
		Rob.append(float(line[2]))
		for i in range(3):
			average[i] += float(line[i])
		c+=1
	for i in range(3):
		average[i] /= c
	print(f"AVERAGE RESULT :\n Accuracy: {average[0]}	Balanced Accuracy: {average[1]}	Robustnedd: {average[2]}")

	print()
	file1.close()
	return Bac,Rob

def score_to_grade(score,canBeZero = False):
	stdev = statistics.stdev(score.values())
	mean = statistics.mean(score.values())
	grade = dict()
	score2 = dict()
	for k,v in score.items():
		if(v == 0 and not canBeZero):
			continue
		score2[k] = v
		if(v > mean + 3*stdev):
			grade[k] = 10
		elif(v > mean + 2*stdev):
			grade[k] = 9
		elif(v > mean + stdev):
			grade[k] = 8
		elif(v > mean):
			grade[k] = 7
		elif(v > mean - stdev):
			grade[k] = 6
		elif(v > mean - 2*stdev):
			grade[k] = 5
		elif(v > mean - 3*stdev):
			grade[k] = 4
		else:
			grade[k] = 3
	grade = dict(sorted(grade.items(), key = lambda kv:abs(float(kv[1]))))
	score2 = dict(sorted(score2.items(), key = lambda kv:abs(float(kv[1]))))
	#print(f"G->{len(grade)}: {grade}\n\nS->{len(score)}: {score}")
	return grade,score2


def get_feature_score(dataDirPath,kernel_types,data_folder,reg_params,gammas,degrees,coef0s):
	fileR = open(f"{dataDirPath}/{data_folder}-feature_score_raw.txt","r+")
	fileW = open(f"{dataDirPath}/{data_folder}-feature_analysis.txt","w+")
	with open(dataDirPath+"/dataset/columns.csv", 'r') as f:
		columns = [line for line in csv.reader(f)][0]
	CG_L,CG_R,CG_P,CG = defaultdict(float),defaultdict(float),defaultdict(float),defaultdict(float)
	count = [0,0,0]
	rawdata = fileR.readlines()
	pos = 0
	for kernel in kernel_types:
		feature_score = dict()
		if 'linear' == kernel:
				fileW.write(f"\n\n\n\nSVM Type: Linear; Reg. Param: {reg_params[0]}\n")
				weights = rawdata[pos].split()
				pos += 1
				for col_i in range(1,len(columns)):
					feature_score[columns[col_i]] = abs(float(weights[col_i]))
				feature_grade,feature_score = score_to_grade(feature_score)
				fileW.write(f"{feature_grade} \n")
				for k,v in feature_grade.items():
					CG_L[k] += v
				count[0] += 1

		if 'poly' == kernel:
			for degree in degrees:
				for coef0 in coef0s:
					fileW.write(f"\n\n\n\nSVM Type: POLY; Reg. Param: {reg_params[2]}; degree: {degree}; coef0: {coef0}\n")
					weights = rawdata[pos].split()
					pos += 1
					for col_i in range(1,len(columns)):
						feature_score[columns[col_i]] = abs(float(weights[col_i]))
					feature_grade,feature_score = score_to_grade(feature_score)
					fileW.write(f"{feature_grade} \n")
					for k,v in feature_grade.items():
						CG_P[k] += v
					count[1] += 1
		if 'rbf' == kernel:
			for gamma in gammas:
				fileW.write(f"\n\n\n\nSVM Type: RBF; Reg. Param: {reg_params[1]}; gamma:{gamma}\n")
				weights = rawdata[pos].split()
				pos += 1
				for col_i in range(1,len(columns)):
					feature_score[columns[col_i]] = abs(float(weights[col_i]))
				feature_grade,feature_score = score_to_grade(feature_score)
				fileW.write(f"{feature_grade} \n")
				for k,v in feature_grade.items():
					CG_R[k] += v
				count[2] += 1
	for col in CG_L.keys():
		CG_L[col] = CG_L[col]/count[0]
		CG_R[col] = CG_R[col]/count[1]
		CG_P[col] = CG_P[col]/count[2]
		CG[col] = (CG_L[col] + CG_R[col] + CG_P[col])/3
	fileW.write(f"\n\n\n----CUMMULATIVE RESULT (Linear)---\n")
	fileW.write(f"{ dict(sorted(CG_L.items(), key = lambda kv:abs(float(kv[1]))))} \n")
	fileW.write(f"\n\n\n----CUMMULATIVE RESULT (RBF)---\n")
	fileW.write(f"{ dict(sorted(CG_R.items(), key = lambda kv:abs(float(kv[1]))))} \n")
	fileW.write(f"\n\n\n----CUMMULATIVE RESULT (Poly)---\n")
	fileW.write(f"{ dict(sorted(CG_P.items(), key = lambda kv:abs(float(kv[1]))))} \n")
	fileW.write(f"\n\n\n----CUMMULATIVE RESULT---\n")
	fileW.write(f"{ dict(sorted(CG.items(), key = lambda kv:abs(float(kv[1]))))} \n")

	print(f"\n\n\n----CUMMULATIVE RESULT (Linear)---\n")
	print(f"{ dict(sorted(CG_L.items(), key = lambda kv:abs(float(kv[1]))))} \n")
	print(f"\n\n\n----CUMMULATIVE RESULT (RBF)---\n")
	print(f"{ dict(sorted(CG_R.items(), key = lambda kv:abs(float(kv[1]))))} \n")
	print(f"\n\n\n----CUMMULATIVE RESULT (Poly)---\n")
	print(f"{ dict(sorted(CG_P.items(), key = lambda kv:abs(float(kv[1]))))} \n")
	print(f"\n\n\n----CUMMULATIVE RESULT---\n")
	print(f"{ dict(sorted(CG.items(), key = lambda kv:abs(float(kv[1]))))} \n")

def createDir(data_folder):
	if(not os.path.isdir(f"./{data_folder}/dataset")):
		os.system(f"mkdir ./{data_folder}/dataset")
	if(not os.path.isdir(f"./{data_folder}/perturbation")):
		os.system(f"mkdir ./{data_folder}/perturbation")
	if(not os.path.isdir(f"./{data_folder}/svm")):
		os.system(f"mkdir ./{data_folder}/svm")		

def caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool= False,is_OH = 1,get_CE = 0,if_part = 0,if_print_raw= False,plot = 'None',PerturbFeature = []):
	createDir(data_folder)
	os.system('rm ../saver/result1.txt')
	os.system('rm ../saver/feature_score_raw.txt')
	os.system('rm ../saver/result_raw.txt')
	os.system('touch ../saver/result1.txt')
	os.system('touch ../saver/result_raw.txt')
	os.system('touch ../saver/feature_score_raw.txt')
	os.chdir(f"./{data_folder}")
	s = subprocess.check_call(f"python3 {data_folder}-get.py", shell = True)
	os.chdir("..")

	if(data_folder == "adult"):
		adult.adult_adversarial_region.execute(perturbations, PerturbFeature)
	if(data_folder == "compas"):
		compas.compas_adversarial_region.execute(perturbations, PerturbFeature)
	if(data_folder == "crime"):
		crime.crime_adversarial_region.execute(perturbations, PerturbFeature)
	if(data_folder == "german"):
		german.german_adversarial_region.execute(perturbations, PerturbFeature)
	if(data_folder == "health"):
		health.health_adversarial_region.execute()
		
	for kernel in kernel_types:
		if(regType == 1):
			loop_model(kernel,reg_params,gammas,degrees,coef0s,abstractions,perturbations,data_folder,is_OH, get_CE, if_part,PerturbFeature)
		if(regType == 2):
			loop_model2(kernel,reg_params,gammas,degrees,coef0s,abstractions,perturbations,data_folder,is_OH, get_CE, if_part)

	dest = shutil.move("../saver/result1.txt", f"./{data_folder}/{data_folder}-results.txt") #shutil.move(source, destination) 
	dest = shutil.move("../saver/result_raw.txt", f"./{data_folder}/{data_folder}-results_raw.txt")
	
	if('top' in perturbations):
		dest = shutil.move("../saver/feature_score_raw.txt", f"./{data_folder}/{data_folder}-feature_score_raw.txt")
		get_feature_score(f"./{data_folder}",kernel_types,data_folder,reg_params,gammas,degrees,coef0s)
	if(get_avg_bool):
		Bac,Rob = get_avg(f"./{data_folder}/{data_folder}-results_raw.txt",kernel_types,reg_params,gammas,degrees,coef0s,abstractions,perturbations,)
		if (plot == 'boxplotCrime'):
			boxplotCrime(Bac,Rob,is_OH,kernel_types,abstractions)
		if (plot == '3DplotPoly'):
			ThreeDpolyPlotter(Bac,Rob,degrees,coef0s)		
	if(if_print_raw):
		Bac,Rob = raw_print(f"./{data_folder}/{data_folder}-results_raw.txt")
		if (plot == 'boxplotDatasets'):
			boxplotDatasets(Bac,Rob,data_folder)


if __name__ == '__main__':
	data_folder = "german"
	reg_params = [1,10,0.01]
	gammas = [0.05]
	degrees = [6]
	coef0s =  [6]
	abstractions = ['interval','raf']
	perturbations = ["cat", "noisecat","noise"]#["top","cat", "noisecat","noise"]
	kernel_types = ['linear','rbf','poly']
	caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,is_OH=1)
	

#if __name__ == '__main__':
#	loop_model('linear')
#	loop_model('rbf')
#	loop_model('poly')

#if __name__ == '__main__':
#	dest = shutil.move("../saver/result1.txt", f"./{data_folder}/{data_folder}-results.txt") #shutil.move(source, destination) 
#	dest = shutil.move("../saver/result_raw.txt", f"./{data_folder}/{data_folder}-results_raw.txt")
#
#	get_avg(f"./{data_folder}/{data_folder}-results_raw.txt")

#-----Crime------
#reg_params = [1,1,1]
#gammas = [0.01,0.001,0.0001,0.00001]
#degrees = [3,9,15,20]
#coef0s = [0]
#abstractions = ['hybrid']


#-----Health------
#reg_params = [0.1]

#-----adult------
#reg_params = [1,0.05,0.01] #for linear raf and poly respectively
#gammas = [0.01,0.03,0.05,0.07,0.09]
#degrees = [3]
#coef0s =  list(range(0,16,3))[1:]
#abstractions = ['hybrid']
#perturbations = ["cat", "noisecat","noise"]



#-----compas------
#reg_params = [1,0.05,0.01]
#gammas = [0.01,0.03,0.05,0.07,0.09]
#degrees = [3]
#coef0s =  list(range(0,16,3))[1:]
#abstractions = ['hybrid']
#perturbations = ["cat", "noisecat","noise"]

#-----German------
#reg_params = [1,10,0.01]#[1,10,0.01]
#gammas = [0.01,0.03,0.05,0.07,0.09]
#degrees = [6]#list(range(0,16,3))[1:]
#coef0s =  list(range(0,16,3))[1:]
#abstractions = ['hybrid']#["interval", "raf","hybrid"]#["interval", "raf","hybrid"]
#perturbations = ["cat", "noisecat","noise"]
#-----------------