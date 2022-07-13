import exec

print("\n\n*** DO NOT EXECUTE TWO SCRIPTS ON PARALLEL ***\n\n")

print(" 1) Numerical Features \n 2) Categorical Features")
choice1 = int(input("Enter choice: "))

print(" 1) german \n 2) adult 3) Compas")
choice = int(input("Enter choice: "))

if(choice == 1):
	print(" 1) Linear \n 2) RBF \n 3) Poly")
	choice2 = int(input("Enter choice: "))
	
	print(" 1) LB \n 2) UB")
	get_CE = 1 if (int(input("Enter choice: ")) == 2) else 0
	
	data_folder = "german"
	reg_params = [1,10,0.01]
	gammas = [0.03]
	degrees = [6]
	coef0s =  [6]
	abstractions = ['raf']
	perturbations = ['noise'] if ( choice1 == 1) else ['cat'] 
	#featuresRBFNoise = [['residence_since'],  ['telephone_A192'], ['people_liable_for'], ['number_of_credits'], ['foreign_worker_A202'], ['age'], ['investment_as_income_percentage'], ['credit_amount'], ['months']]
	#featuresPolyNoise = [['people_liable_for'], ['telephone_A192'], ['foreign_worker_A202'], ['number_of_credits'],['residence_since'], ['investment_as_income_percentage'], ['credit_amount'], ['age'], ['months']]
	#featuresLinearNoise = [['people_liable_for'], ['residence_since'],  ['telephone_A192'], ['investment_as_income_percentage'],  ['foreign_worker_A202'], ['number_of_credits'], ['months'], ['age'], ['credit_amount']]
	#
	#featuresRBFCat = []
	#featuresPolyCat = [['sex_male'], ['status'], ['credit_history'], ['purpose'], ['savings'], ['employment'], ['other_debtors'], ['property'], ['installment_plans'], ['housing'], ['skill_level']]
	#featuresLinearCat = [ ['sex_male'], ['housing'], ['installment_plans'], ['skill_level'],['property'], ['other_debtors'], ['employment'], ['savings'], ['status'], ['purpose'], ['credit_history'] ]
	
	ScoreLinear = {'people_liable_for': 0.012609, 'telephone_A192': 0.032334, 'residence_since': 0.034245, 'sex_male': 0.117577, 'housing=A151': 0.194178, 'installment_plans=A141': 0.206695, 'skill_level=A171': 0.238366, 'investment_as_income_percentage': 0.279244, 'property=A121': 0.288805, 'foreign_worker_A202': 0.303454, 'other_debtors=A101': 0.30931, 'employment=A71': 0.312765, 'number_of_credits': 0.336012, 'savings=A61': 0.380627, 'months': 0.511288, 'age': 0.549109, 'status=A11': 0.583695, 'purpose=A40': 0.715379, 'credit_amount': 0.736313, 'credit_history=A30': 0.774001} 
	ScorePoly = {'telephone_A192': 0.039285, 'sex_male': 0.043084, 'people_liable_for': 0.054234, 'foreign_worker_A202': 0.211242, 'residence_since': 0.228259, 'status=A11': 0.228712, 'credit_history=A30': 0.228712, 'purpose=A40': 0.228712, 'savings=A61': 0.228712, 'employment=A71': 0.228712, 'other_debtors=A101': 0.228712, 'property=A121': 0.228712, 'installment_plans=A141': 0.228712, 'housing=A151': 0.228712, 'skill_level=A171': 0.228712, 'investment_as_income_percentage': 0.300098, 'number_of_credits': 0.323626, 'age': 0.373859, 'credit_amount': 0.397331, 'months': 0.551782} 
	ScoreRBF = {'residence_since': 0.019464, 'status=A11': 0.024455, 'credit_history=A30': 0.024455, 'purpose=A40': 0.024455, 'savings=A61': 0.024455, 'employment=A71': 0.024455, 'other_debtors=A101': 0.024455, 'property=A121': 0.024455, 'installment_plans=A141': 0.024455, 'housing=A151': 0.024455, 'skill_level=A171': 0.024455, 'sex_male': 0.035808, 'people_liable_for': 0.086637, 'telephone_A192': 0.10342, 'number_of_credits': 0.196492, 'investment_as_income_percentage': 0.29048, 'foreign_worker_A202': 0.313735, 'age': 0.368907, 'credit_amount': 0.445705, 'months': 0.459506} 
	
	
	if choice2 == 1:
		kernel_types = ['linear']
		#features = featuresLinearNoise if ( choice1 == 1) else featuresLinearCat
		Score = ScoreLinear
	if choice2 == 2:
		kernel_types = ['rbf']
		#features = featuresRBFNoise if ( choice1 == 1) else featuresRBFCat
		Score = ScoreRBF
	if choice2 == 3:
		kernel_types = ['poly']
		#features = featuresPolyNoise if ( choice1 == 1) else featuresPolyCat
		Score = ScorePoly
	
	for feat in Score.keys():
		if( ("=" not in feat and feat != 'sex_male') and choice1 == 1):
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n") 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat])
		if( ("=" in feat or feat == 'sex_male') and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat])

if(choice == 2):
	print(" 1) Linear \n 2) RBF \n 3) Poly")
	choice2 = int(input("Enter choice: "))
	
	print(" 1) LB \n 2) UB")
	get_CE = 1 if (int(input("Enter choice: ")) == 2) else 0
	
	data_folder = "adult"
	reg_params = [1,0.05,0.01] #for linear rbf and poly respectively
	gammas = [0.03]
	degrees = [3]
	coef0s =  [3]
	abstractions = ['raf']
	perturbations = ['noise'] if ( choice1 == 1) else ['cat'] 
	
	ScoreLinear = {'fnlwgt': 0.024315, 'age': 0.07576, 'capital_loss': 0.082618, 'hours_per_week': 0.104416, 'sex_male': 0.212629, 'race=amer_indian_eskimo': 0.236754, 'education_num': 0.240729, 'workclass=federal_gov': 0.407883, 'marital_status=divorced': 0.635387, 'relationship=husband': 0.655684, 'education=10th': 0.801337, 'capital_gain': 0.905834, 'occupation=adm_clerical': 0.911317, 'native_country=cambodia': 1.040589} 
	ScorePoly = {'capital_loss': 0.059535, 'sex_male': 0.325648, 'hours_per_week': 0.368317, 'age': 0.425033, 'workclass=federal_gov': 0.444059, 'education=10th': 0.444059, 'marital_status=divorced': 0.444059, 'occupation=adm_clerical': 0.444059, 'relationship=husband': 0.444059, 'race=amer_indian_eskimo': 0.444059, 'native_country=cambodia': 0.444059, 'education_num': 0.485843, 'fnlwgt': 1.402729, 'capital_gain': 1.474939} 
	ScoreRBF = {'workclass=federal_gov': 0.005304, 'education=10th': 0.005304, 'marital_status=divorced': 0.005304, 'occupation=adm_clerical': 0.005304, 'relationship=husband': 0.005304, 'race=amer_indian_eskimo': 0.005304, 'native_country=cambodia': 0.005304, 'capital_loss': 0.022981, 'fnlwgt': 0.02504, 'hours_per_week': 0.082677, 'age': 0.083364, 'sex_male': 0.083925, 'education_num': 0.206012, 'capital_gain': 0.515228} 

	
	if choice2 == 1:
		kernel_types = ['linear']
		Score = ScoreLinear
	if choice2 == 2:
		kernel_types = ['rbf']
		Score = ScoreRBF
	if choice2 == 3:
		kernel_types = ['poly']
		Score = ScorePoly
	
	for feat in Score.keys():
		if( ("=" not in feat and feat != 'sex_male') and choice1 == 1):
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n") 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat])
		if( ("=" in feat or feat == 'sex_male') and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat])



if(choice == 3):
	print(" 1) Linear \n 2) RBF \n 3) Poly")
	choice2 = int(input("Enter choice: "))
	
	print(" 1) LB \n 2) UB")
	get_CE = 1 if (int(input("Enter choice: ")) == 2) else 0
	
	data_folder = "compas"
	reg_params = [1,0.05,0.01]
	gammas = [0.03]#[0.01,0.03,0.05,0.07,0.09]
	degrees = [3]
	coef0s =  [3]#list(range(0,16,3))[1:]
	abstractions = ['raf']
	perturbations = ['noise'] if ( choice1 == 1) else ['cat'] 
	
	ScoreLinear = {'juv_fel_count': 0.006952, 'race_caucasian': 0.009066, 'diff_jail': 0.031645, 'sex_male': 0.080678, 'diff_custody': 0.087368, 'age': 0.105114, 'c_charge_degree_m': 0.115079, 'v_score_text': 0.219388, 'priors_count': 0.345174, 'c_charge_desc=abuse_without_great_harm': 1.850682}  
	ScorePoly = {'juv_fel_count': 0.015534, 'sex_male': 0.023331, 'priors_count': 0.101191, 'v_score_text': 0.112393, 'age': 0.113156, 'c_charge_desc=abuse_without_great_harm': 0.127739, 'c_charge_degree_m': 0.176032, 'race_caucasian': 0.33039, 'diff_jail': 0.359672, 'diff_custody': 0.54946} 
	ScoreRBF = {'c_charge_desc=abuse_without_great_harm': 0.014228, 'juv_fel_count': 0.016883, 'race_caucasian': 0.026203, 'c_charge_degree_m': 0.029751, 'diff_jail': 0.04002, 'sex_male': 0.041855, 'age': 0.101345, 'diff_custody': 0.125053, 'v_score_text': 0.232232, 'priors_count': 0.287674} 

	
	if choice2 == 1:
		kernel_types = ['linear']
		Score = ScoreLinear
	if choice2 == 2:
		kernel_types = ['rbf']
		Score = ScoreRBF
	if choice2 == 3:
		kernel_types = ['poly']
		Score = ScorePoly
	
	for feat in Score.keys():
		if( ("=" not in feat and feat not in ['race_caucasian','sex_male']) and choice1 == 1):
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n") 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat])
		if( ("=" in feat or feat in ['race_caucasian','sex_male']) and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat])
