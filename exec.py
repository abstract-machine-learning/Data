import subprocess
import os
import csv
import shutil
import dataset_mapper
import classifier_mapper
import svm
import crime.crime_adversarial_region
import adult.adult_adversarial_region
import compas.compas_adversarial_region
import german.german_adversarial_region
import health.health_adversarial_region

data_folder = "german"	
training_name = "dataset/training-set.csv"
test_name = "dataset/test-set.csv"
adversarial_name = "adversarial-region.dat"

svm_loc = "./domains/{data_folder}/model/"

reg_params = [1,10,0.01]#[1,10,0.01]
gammas = [0.01,0.03,0.05,0.07,0.09]
degrees = [6]#list(range(0,16,3))[1:]
coef0s =  list(range(0,16,3))[1:]
abstractions = ['raf']#["interval", "raf","hybrid"]#["interval", "raf","hybrid"]
perturbations = ["top","cat", "noisecat","noise"]
kernel_types = ['linear','rbf','poly']
exceptions = []

def test_SVM(model):
	from sklearn import metrics
	dataset_path = f"./{data_folder}/{test_name}"
	dataset_mapper1 = dataset_mapper.DatasetMapper()
	x, y = dataset_mapper1.read(dataset_path)
	y_pred = model.predict(x)
	print("Accuracy:",metrics.accuracy_score(y, y_pred))
	print("Balanced Accuracy:",metrics.balanced_accuracy_score(y, y_pred))


def create_model(kernel_name,reg_param = 1,gamma = 1,degree = 1, coef0 = 0):	
	
	#s = subprocess.check_call(f"python3 {data_folder}-get.py", shell = True)

	dataset_path = f"./{data_folder}/{training_name}"
	output_path = f"./{data_folder}/svm/{data_folder}-svm_{kernel_name}_g{gamma}_d{degree}_c{coef0}_C{reg_param}.dat"

	if(os.path.isfile(output_path)==False):
	#if(True):
		print(f"Creating SVM: {output_path}")
		# Trains model
		dataset_mapper1 = dataset_mapper.DatasetMapper()
		x, y = dataset_mapper1.read(dataset_path)
		
		trainer = svm.SVM(kernel_name, gamma, degree, coef0, reg_param)
		model = trainer.train(x, y)
		
		classifier_mapper1 = classifier_mapper.ClassifierMapper()
		classifier_mapper1.create(model, output_path)
		test_SVM(model)
	else:
		print(f"SVM Already present: {output_path}")

	return output_path


def run_saver(svm_addr,abstraction = "raf",perturbation = "cat"):
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
	print(f"bin/saver {rel_svm_loc} {rel_dataset_loc} {abstraction} from_file {perturbation_file} {tier_file} {is_binary} {is_top}")
	s = subprocess.check_call(f"bin/saver {rel_svm_loc} {rel_dataset_loc} {abstraction} from_file {perturbation_file} {tier_file} {is_binary} {is_top}", shell = True)
	os.chdir(f"../Data/")
	print(f"Finished Analysis")


#def loop_model(kernel_name):
#	for reg in reg_params:
#		#for kernel_name in kernel_names:
#		if kernel_name == 'linear':
#			svm_addr = create_model(kernel_name,reg)
#			loop_saver(svm_addr)
#		
#		if kernel_name == 'rbf':
#			for gamma in gammas:
#				svm_addr = create_model(kernel_name,reg, gamma = gamma)
#				loop_saver(svm_addr)
#		
#		if kernel_name == 'poly':
#			for degree in degrees:
#				for coef0 in coef0s:
#					try:
#						svm_addr = create_model(kernel_name,reg, degree = degree, coef0 = coef0)
#						loop_saver(svm_addr)
#					except:
#						print(f"\t-----Exception Occured for (degree= {degree},coeff = {coef0})--------")
#						exceptions.append((degree,coef0))

def loop_model(kernel_name):
	#for reg in reg_params:
		#for kernel_name in kernel_names:
	if kernel_name == 'linear':
		svm_addr = create_model(kernel_name,reg_params[0])
		loop_saver(svm_addr)
	
	if kernel_name == 'rbf':
		for gamma in gammas:
			svm_addr = create_model(kernel_name,reg_params[1], gamma = gamma)
			loop_saver(svm_addr)
	
	if kernel_name == 'poly':
		for degree in degrees:
			for coef0 in coef0s:
				try:
					svm_addr = create_model(kernel_name,reg_params[2], degree = degree, coef0 = coef0)
					loop_saver(svm_addr)
				except:
					print(f"\t-----Exception Occured for (degree= {degree},coeff = {coef0})--------")
					exceptions.append((degree,coef0))

def loop_saver(svm_addr):
	for abstraction in abstractions:
		for perturbation in perturbations:
			run_saver(svm_addr,abstraction,perturbation)

def get_avg(rawPath):
	kernal = "poly"
	file1 = open(rawPath,"r+") 
	lines = file1.readlines()
	lineNo = 0
	if kernal == "poly":
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
					print(f"{reg}	{degree}	{coef0}	  {average[0]}	{average[1]}  {average[2]}")
	if kernal == "rbf":
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
				print(f"{reg}	{gamma}  {average[0]}	{average[1]}  {average[2]}")

	print()
	file1.close()

def get_avg_complete(rawPath):
	  
	file1 = open(rawPath,"r+") 
	average = [0,0,0]
	c = 0
	for line in file1.readlines():
		line = line.split()
		for i in range(3):
			average[i] += float(line[i])
		c+=1
	for i in range(3):
		average[i] /= c
	print(f"AVERAGE RESULT :\n Accuracy: {average[0]}	Balanced Accuracy: {average[1]}	Robustnedd: {average[2]}")

	print()
	file1.close()

def get_feature_score(dataDirPath):
	fileR = open(f"{dataDirPath}/{data_folder}-feature_score_raw.txt","r+")
	fileW = open(f"{dataDirPath}/{data_folder}-feature_analysis.txt","w+")
	with open(dataDirPath+"/dataset/columns.csv", 'r') as f:
		columns = [line for line in csv.reader(f)][0]
	
	rawdata = fileR.readlines()
	pos = 0
	for kernal in kernel_types:
		#for reg_param in reg_params:
		if 'linear' == kernal:
				fileW.write(f"\n\n\n\nSVM Type: Linear; Reg. Param: {reg_params[0]}\n")
				weights = rawdata[pos].split()
				feature_score = dict()
				pos += 1
				for col_i in range(1,len(columns)):
					feature_score[columns[col_i]] = weights[col_i]
				fileW.write(f"{dict(sorted(feature_score.items(), key = lambda kv:abs(float(kv[1]))))} \n")
		if 'poly' == kernal:
			for degree in degrees:
				for coef0 in coef0s:
					fileW.write(f"\n\n\n\nSVM Type: POLY; Reg. Param: {reg_params[2]}; degree: {degree}; coef0: {coef0}\n")
					weights = rawdata[pos].split()
					pos += 1
					for col_i in range(1,len(columns)):
						feature_score[columns[col_i]] = weights[col_i]
					fileW.write(f"{dict(sorted(feature_score.items(), key = lambda kv:abs(float(kv[1]))))} \n")
		if 'rbf' == kernal:
			for gamma in gammas:
				fileW.write(f"\n\n\n\nSVM Type: RBF; Reg. Param: {reg_params[1]}; gamma:{gamma}\n")
				weights = rawdata[pos].split()
				pos += 1
				for col_i in range(1,len(columns)):
					feature_score[columns[col_i]] = weights[col_i]
				fileW.write(f"{dict(sorted(feature_score.items(), key = lambda kv:abs(float(kv[1]))))} \n")

if __name__ == '__main__':
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
		adult.adult_adversarial_region.execute()
	if(data_folder == "compas"):
		compas.compas_adversarial_region.execute()
	if(data_folder == "crime"):
		crime.crime_adversarial_region.execute()
	if(data_folder == "german"):
		german.german_adversarial_region.execute()
	if(data_folder == "health"):
		health.health_adversarial_region.execute()
	
	for kernal in kernel_types:
		loop_model(kernal)

	dest = shutil.move("../saver/result1.txt", f"./{data_folder}/{data_folder}-results.txt") #shutil.move(source, destination) 
	dest = shutil.move("../saver/result_raw.txt", f"./{data_folder}/{data_folder}-results_raw.txt")
	dest = shutil.move("../saver/feature_score_raw.txt", f"./{data_folder}/{data_folder}-feature_score_raw.txt")

	if('top' in perturbations):
		get_feature_score(f"./{data_folder}")
	get_avg_complete(f"./{data_folder}/{data_folder}-results_raw.txt")



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
#reg_params = [1]
#gammas = [0.01,0.001,0.0001,0.00001]
#degrees = [3,9,15,20]
#coef0 = 0


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