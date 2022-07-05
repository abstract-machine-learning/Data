import exec

datasets = ["adult","compas","crime","german","health"]
kernels =   ['linear','rbf','poly']
perturbations = ["top [for Ranking]","cat", "noisecat","noise"]

for i in range(len(datasets)):
	print(f"{i}) {datasets[i]}")
dataset_id = int(input("Pick a dataset ID from above choices: "))

for i in range(len(kernels)):
	print(f"{i}) {kernels[i]}")
kernel_id = int(input("Pick a Kernel ID from above choices: "))

for i in range(len(perturbations)):
	print(f"{i}) {perturbations[i]}")
perturbation_id = int(input("Pick a Perturbation ID from above choices: "))

reg = float(input("Input Regularization Parameter: "))

if(kernels[kernel_id] == "linear"):
	svm_addr = create_model("linear",reg)
	loop_saver(svm_addr)

if(kernels[kernel_id] == "rbf"):
	gamma = float(input("Enter Gamma: "))
	svm_addr = create_model("rbf",reg, gamma = gamma)
	loop_saver(svm_addr)

if(kernels[kernel_id] == "poly"):
	degree = float(input("Enter Degree: "))
	coef0 = float(input("Enter Coefficent: "))
	try:
		svm_addr = create_model("poly",reg, degree = degree, coef0 = coef0)
		loop_saver(svm_addr)
	except:
		print(f"\t-----Exception Occured for (degree= {degree},coeff = {coef0})--------")





comment1 = "Obtain 3D plot Poly; Run saver on RAF OH noisecat perturbations; with degree= [3,6,9,12] and coeff0 = [3,6,9,12,15] with reg param = 1"

comment2 = "Obtain 3D plot RBF;  Run saver on RAF OH noisecat perturbations; with reg. parm = [0.4,0.6,0.8,1.2,1.4] and coeff0 = [0.0001,0.0006,0.0011,0.0016,0.0021]"


comment4 = "Obtain box plot all dataset: For each dataset consider the set of input present at bottom of exec.py and find the box plot of resulting vlaues."