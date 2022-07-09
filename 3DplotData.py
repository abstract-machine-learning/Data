import exec

data_folder = "crime"
print("\n\n*** DO NOT EXECUTE TWO SCRIPTS IN PARALLEL ***\n\n")

print(" 1) Poly Plot Data \n 2) RBF Plot Data")
choice = int(input("Enter choice: "))
if(choice == 1):
	reg_params = [1]
	gammas = []
	degrees = [3,6,9,12]
	coef0s =  [3,6,9,12,15]
	abstractions = ['raf']
	perturbations = ["noisecat"]
	kernel_types = ['poly']
	exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 2,get_avg_bool = True, is_OH = 1, get_CE = 0, if_part = 0)
if(choice == 2):
	reg_params = [0.4,0.8,1.2,1.4,1.6]
	gammas = [0.0001,0.0006,0.0011,0.0016,0.0021]
	degrees = []
	coef0s =  []
	abstractions = ['raf']
	perturbations = ["noisecat"]
	kernel_types = ['rbf']
	exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 2,get_avg_bool = True, is_OH = 1, get_CE = 0, if_part = 0)