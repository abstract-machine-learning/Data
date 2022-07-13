import exec

print("\n\n\t\t*** DO NOT EXECUTE TWO SCRIPTS IN PARALLEL ***\n\n")


def execute():
	print(" 1) Adult \n 2) Compas \n 3) Crime \n 4) German \n 5) Health \n 6) EXIT")
	choice = int(input("Enter choice: "))
	data_folders = ["","adult","compas","crime","german","health"]
	data_folder = ""
	if (choice > 0 and choice < 6):
		data_folder = data_folders[choice]
		reg_params = [1]
		gammas = []
		degrees = []
		coef0s =  []
		abstractions = ['raf']
		perturbations = ["cat","noisecat","noise"]
		kernel_types = ['linear']
		exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1,get_avg_bool = False, is_OH = 1, get_CE = 0, if_part = 0,if_print_raw=True)
	elif(choice == 6):
		print("\nThank you\n")
		return data_folder,True
	else:
		print("\nInvalid Choice\n")
	return data_folder,False


while(True):
	data_folder,ifExit = execute()
	if(ifExit):
 		break
	print(f"\n\n\n OUTPUT LOCATION: \n" +
		f"1) Observe the Acc. Bal. Acc. and Robustness LB values from the output\n" +
		f"2) Read the table and the paths above it for options\n"
		f"3) Also saved at ./{data_folder}/{data_folder}-results.txt\n")
