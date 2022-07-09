import exec

print("\n\n\t\t*** DO NOT EXECUTE TWO SCRIPTS IN PARALLEL ***\n\n")


def execute(UBorLB):
	print(" 1) Adult \n 2) Compas \n 3) Crime \n 4) German \n 5) Health \n 6) EXIT")
	choice = int(input("Enter choice: "))
	data_folder = ""
	get_CE = 1 if UBorLB == 2 else 0;
	if(choice == 1):
		data_folder = "adult"
		reg_params = [1,0.05,0.01] #for linear rbf and poly respectively
		gammas = [0.05]
		degrees = [3]
		coef0s =  [3]
		abstractions = ['raf']
		perturbations = ["noisecat"]
		kernel_types = ['linear','rbf','poly']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False, is_OH = 1, get_CE = get_CE, if_part = 0)
	
	elif(choice == 2):
		data_folder = "compas"
		reg_params = [1,0.05,0.01]
		gammas = [0.01]
		degrees = [3]
		coef0s =  [3]
		abstractions = ['raf']
		perturbations = ["noisecat"]
		kernel_types = ['linear','rbf','poly']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,is_OH = 1, get_CE = get_CE, if_part = 0)
	
	elif(choice == 3):
		data_folder = "crime"
		reg_params = [1,1,1]
		gammas = [0.0001]
		degrees = [9]
		coef0s = [0]
		abstractions = ['raf']
		perturbations = ["noisecat"]
		kernel_types = ['linear','rbf','poly']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,is_OH = 1, get_CE = get_CE, if_part = 0)
	
	elif(choice == 4):
		data_folder = "german"
		reg_params = [1,10,0.01]#[1,10,0.01]
		gammas = [0.05]
		degrees = [6]
		coef0s =  [6]
		abstractions = ['raf']
		perturbations = ["noisecat"]
		kernel_types = ['linear','rbf','poly']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,is_OH = 1, get_CE = get_CE, if_part = 0)
	
	elif(choice == 5):
		data_folder = "health"
		reg_params = [0.01,0.1,0.1]
		gammas = [0.01]
		degrees = [3]
		coef0s =  [0.01]
		abstractions = ['raf']
		perturbations = ["noisecat"]
		kernel_types = ['linear','rbf','poly']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False,is_OH = 1, get_CE = get_CE, if_part = 0)
	elif(choice == 6):
		print("\nThank you\n")
		return data_folder,True
	else:
		print("\nInvalid Choice\n")
	return data_folder,False




print("As explained in the paper LB and UB are found using alternative\n"
 + "implementation of RAF-OH though output will contain both LB and UB in each\n"
 +  "case. Observe the one the execution is for for stricter upper/lower bound.")
print(" 1) LB  2) UB ")
choice = int(input("Enter choice: "))

if(choice == 1):
	while(True):
		data_folder,ifExit = execute(choice)
		if(ifExit):
	 		break
		print(f"\n\n\n OUTPUT LOCATION: \n" +
			f"1) Observe the Robustness LB values from the output\n" +
			f"2) Also saved at ./{data_folder}/{data_folder}-results.txt\n")

elif(choice == 2):
	while(True):
		data_folder,ifExit = execute(choice)
		if(ifExit):
	 		break
		print(f"\n\n\n OUTPUT LOCATION: \n" +
			f"1) Observe the Robustness UB values from the output\n" +
			f"2) Also saved at ./{data_folder}/{data_folder}-results.txt\n")
else:
	print("\nInvalid Choice\n")
