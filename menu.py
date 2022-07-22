import exec

datasets = ["adult","compas","crime","german","health"]
kernels =   ['linear','rbf','poly']
perturbations = ["top [for Ranking]","cat", "noisecat","noise"]
abstractions1 = ['interval']
abstractions2 = ['raf']

for i in range(len(datasets)):
	print(f"{i}) {datasets[i]}")
dataset_id = int(input("Pick a dataset ID from above choices: "))

for i in range(len(kernels)):
	print(f"{i}) {kernels[i]}")
kernel_id = int(input("Pick a Kernel ID from above choices: "))
kernel_types = [kernels[kernel_id]]

perturbations = ['cat','noisecat','noise']

reg = float(input("Input Regularization Parameter: "))
gammas,degrees,coef0s = [], [], [];
reg_params = [reg]

if(kernels[kernel_id] == "linear"):
	pass

if(kernels[kernel_id] == "rbf"):
	gammas = [float(input("Enter Gamma: "))]


if(kernels[kernel_id] == "poly"):
	degrees = [float(input("Enter Degree: "))]
	coef0s = [float(input("Enter Coefficent: "))]

# Without OH
exec.caller(datasets[dataset_id],reg_params,gammas,degrees,coef0s,abstractions1,perturbations,kernel_types,regType = 2,get_avg_bool= False,is_OH = 0,get_CE = 0,if_part = 0,if_print_raw= False,plot = 'None',PerturbFeature = [], epsilon = 0.05, ifmlx = False)

# With OH
exec.caller(datasets[dataset_id],reg_params,gammas,degrees,coef0s,abstractions1,perturbations,kernel_types,regType = 2,get_avg_bool= False,is_OH = 1,get_CE = 0,if_part = 0,if_print_raw= False,plot = 'None',PerturbFeature = [], epsilon = 0.05, ifmlx = False)

# Without OH
exec.caller(datasets[dataset_id],reg_params,gammas,degrees,coef0s,abstractions2,perturbations,kernel_types,regType = 2,get_avg_bool= False,is_OH = 0,get_CE = 0,if_part = 0,if_print_raw= False,plot = 'None',PerturbFeature = [], epsilon = 0.05, ifmlx = False)

# With OH
exec.caller(datasets[dataset_id],reg_params,gammas,degrees,coef0s,abstractions2,perturbations,kernel_types,regType = 2,get_avg_bool= False,is_OH = 1,get_CE = 0,if_part = 0,if_print_raw= False,plot = 'None',PerturbFeature = [], epsilon = 0.05, ifmlx = False)


print(f"\n\n\n OUTPUT LOCATION: \n" +
	f"1) Observe the Robustness LB values from the output. \n" +
	f" They are in the same order as in the table \n" +
	f"2) Acc. and B. Acc. are same for all as its the same SVM \n" +
	
	f"4) Also saved at ./{data_folder}/{data_folder}-results.txt \n")
