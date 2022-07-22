import exec

print("\n\n*** DO NOT EXECUTE TWO SCRIPTS ON PARALLEL ***\n\n")

print(" 1) Numerical Features \n 2) Categorical Features")
choice1 = int(input("Enter choice: "))

print(" 1) German \n 2) Adult \n 3) Compas \n 4) Crime \n 5) Health")
choice = int(input("Enter choice: "))

epsilon = 0.3
if (choice1 == 1):
	epsilon = float(input("Pertubation (epsilon) [Check from table] : "))

if(choice == 1): # German
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
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon, ifmlx = True)
		if( ("=" in feat or feat == 'sex_male') and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)

if(choice == 2): # Adult
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
	ScoreRBF = {'workclass=federal_gov': 0.005304, 'education=10th': 0.005304, 'marital_status=divorced': 0.005304, 'occupation=adm_clerical': 0.005304, 'relationship=husband': 0.005304, 'race=amer_indian_eskimo': 0.005304, 'native_country=cambodia': 0.005304, 'capital_loss': 0.022981, 'fnlwgt': 0.02504, 'hours_per_week': 0.082677, 'age': 0.083364, 'sex_male': 0.083925, 'education_num': 0.206012, 'capital_gain': 0.515228} 
	ScorePoly = {'capital_loss': 0.059535, 'sex_male': 0.325648, 'hours_per_week': 0.368317, 'age': 0.425033, 'workclass=federal_gov': 0.444059, 'education=10th': 0.444059, 'marital_status=divorced': 0.444059, 'occupation=adm_clerical': 0.444059, 'relationship=husband': 0.444059, 'race=amer_indian_eskimo': 0.444059, 'native_country=cambodia': 0.444059, 'education_num': 0.485843, 'fnlwgt': 1.402729, 'capital_gain': 1.474939} 

	
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
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)
		if( ("=" in feat or feat == 'sex_male') and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)



if(choice == 3): # Compas
	print(" 1) Linear \n 2) RBF \n 3) Poly")
	choice2 = int(input("Enter choice: "))
	
	print(" 1) LB \n 2) UB")
	get_CE = 1 if (int(input("Enter choice: ")) == 2) else 0
	
	data_folder = "compas"
	reg_params = [1,0.05,0.01]
	gammas = [0.03]
	degrees = [3]
	coef0s =  [3]
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
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)
		if( ("=" in feat or feat in ['race_caucasian','sex_male']) and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)


if(choice == 4): # Crime
	print(" 1) Linear \n 2) RBF \n 3) Poly")
	choice2 = int(input("Enter choice: "))
	
	print(" 1) LB \n 2) UB")
	get_CE = 1 if (int(input("Enter choice: ")) == 2) else 0
	
	data_folder = "crime"
	reg_params = [1,1,1]
	gammas = [0.01]
	degrees = [3]
	coef0s = [0]
	abstractions = ['raf']
	perturbations = ['noise'] if ( choice1 == 1) else ['cat'] 
	
	ScoreLinear = {'med_own_cost_pct_inc_no_mtg': 0.004108, 'med_own_cost_pct_inc': 0.008103, 'race_pct_asian': 0.009453, 'pct_same_city85': 0.010753, 'pct_hous_occup': 0.013564, 'med_rent': 0.014094, 'pct_not_hs_grad': 0.016294, 'pct_immig_rec5': 0.017592, 'rent_high_q': 0.017959, 'pct_larg_house_fam': 0.02211, 'num_kids_born_never_mar': 0.022396, 'med_numbr': 0.026667, 'pop_dens': 0.027855, 'land_area': 0.027978, 'pct_immig_recent': 0.033636, 'pct_teen2par': 0.035377, 'age_pct_65up': 0.036846, 'pct_hous_less3br': 0.03819, 'pct_empl_manu': 0.038193, 'asian_per_cap': 0.039368, 'indian_per_cap': 0.041532, 'own_occ_qrange': 0.04411, 'pct_work_mom_young_kids': 0.045833, 'pct_immig_rec8': 0.046772, 'pct_urban': 0.050172, 'black_per_cap': 0.050517, 'pct_wo_full_plumb': 0.050675, 'pct_foreign_born': 0.054729, 'pct_w_retire': 0.05666, 'pct_vacant_boarded': 0.0576, 'num_in_shelters': 0.058712, 'householdsize': 0.058782, 'rent_median': 0.062057, 'pct_hous_own_occ': 0.065367, 'pct_unemployed': 0.066621, 'pct_w_farm_self': 0.068307, 'pct_w_inv_inc': 0.069124, 'pct_empl_profserv': 0.072146, 'pct_same_state85': 0.072505, 'pct_immig_rec10': 0.075479, 'hisp_per_cap': 0.077337, 'pct_young_kids2par': 0.077517, 'pct_pop_under_pov': 0.084, 'pct_hous_no_phone': 0.088226, 'pers_per_rent_occ_hous': 0.089379, 'pct_w_soc_sec': 0.093033, 'pct_w_wage': 0.093796, 'pct_occup_mgmt_prof': 0.097359, 'race_pct_white': 0.098553, 'pct_pers_own_occup': 0.101753, 'pct_kids_born_never_mar': 0.102099, 'rent_low_q': 0.104254, 'pct_vac_more6mos': 0.104375, 'pers_per_fam': 0.106193, 'med_yr_hous_built': 0.107339, 'pct_occup_manu': 0.107658, 'pct_use_pub_trans': 0.109144, 'pct_same_house85': 0.113064, 'lemas_pct_offic_drug_un': 0.114285, 'pct_w_pub_asst': 0.126199, 'num_immig': 0.130692, 'numb_urban': 0.131455, 'rent_qrange': 0.133857, 'pct_born_same_state': 0.138889, 'age_pct_12t29': 0.139482, 'pct_speak_engl_only': 0.139523, 'med_rent_pct_hous_inc': 0.141884, 'pct_employ': 0.141973, 'pct_fam2par': 0.145968, 'pers_per_own_occ_hous': 0.147053, 'pct_rec_immig5': 0.151343, 'pct_recent_immig': 0.151833, 'age_pct_16t24': 0.153537, 'pct_bs_or_more': 0.160191, 'total_pct_div': 0.160575, 'race_pct_hisp': 0.160605, 'male_pct_nev_marr': 0.16171, 'age_pct_12t21': 0.16373, 'own_occ_hi_quart': 0.16589, 'racepctblack': 0.184404, 'med_income': 0.196846, 'hous_vacant': 0.197632, 'own_occ_med_val': 0.200809, 'pct_work_mom': 0.210277, 'population': 0.212269, 'pct_less9thgrade': 0.215958, 'num_street': 0.241569, 'female_pct_div': 0.269834, 'own_occ_low_quart': 0.270028, 'male_pct_divorce': 0.279513, 'pct_larg_house_occup': 0.302977, 'per_cap_inc': 0.316946, 'pct_not_speak_engl_well': 0.329044, 'num_under_pov': 0.361334, 'pct_rec_immig8': 0.364879, 'med_fam_inc': 0.397782, 'pct_rec_immig10': 0.401083, 'pers_per_occup_hous': 0.445368, 'pct_kids2par': 0.448853, 'pct_pers_dense_hous': 0.450659, 'white_per_cap': 0.45327, 'state=a_k': 1.327478} 

	ScorePoly = {'age_pct_65up': 0.00055, 'asian_per_cap': 0.000792, 'pct_larg_house_occup': 0.001073, 'pct_immig_rec10': 0.001389, 'pct_immig_rec5': 0.002352, 'pct_recent_immig': 0.002882, 'own_occ_hi_quart': 0.003178, 'pers_per_fam': 0.003514, 'pct_occup_manu': 0.003568, 'age_pct_12t29': 0.00486, 'med_numbr': 0.005247, 'pct_not_speak_engl_well': 0.005475, 'pers_per_occup_hous': 0.005475, 'pct_born_same_state': 0.005911, 'householdsize': 0.00602, 'per_cap_inc': 0.006485, 'pct_hous_own_occ': 0.00717, 'pct_w_soc_sec': 0.007287, 'state=a_k': 0.00767, 'pct_immig_rec8': 0.008241, 'pct_rec_immig5': 0.008699, 'rent_low_q': 0.009247, 'rent_median': 0.010093, 'pct_larg_house_fam': 0.010146, 'pct_immig_recent': 0.010574, 'pct_wo_full_plumb': 0.011273, 'pct_empl_manu': 0.011404, 'num_immig': 0.011436, 'pct_w_retire': 0.011727, 'own_occ_med_val': 0.012119, 'pct_work_mom_young_kids': 0.013443, 'pct_employ': 0.013463, 'pct_hous_no_phone': 0.013523, 'pct_speak_engl_only': 0.014017, 'pop_dens': 0.014062, 'num_kids_born_never_mar': 0.014316, 'race_pct_asian': 0.015412, 'age_pct_16t24': 0.015418, 'num_in_shelters': 0.016237, 'med_income': 0.017125, 'pct_use_pub_trans': 0.017361, 'pct_rec_immig10': 0.018185, 'pct_foreign_born': 0.018922, 'pct_rec_immig8': 0.020195, 'pct_w_wage': 0.020316, 'pct_vac_more6mos': 0.020556, 'hisp_per_cap': 0.021203, 'med_own_cost_pct_inc': 0.021692, 'age_pct_12t21': 0.022317, 'med_rent': 0.022782, 'num_under_pov': 0.023076, 'male_pct_nev_marr': 0.023547, 'pct_same_house85': 0.023775, 'pct_occup_mgmt_prof': 0.024815, 'rent_high_q': 0.025124, 'num_street': 0.025386, 'own_occ_low_quart': 0.026845, 'land_area': 0.027638, 'pct_bs_or_more': 0.029281, 'white_per_cap': 0.029478, 'indian_per_cap': 0.030016, 'med_fam_inc': 0.030816, 'pct_same_city85': 0.03124, 'pct_w_farm_self': 0.031651, 'numb_urban': 0.033056, 'pct_pers_own_occup': 0.033414, 'pct_same_state85': 0.033715, 'population': 0.034711, 'med_yr_hous_built': 0.036053, 'own_occ_qrange': 0.03777, 'pct_pop_under_pov': 0.042449, 'pct_unemployed': 0.045009, 'pers_per_own_occ_hous': 0.046514, 'pers_per_rent_occ_hous': 0.047425, 'hous_vacant': 0.048753, 'pct_less9thgrade': 0.049955, 'pct_young_kids2par': 0.051354, 'med_own_cost_pct_inc_no_mtg': 0.051718, 'pct_empl_profserv': 0.054938, 'pct_vacant_boarded': 0.055054, 'pct_urban': 0.055181, 'pct_hous_occup': 0.055595, 'female_pct_div': 0.056672, 'pct_not_hs_grad': 0.056797, 'pct_hous_less3br': 0.057576, 'race_pct_hisp': 0.061396, 'male_pct_divorce': 0.061641, 'total_pct_div': 0.062543, 'pct_w_pub_asst': 0.063715, 'lemas_pct_offic_drug_un': 0.066551, 'pct_pers_dense_hous': 0.06716, 'black_per_cap': 0.067389, 'pct_work_mom': 0.071911, 'rent_qrange': 0.073205, 'med_rent_pct_hous_inc': 0.081529, 'pct_teen2par': 0.093646, 'pct_w_inv_inc': 0.093655, 'pct_fam2par': 0.111026, 'pct_kids2par': 0.134257, 'racepctblack': 0.145416, 'pct_kids_born_never_mar': 0.151538, 'race_pct_white': 0.153774} 

	ScoreRBF = {'pct_hous_no_phone': 3.3*(10**(-5)), 'age_pct_12t29': 0.000349, 'age_pct_65up': 0.00112, 'own_occ_low_quart': 0.002093, 'pct_w_soc_sec': 0.0021, 'age_pct_12t21': 0.002164, 'pct_w_wage': 0.004514, 'pct_w_retire': 0.004532, 'age_pct_16t24': 0.004596, 'female_pct_div': 0.005363, 'pct_employ': 0.006783, 'med_yr_hous_built': 0.006842, 'race_pct_asian': 0.006923, 'med_fam_inc': 0.007797, 'pct_use_pub_trans': 0.007869, 'pct_not_speak_engl_well': 0.008996, 'pct_born_same_state': 0.009676, 'total_pct_div': 0.010962, 'pct_same_house85': 0.011061, 'med_income': 0.011734, 'pct_occup_manu': 0.01255, 'indian_per_cap': 0.014026, 'pers_per_own_occ_hous': 0.01473, 'num_street': 0.015765, 'own_occ_med_val': 0.016905, 'pct_speak_engl_only': 0.018445, 'per_cap_inc': 0.018766, 'rent_low_q': 0.020208, 'own_occ_hi_quart': 0.020381, 'pct_pers_own_occup': 0.021123, 'pct_immig_rec10': 0.021949, 'pct_occup_mgmt_prof': 0.022746, 'num_immig': 0.024074, 'pop_dens': 0.024182, 'pct_same_city85': 0.025211, 'med_own_cost_pct_inc_no_mtg': 0.025306, 'pct_rec_immig10': 0.025985, 'pct_foreign_born': 0.026093, 'med_own_cost_pct_inc': 0.026134, 'pct_vac_more6mos': 0.026425, 'num_kids_born_never_mar': 0.026564, 'num_in_shelters': 0.027231, 'male_pct_divorce': 0.027546, 'pct_immig_rec8': 0.028053, 'pct_hous_less3br': 0.028066, 'pct_same_state85': 0.02942, 'pct_hous_occup': 0.030318, 'pct_rec_immig5': 0.032617, 'pct_urban': 0.033038, 'householdsize': 0.03443, 'pct_bs_or_more': 0.035691, 'pct_young_kids2par': 0.037722, 'pct_recent_immig': 0.038726, 'num_under_pov': 0.039152, 'pct_wo_full_plumb': 0.040028, 'pct_less9thgrade': 0.042979, 'pct_empl_manu': 0.044145, 'pct_rec_immig8': 0.044742, 'pct_larg_house_occup': 0.04477, 'pct_w_inv_inc': 0.045312, 'pct_hous_own_occ': 0.046228, 'white_per_cap': 0.046706, 'land_area': 0.048502, 'rent_high_q': 0.049942, 'pct_not_hs_grad': 0.051098, 'rent_median': 0.051413, 'pct_pop_under_pov': 0.051499, 'pct_unemployed': 0.053388, 'numb_urban': 0.053486, 'pers_per_fam': 0.053619, 'pct_larg_house_fam': 0.054894, 'own_occ_qrange': 0.055774, 'pers_per_occup_hous': 0.058707, 'pers_per_rent_occ_hous': 0.060013, 'black_per_cap': 0.060615, 'pct_w_pub_asst': 0.060804, 'pct_vacant_boarded': 0.060992, 'male_pct_nev_marr': 0.061954, 'asian_per_cap': 0.062097, 'med_rent_pct_hous_inc': 0.063294, 'population': 0.064506, 'race_pct_hisp': 0.069915, 'pct_immig_rec5': 0.070132, 'pct_teen2par': 0.07193, 'pct_empl_profserv': 0.072509, 'pct_fam2par': 0.07364, 'hous_vacant': 0.074439, 'med_rent': 0.075808, 'med_numbr': 0.076177, 'pct_kids2par': 0.077589, 'pct_pers_dense_hous': 0.079355, 'rent_qrange': 0.083001, 'pct_immig_recent': 0.08506, 'pct_work_mom_young_kids': 0.091108, 'state=a_k': 0.091919, 'pct_work_mom': 0.097567, 'hisp_per_cap': 0.105521, 'pct_w_farm_self': 0.106547, 'lemas_pct_offic_drug_un': 0.111236, 'racepctblack': 0.148031, 'race_pct_white': 0.168484, 'pct_kids_born_never_mar': 0.170315} 
	
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
		if( ("=" not in feat) and choice1 == 1):
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n") 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon, ifmlx = True)
		if( ("=" in feat) and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)


if(choice == 5): # Health
	print(" 1) Linear \n 2) RBF \n 3) Poly")
	choice2 = int(input("Enter choice: "))
	
	print(" 1) LB \n 2) UB")
	get_CE = 1 if (int(input("Enter choice: ")) == 2) else 0
	
	data_folder = "health"
	reg_params = [0.01,0.1,0.1]
	gammas = [0.01]
	degrees = [3]
	coef0s =  [0.01]
	abstractions = ['raf']
	perturbations = ['noise'] if ( choice1 == 1) else ['cat'] 
	
	ScoreLinear = {'Specialty=Pathology': 1.9*(10**(-5)), 'Specialty=Specialty_?': 0.000112, 'ProcedureGroup=SAS': 0.000551, 'PCP': 0.000884, 'ProviderID': 0.001102, 'ProcedureGroup=SMS': 0.001227, 'max_PayDelay': 0.001608, 'PlaceSvc=PlaceSvc_?': 0.001796, 'ProcedureGroup=SNS': 0.001915, 'PrimaryConditionGroup=CATAST': 0.002734, 'PrimaryConditionGroup=PNCRDZ': 0.003891, 'PrimaryConditionGroup=RENAL1': 0.004499, 'ProcedureGroup=ProcedureGroup_?': 0.004618, 'ProcedureGroup=SDS': 0.004696, 'ProcedureGroup=SO': 0.004758, 'PrimaryConditionGroup=PERVALV': 0.005244, 'ProcedureGroup=SRS': 0.005545, 'Specialty=Obstetrics and Gynecology': 0.006128, 'PrimaryConditionGroup=SEPSIS': 0.00721, 'Specialty=Pediatrics': 0.008479, 'PlaceSvc=Ambulance': 0.009014, 'ProcedureGroup=ANES': 0.009573, 'ProcedureGroup=SUS': 0.011422, 'ProcedureGroup=SEOA': 0.01145, 'min_PayDelay': 0.011546, 'PrimaryConditionGroup=FLaELEC': 0.011823, 'ProcedureGroup=SIS': 0.012257, 'ProcedureGroup=SMCD': 0.012548, 'ProcedureGroup=SGS': 0.013044, 'ProcedureGroup=RAD': 0.014125, 'PrimaryConditionGroup=MISCL1': 0.015382, 'PrimaryConditionGroup=PERINTL': 0.016581, 'PlaceSvc=Outpatient Hospital': 0.017274, 'PrimaryConditionGroup=PrimaryConditionGroup_?': 0.019663, 'Specialty=Anesthesiology': 0.020814, 'Specialty=Emergency': 0.021953, 'Specialty=Laboratory': 0.022112, 'PrimaryConditionGroup=GIOBSENT': 0.022436, 'PrimaryConditionGroup=PNEUM': 0.0251, 'PrimaryConditionGroup=HIPFX': 0.025382, 'Vendor': 0.025575, 'PrimaryConditionGroup=SEIZURE': 0.02793, 'PlaceSvc=Home': 0.028758, 'Specialty=General Practice': 0.030313, 'PrimaryConditionGroup=HEART4': 0.030619, 'PlaceSvc=Other': 0.031885, 'PlaceSvc=Urgent Care': 0.03257, 'PrimaryConditionGroup=APPCHOL': 0.032854, 'Specialty=Rehabilitation': 0.033246, 'PrimaryConditionGroup=HEMTOL': 0.035813, 'PrimaryConditionGroup=SKNAUT': 0.040855, 'ProcedureGroup=MED': 0.042124, 'PrimaryConditionGroup=ROAMI': 0.042186, 'PlaceSvc=Independent Lab': 0.042226, 'PrimaryConditionGroup=MISCL5': 0.043929, 'PrimaryConditionGroup=AMI': 0.04664, 'PrimaryConditionGroup=ODaBNCA': 0.051189, 'PayDelay': 0.052775, 'PrimaryConditionGroup=INFEC4': 0.053673, 'PlaceSvc=Inpatient Hospital': 0.054654, 'PrimaryConditionGroup=UTI': 0.055199, 'Sex=?': 0.055712, 'PrimaryConditionGroup=GYNEC1': 0.058941, 'Specialty=Surgery': 0.059227, 'LabCount_months': 0.061084, 'PrimaryConditionGroup=TRAUMA': 0.061579, 'Specialty=Diagnostic Imaging': 0.061948, 'PrimaryConditionGroup=RESPR4': 0.063054, 'PrimaryConditionGroup=RENAL3': 0.064214, 'PrimaryConditionGroup=HEART2': 0.064501, 'LabCount_total': 0.068343, 'PrimaryConditionGroup=GIBLEED': 0.068535, 'Specialty=Other': 0.069636, 'PrimaryConditionGroup=PRGNCY': 0.069773, 'PrimaryConditionGroup=MISCHRT': 0.073718, 'ProcedureGroup=SCS': 0.075631, 'PrimaryConditionGroup=FXDISLC': 0.077975, 'count_ProviderID': 0.088493, 'PlaceSvc=Office': 0.095032, 'Specialty=Internal': 0.096612, 'PrimaryConditionGroup=NEUMENT': 0.099667, 'ProcedureGroup=PL': 0.101905, 'ProcedureGroup=EM': 0.107812, 'DrugCount_months': 0.113765, 'PrimaryConditionGroup=METAB1': 0.138028, 'PrimaryConditionGroup=MSC2a3': 0.140736, 'PrimaryConditionGroup=METAB3': 0.150691, 'PrimaryConditionGroup=ARTHSPIN': 0.177091, 'AgeAtFirstClaim=0-9': 0.193633, 'PrimaryConditionGroup=CANCRB': 0.201133, 'PrimaryConditionGroup=LIVERDZ': 0.216519, 'PrimaryConditionGroup=CANCRM': 0.233073, 'DrugCount_total': 0.243661, 'PrimaryConditionGroup=CHF': 0.357082, 'PrimaryConditionGroup=CANCRA': 0.436935, 'PrimaryConditionGroup=RENAL2': 0.481277, 'PrimaryConditionGroup=STROKE': 0.571565, 'PrimaryConditionGroup=GYNECA': 0.715078, 'PrimaryConditionGroup=COPD': 1.065026} 

	ScorePoly = {'PrimaryConditionGroup=HIPFX': 0.002125, 'PrimaryConditionGroup=HEMTOL': 0.008153, 'PlaceSvc=Other': 0.013525, 'PrimaryConditionGroup=APPCHOL': 0.014098, 'PrimaryConditionGroup=LIVERDZ': 0.014098, 'PrimaryConditionGroup=PERINTL': 0.019774, 'PrimaryConditionGroup=PNCRDZ': 0.020583, 'Specialty=Obstetrics and Gynecology': 0.023992, 'PrimaryConditionGroup=SEPSIS': 0.03455, 'PrimaryConditionGroup=FXDISLC': 0.035073, 'PlaceSvc=Home': 0.041408, 'PrimaryConditionGroup=MSC2a3': 0.043689, 'PrimaryConditionGroup=ARTHSPIN': 0.049609, 'PrimaryConditionGroup=CANCRM': 0.057504, 'PCP': 0.05921, 'PlaceSvc=Inpatient Hospital': 0.062709, 'ProcedureGroup=SGS': 0.070263, 'PrimaryConditionGroup=GYNEC1': 0.071428, 'ProcedureGroup=SNS': 0.073983, 'Specialty=Specialty_?': 0.074492, 'PrimaryConditionGroup=GIBLEED': 0.076775, 'PrimaryConditionGroup=METAB1': 0.079249, 'ProcedureGroup=SRS': 0.079934, 'Specialty=Diagnostic Imaging': 0.08343, 'ProcedureGroup=SUS': 0.085759, 'PrimaryConditionGroup=CATAST': 0.093551, 'PrimaryConditionGroup=RENAL2': 0.093998, 'Specialty=Pathology': 0.094962, 'PrimaryConditionGroup=RENAL1': 0.096263, 'PrimaryConditionGroup=ROAMI': 0.097554, 'PrimaryConditionGroup=NEUMENT': 0.101797, 'PrimaryConditionGroup=MISCL5': 0.106494, 'ProcedureGroup=ProcedureGroup_?': 0.108541, 'ProcedureGroup=ANES': 0.109738, 'PrimaryConditionGroup=AMI': 0.122467, 'Specialty=Pediatrics': 0.132452, 'PlaceSvc=PlaceSvc_?': 0.133592, 'PrimaryConditionGroup=MISCL1': 0.135961, 'PrimaryConditionGroup=GIOBSENT': 0.14024, 'ProcedureGroup=SO': 0.141415, 'PrimaryConditionGroup=INFEC4': 0.142683, 'PrimaryConditionGroup=PERVALV': 0.146255, 'PrimaryConditionGroup=CHF': 0.14998, 'PrimaryConditionGroup=CANCRA': 0.151216, 'PlaceSvc=Ambulance': 0.161541, 'ProcedureGroup=SMCD': 0.17151, 'PrimaryConditionGroup=ODaBNCA': 0.175163, 'Specialty=Laboratory': 0.17552, 'PrimaryConditionGroup=FLaELEC': 0.185854, 'PrimaryConditionGroup=HEART2': 0.203981, 'PrimaryConditionGroup=MISCHRT': 0.210582, 'PrimaryConditionGroup=SKNAUT': 0.213865, 'Specialty=Anesthesiology': 0.215421, 'ProcedureGroup=SAS': 0.22517, 'PrimaryConditionGroup=RENAL3': 0.229022, 'PrimaryConditionGroup=PNEUM': 0.23202, 'ProcedureGroup=EM': 0.235442, 'ProcedureGroup=RAD': 0.240286, 'ProcedureGroup=SEOA': 0.241414, 'PrimaryConditionGroup=PrimaryConditionGroup_?': 0.24707, 'PrimaryConditionGroup=UTI': 0.253684, 'Specialty=Other': 0.276931, 'ProcedureGroup=SIS': 0.279427, 'PrimaryConditionGroup=CANCRB': 0.288792, 'PrimaryConditionGroup=STROKE': 0.292428, 'PayDelay': 0.29825, 'PrimaryConditionGroup=SEIZURE': 0.304709, 'PrimaryConditionGroup=PRGNCY': 0.310982, 'Specialty=Surgery': 0.33199, 'Specialty=Emergency': 0.333775, 'PrimaryConditionGroup=HEART4': 0.335941, 'Specialty=Rehabilitation': 0.357338, 'PlaceSvc=Urgent Care': 0.358464, 'PlaceSvc=Outpatient Hospital': 0.385935, 'ProcedureGroup=SMS': 0.408463, 'ProcedureGroup=MED': 0.434149, 'PrimaryConditionGroup=TRAUMA': 0.458153, 'ProcedureGroup=SDS': 0.46737, 'PlaceSvc=Independent Lab': 0.484111, 'max_PayDelay': 0.512731, 'PrimaryConditionGroup=RESPR4': 0.536181, 'PrimaryConditionGroup=GYNECA': 0.57163, 'Vendor': 0.581454, 'LabCount_total': 0.613078, 'ProviderID': 0.688517, 'PlaceSvc=Office': 0.711158, 'Specialty=Internal': 0.718091, 'Specialty=General Practice': 0.735037, 'PrimaryConditionGroup=COPD': 0.780564, 'count_ProviderID': 0.843463, 'LabCount_months': 0.863791, 'ProcedureGroup=PL': 0.942941, 'DrugCount_total': 0.95486, 'DrugCount_months': 1.029662, 'PrimaryConditionGroup=METAB3': 1.051466, 'ProcedureGroup=SCS': 1.12354, 'min_PayDelay': 1.579491, 'Sex=?': 5.379243, 'AgeAtFirstClaim=0-9': 5.379243} 

	ScoreRBF = {'PrimaryConditionGroup=SEPSIS': 0.000191, 'ProcedureGroup=RAD': 0.000522, 'PlaceSvc=Urgent Care': 0.000674, 'ProcedureGroup=SGS': 0.001023, 'ProcedureGroup=SO': 0.004908, 'Sex=?': 0.005708, 'AgeAtFirstClaim=0-9': 0.005708, 'PrimaryConditionGroup=CATAST': 0.005962, 'max_PayDelay': 0.007243, 'PrimaryConditionGroup=MISCHRT': 0.007551, 'ProcedureGroup=SAS': 0.008879, 'ProcedureGroup=SUS': 0.010466, 'LabCount_months': 0.010944, 'PrimaryConditionGroup=SKNAUT': 0.01255, 'Specialty=Rehabilitation': 0.012753, 'PrimaryConditionGroup=RENAL1': 0.01286, 'PrimaryConditionGroup=PNEUM': 0.01289, 'ProcedureGroup=SRS': 0.01428, 'ProcedureGroup=SMS': 0.015103, 'PrimaryConditionGroup=APPCHOL': 0.015165, 'PlaceSvc=Other': 0.015988, 'ProcedureGroup=PL': 0.016381, 'Specialty=Anesthesiology': 0.01843, 'PlaceSvc=Ambulance': 0.018929, 'PrimaryConditionGroup=PNCRDZ': 0.01932, 'PrimaryConditionGroup=FLaELEC': 0.020218, 'Specialty=General Practice': 0.020753, 'PayDelay': 0.020761, 'PrimaryConditionGroup=PERVALV': 0.020843, 'PlaceSvc=Outpatient Hospital': 0.02437, 'Specialty=Laboratory': 0.024816, 'PrimaryConditionGroup=PrimaryConditionGroup_?': 0.027032, 'Specialty=Emergency': 0.02743, 'Specialty=Pathology': 0.027603, 'PrimaryConditionGroup=SEIZURE': 0.028726, 'PrimaryConditionGroup=HEMTOL': 0.028741, 'ProcedureGroup=SDS': 0.029288, 'DrugCount_months': 0.030886, 'PlaceSvc=Independent Lab': 0.032215, 'ProcedureGroup=SEOA': 0.035579, 'ProcedureGroup=MED': 0.036726, 'Specialty=Surgery': 0.037351, 'PrimaryConditionGroup=HIPFX': 0.037379, 'PrimaryConditionGroup=ROAMI': 0.037856, 'ProcedureGroup=SMCD': 0.038046, 'PlaceSvc=PlaceSvc_?': 0.039604, 'PlaceSvc=Home': 0.03974, 'PrimaryConditionGroup=MISCL1': 0.043832, 'ProcedureGroup=SNS': 0.044128, 'ProcedureGroup=SIS': 0.04539, 'ProcedureGroup=ProcedureGroup_?': 0.046425, 'PrimaryConditionGroup=PERINTL': 0.047446, 'Specialty=Specialty_?': 0.04836, 'PlaceSvc=Inpatient Hospital': 0.048778, 'Specialty=Pediatrics': 0.052916, 'PrimaryConditionGroup=GIOBSENT': 0.05344, 'PCP': 0.05413, 'PrimaryConditionGroup=ODaBNCA': 0.055467, 'PrimaryConditionGroup=INFEC4': 0.059929, 'PrimaryConditionGroup=UTI': 0.060559, 'count_ProviderID': 0.060871, 'ProviderID': 0.062597, 'PrimaryConditionGroup=MISCL5': 0.063712, 'PrimaryConditionGroup=RESPR4': 0.068286, 'Vendor': 0.068686, 'ProcedureGroup=ANES': 0.070109, 'PrimaryConditionGroup=RENAL3': 0.070319, 'PrimaryConditionGroup=HEART2': 0.072895, 'Specialty=Diagnostic Imaging': 0.073188, 'PrimaryConditionGroup=GIBLEED': 0.074284, 'Specialty=Obstetrics and Gynecology': 0.074809, 'PrimaryConditionGroup=FXDISLC': 0.0792, 'PrimaryConditionGroup=CANCRM': 0.083277, 'min_PayDelay': 0.084533, 'PrimaryConditionGroup=NEUMENT': 0.090571, 'ProcedureGroup=SCS': 0.097381, 'PrimaryConditionGroup=TRAUMA': 0.102021, 'PrimaryConditionGroup=AMI': 0.103224, 'ProcedureGroup=EM': 0.103637, 'Specialty=Other': 0.10608, 'PlaceSvc=Office': 0.114197, 'PrimaryConditionGroup=GYNEC1': 0.120906, 'PrimaryConditionGroup=PRGNCY': 0.125797, 'Specialty=Internal': 0.128459, 'PrimaryConditionGroup=HEART4': 0.151217, 'PrimaryConditionGroup=METAB1': 0.154441, 'PrimaryConditionGroup=MSC2a3': 0.160904, 'PrimaryConditionGroup=CANCRA': 0.16348, 'LabCount_total': 0.18432, 'PrimaryConditionGroup=ARTHSPIN': 0.184788, 'PrimaryConditionGroup=LIVERDZ': 0.215455, 'PrimaryConditionGroup=METAB3': 0.274361, 'PrimaryConditionGroup=CHF': 0.276181, 'PrimaryConditionGroup=CANCRB': 0.285056, 'PrimaryConditionGroup=RENAL2': 0.298611, 'DrugCount_total': 0.299905, 'PrimaryConditionGroup=GYNECA': 0.327764, 'PrimaryConditionGroup=STROKE': 0.375117, 'PrimaryConditionGroup=COPD': 0.935849} 

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
		if( (feat in ['LabCount_total', 'LabCount_months', 'DrugCount_total', 'DrugCount_months', 'Vendor', 'PCP', 'PayDelay', 'max_PayDelay', 'min_PayDelay']) and choice1 == 1):
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n") 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)
		if( (feat in ['Sex=?', 'AgeAtFirstClaim=0-9']) and choice1 == 2):
			
			print(f"\n\n\t\t{feat}: {Score[feat]}\n\n")
			feat = feat.split('=', 2)[0] 
			exec.caller(data_folder,reg_params,gammas,degrees,coef0s,abstractions,perturbations,kernel_types,regType = 1, is_OH = 1, get_CE = get_CE, get_avg_bool = False,PerturbFeature=[feat], epsilon = epsilon)

