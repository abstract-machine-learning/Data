import exec

print("\n\n\t\t*** DO NOT EXECUTE TWO SCRIPTS IN PARALLEL ***\n\n")


def execute(kernel_name,reg_params):
	print(" 1) Interval \n 2) Interval with OH \n 3) RAF \n 4) RAF with OH \n 5) EXIT")
	choice = int(input("Enter choice: "))
	data_folder = "crime"
	gammas = [0.1,0.01,0.001,0.0001,0.00005]
	degrees = [3,6,9,12]
	coef0s =  [3,6,9,12,15]
	perturbations = ["noisecat"]
	kernel_types = [kernel_name]

	if(choice == 1):
		abstractions = ['interval']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 2,get_avg_bool = True, is_OH = 0, get_CE = 0, if_part = 0,plot = 'boxplotCrime')
	
	elif(choice == 2):
		abstractions = ['interval']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 2,get_avg_bool = True, is_OH = 1, get_CE = 0, if_part = 0,plot = 'boxplotCrime')
	
	elif(choice == 3):
		abstractions = ['raf']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 2,get_avg_bool = True,is_OH = 0, get_CE = 0, if_part = 0,plot = 'boxplotCrime')
	
	elif(choice == 4):
		abstractions = ['raf']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 2,get_avg_bool = True,is_OH = 1, get_CE = 0, if_part = 0,plot = 'boxplotCrime')
	
	elif(choice == 5):
		print("\nThank you\n")
		return data_folder,True
	else:
		print("\nInvalid Choice\n")
	return data_folder,False

def outputLocPrint(data_folder):
	print(f"\n\n\n OUTPUT LOCATION: \n" +
		f"1) Observe the Robustness UB values from the output\n" +
		f"2) Also saved at ./{data_folder}/{data_folder}-results.txt\n"+
		f"3) Check ./{data_folder}/{data_folder}-results_raw.txt for summary where\n" + 
		"the coloums are in the order Accuracy, Balanced Accuracy and Robutness\n")


print(" 1) Linear  2) Poly 3) RBF ")
choice = int(input("Enter choice: "))

if(choice == 1):
	while(True):
		reg_params = [0.1,0.01,0.001,0.0001]
		data_folder,ifExit = execute('linear',reg_params)
		if(ifExit):
	 		break
		outputLocPrint(data_folder)

elif(choice == 2):
	while(True):
		reg_params = [1]
		data_folder,ifExit = execute('poly',reg_params)
		if(ifExit):
	 		break
		outputLocPrint(data_folder)

elif(choice == 3):
	while(True):
		reg_params = [10,3,0.3]
		data_folder,ifExit = execute('rbf',reg_params)
		if(ifExit):
	 		break
		outputLocPrint(data_folder)

else:
	print("\nInvalid Choice\n")
