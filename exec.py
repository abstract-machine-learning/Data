import subprocess
import os
import shutil
import dataset_mapper
import classifier_mapper
import svm
import crime.crime_adversarial_region
import adult.adult_adversarial_region
import compas.compas_adversarial_region
import german.german_adversarial_region
import health.health_adversarial_region

data_folder = "health"	
training_name = "dataset/training-set.csv"
test_name = "dataset/test-set.csv"
adversarial_name = "adversarial-region.dat"

svm_loc = "./domains/{data_folder}/model/"

def test_SVM(model):
	from sklearn import metrics
	dataset_path = f"./{data_folder}/{test_name}"
	dataset_mapper1 = dataset_mapper.DatasetMapper()
	x, y = dataset_mapper1.read(dataset_path)
	y_pred = model.predict(x)
	print("Accuracy:",metrics.accuracy_score(y, y_pred))
	print("Balanced Accuracy:",metrics.balanced_accuracy_score(y, y_pred))


def create_model(kernel_name,reg_param = 1,gamma = 1,degree = 1, coef0 = 0.01):	
	
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
	
	print(f"Start Analysis")
	print(f"bin/saver {rel_svm_loc} {rel_dataset_loc} {abstraction} from_file {perturbation_file} {tier_file} {is_binary}")
	s = subprocess.check_call(f"bin/saver {rel_svm_loc} {rel_dataset_loc} {abstraction} from_file {perturbation_file} {tier_file} {is_binary}", shell = True)
	os.chdir(f"../Data/")
	print(f"Finished Analysis")

#svm_addr = create_model()
#print(f"SVM created: {svm_addr}")
#run_saver(svm_addr)



def loop_model(kernel_name):
	#kernel_names = ['linear', 'poly', 'rbf']
	reg_params =[0.1]
	gammas = [0.01,0.001,0.0001,0.00001]
	degrees = [3,9,15,20]

	for reg in reg_params:
		#for kernel_name in kernel_names:
		if kernel_name == 'linear':
			svm_addr = create_model(kernel_name,reg)
			loop_saver(svm_addr)
		
		if kernel_name == 'rbf':
			for gamma in gammas:
				if(kernel_name == 'rbf' and gamma == 1):
					continue # already calculated
				svm_addr = create_model(kernel_name,reg, gamma = gamma)
				loop_saver(svm_addr)
		
		if kernel_name == 'poly':
			for degree in degrees:
				svm_addr = create_model(kernel_name,reg, degree = degree)
				loop_saver(svm_addr)

def loop_saver(svm_addr):
	abstractions = ["interval", "raf","hybrid"]
	perturbations = ["cat", "noisecat","noise"]

	for abstraction in abstractions:
		for perturbation in perturbations:
			run_saver(svm_addr,abstraction,perturbation)

def get_avg(rawPath):
	  
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

if __name__ == '__main__':
	os.system('rm ../saver/result1.txt')
	os.system('rm ../saver/result_raw.txt')
	os.system('touch ../saver/result1.txt')
	os.system('touch ../saver/result_raw.txt')
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
	
	loop_model('linear')
	loop_model('rbf')
	loop_model('poly')
	

	#loop_saver("./adult/model/./svm_rbf_g1_d1_c0_C1.dat")
	#svm_addr = create_model('rbf',1)

	dest = shutil.move("../saver/result1.txt", f"./{data_folder}/{data_folder}-results.txt") #shutil.move(source, destination) 
	dest = shutil.move("../saver/result_raw.txt", f"./{data_folder}/{data_folder}-results_raw.txt")

	get_avg(f"./{data_folder}/{data_folder}-results_raw.txt")



#if __name__ == '__main__':
#	loop_model('linear')
#	#loop_model('rbf')
#	#loop_model('poly')



#-----German------
#reg_params = [15]
#gammas = [0.01,0.001,0.0001,0.00001]
#degrees = [3,9,15,20]
#coef0 = 40
#-----------------

#-----Crime------
#reg_params = [3]
#gammas = [0.01,0.001,0.0001,0.00001]
#degrees = [3,9,15,20]
#coef0 = 40
#-----------------

#-----Crime------
#reg_params = [1]
#gammas = [0.01,0.001,0.0001,0.00001]
#degrees = [3,9,15,20]
#coef0 = 0
#-----Crime------


#-----Health------
#reg_params = [0.1]

#-----Crime------