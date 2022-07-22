import exec

print("\n\n*** DO NOT EXECUTE TWO SCRIPTS ON PARALLEL ***\n\n")

get_CE = 0

while(True):
	print(" 1) RBF \n 2) Poly \n 3) Linear")
	kernel_types = []
	ch= int(input("Enter choice: "))
	
	print(" 1) Adult \n 2) Compas \n 3) Crime \n 4) German \n 5) Health 6) Exit")
	choice = int(input("Enter choice: "))
	
	if(ch == 1):
		kernel_types = ['rbf']
	if(ch == 2):
		kernel_types = ['poly']
	if(ch == 3):
		kernel_types = ['linear']

	if(choice == 1):
		data_folder = "adult"
		reg_params = [1,0.05,0.01] #for linear rbf and poly respectively
		gammas = [0.01]
		degrees = [3]
		coef0s =  [3]
		abstractions = ['raf']
		perturbations = []
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,get_CE = get_CE, ifmlx = True)
	
	if(choice == 2):
		data_folder = "compas"
		reg_params = [1,0.05,0.01]
		gammas = [0.03]
		degrees = [3]
		coef0s =  [3]
		abstractions = ['raf']
		perturbations = []
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,get_CE = get_CE, ifmlx = True)
	
	if(choice == 3):
		data_folder = "crime"
		reg_params = [1,1,1]
		gammas = [0.01]
		degrees = [3]
		coef0s = [0]
		abstractions = ['raf']
		perturbations = []
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,get_CE = get_CE, ifmlx = True)
	
	if(choice == 4):
		data_folder = "german"
		reg_params = [1,10,0.01]
		gammas = [0.03]
		degrees = [6]
		coef0s =  [6]
		abstractions = ['raf']
		perturbations = []
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,get_CE = get_CE, ifmlx = True)
	
	if(choice == 5):
		data_folder = "health"
		reg_params = [0.01,0.1,0.1]
		gammas = [0.01]
		degrees = [3]
		coef0s =  [0.01]
		abstractions = ['raf']
		perturbations = []
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,get_CE = get_CE, ifmlx = True)

	if(choice == 6):
		data_folder = ""
		break

	if not (data_folder == ""):
		print(f"\n\n\n OUTPUT LOCATION: \n" +
			f"1) Check ./{data_folder}/{data_folder}-feature_analysis.txt for feature grades" +
		 	"for each SVM. Cummulative feature grades over particular or all kernel at the bottom of the file\n")
