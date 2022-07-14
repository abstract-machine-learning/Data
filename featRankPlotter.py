import dataset_mapper
import svm
import statistics
import Perturbation
import matplotlib.pyplot as plt
import numpy as np

#kernel_name = 'poly'
#reg_param = 0.01
#gamma = 0.01
#degree = 6 
#coef0 = 3


# Their
featRank2 = {'purpose=A42': 4, 'credit_history=A30': 5, 'purpose=A46': 5, 'purpose=A49': 5, 'savings=A63': 5, 'other_debtors=A101': 5, 'housing=A151': 5, 'skill_level=A172': 5, 'credit_amount': 6, 'number_of_credits': 6, 'foreign_worker_A202': 6, 'sex_male': 6, 'credit_history=A31': 6, 'purpose=A410': 6, 'purpose=A44': 6, 'purpose=A45': 6, 'purpose=A48': 6, 'savings=A62': 6, 'savings=A64': 6, 'employment=A71': 6, 'employment=A72': 6, 'other_debtors=A103': 6, 'property=A122': 6, 'property=A124': 6, 'installment_plans=A141': 6, 'installment_plans=A142': 6, 'housing=A152': 6, 'housing=A153': 6, 'skill_level=A171': 6, 'skill_level=A174': 6, 'age': 7, 'people_liable_for': 7, 'status=A12': 7, 'status=A13': 7, 'credit_history=A32': 7, 'credit_history=A33': 7, 'purpose=A41': 7, 'purpose=A43': 7, 'savings=A61': 7, 'savings=A65': 7, 'employment=A73': 7, 'employment=A75': 7, 'other_debtors=A102': 7, 'installment_plans=A143': 7, 'skill_level=A173': 7, 'months': 8, 'investment_as_income_percentage': 8, 'residence_since': 8, 'telephone_A192': 8, 'status=A11': 8, 'status=A14': 8, 'credit_history=A34': 8, 'employment=A74': 8, 'property=A121': 8, 'property=A123': 8, 'purpose=A40': 9} 

# Our
featRank1 = {'sex_male': 6, 'status=A11': 6, 'credit_history=A30': 6, 'purpose=A40': 6, 'savings=A61': 6, 'employment=A71': 6, 'other_debtors=A101': 6, 'property=A121': 6, 'installment_plans=A141': 6, 'housing=A151': 6, 'skill_level=A171': 6, 'residence_since': 7, 'number_of_credits': 7, 'people_liable_for': 7, 'telephone_A192': 7, 'investment_as_income_percentage': 9, 'age': 9, 'months': 10, 'credit_amount': 10, 'foreign_worker_A202': 10} 

featColor = {'residence_since': 'b', 'people_liable_for': 'g', 'telephone_A192': 'y', 'sex_male': 'c', 'investment_as_income_percentage': 'm', 'number_of_credits': 'r', 'foreign_worker_A202': 'orange', 'months': 'cyan', 'age': 'pink', 'credit_amount': 'peru',}

kernel_name = 'rbf'
reg_param = 10
gamma = 0.05
degree = 6
coef0 = 3

data_folder = "german"	
training_name = "dataset/training-set.csv"
test_name = "dataset/test-set.csv"

def barPlot():
	F1 = []
	F2 = []
	X = []
	for k,v in featRank1.items():
		if "=" in k:
			continue
		F1.append(v)
		F2.append(featRank2[k])
		X.append(k)
	
	X_axis = np.arange(len(X))

	plt.bar(X_axis - 0.2, F1, 0.4, label = 'Our')
	plt.bar(X_axis + 0.2, F2, 0.4, label = 'Their')
	  
	plt.xticks(X_axis, X)
	plt.xlabel("Feature")
	plt.ylabel("Grade")
	plt.legend()
	plt.show()

def test_SVM(model):
	from sklearn import metrics
	dataset_path = f"./{data_folder}/{test_name}"
	dataset_mapper1 = dataset_mapper.DatasetMapper()
	x, y = dataset_mapper1.read(dataset_path)
	y_pred = model.predict(x)
	print("Accuracy:",metrics.accuracy_score(y, y_pred))
	print("Balanced Accuracy:",metrics.balanced_accuracy_score(y, y_pred))


def outcomeCurve(model,feat,input_mid):
	Fid = Perturbation.readColumns(f'./{data_folder}/dataset/columns.csv').index(feat)
	outcomes = dict()
	store = input_mid[Fid]
	for Fval in range(-5,6):
		input_mid[Fid] = store - Fval/10
		print(input_mid[Fid])
		#if not (input_mid[Fid] <= 1 and input_mid[Fid] >= 0):
			#continue	
		outcomes[Fval/10] = list(model.decision_function([input_mid]))[0]
	print(outcomes)
	input_mid[Fid] = store
	mid = outcomes[0.0]
	for key in outcomes.keys():
		outcomes[key] = abs(outcomes[key] - mid)
	return outcomes

def alloutcomeCurve(model):
	allOutcomes = dict()
	cols = Perturbation.readColumns(f'./{data_folder}/dataset/columns.csv')
	input_mid = [0.0]*(len(cols))
	for cid in range(len(cols)):
		if '=' in cols[cid]:
			if cols[cid] in featRank1.keys():
				input_mid[cid] = 1.0
			else:
				input_mid[cid] = 0.0
		else:
			input_mid[cid] = 0.5
	#input_mid = [0.25,0.113843955,0.33333334,0.0,0.25,0.0,0.0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0]
	input_mid = [0.029411765,0.05425333,0.33333334,1.0,0.5535714,0.0,0.0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0]
	for feat in featRank1.keys():
		if '=' in feat or feat == 'sex_male':
			continue
		allOutcomes[feat] = outcomeCurve(model,feat,input_mid)
	
	print(allOutcomes)

	f = plt.figure()
	f.set_figwidth(2)
	f.set_figheight(2)
	i = 0
	for legend,data in allOutcomes.items():
		x = list(data.keys())
		y = list(data.values())
		#print(f"{legend} --> {y}")
		plt.plot(x, y,'--bo', color = featColor[legend])
		
		pos11,pos12 = (x[-1],y[-1])
		pos21,pos22 = (x[0],y[0])
		if(legend in ["residence_since"]):
			pos11,pos12 = (x[-1],y[-1]-0.02)
		if(legend in ["investment_as_income_percentage"]):
			pos21,pos22 = (x[0],y[0]-0.022)
			pos11,pos12 = (x[-1],y[-1]-0.023)
		plt.text(pos11,pos12, f'{featRank1[legend]}',fontsize = 30.0)
		plt.text(pos21,pos22, f'{featRank2[legend]}',fontsize = 30.0)
		i += 1
	plt.text(-0.37,0.35, f'MLX',fontsize = 30.0)
	plt.text(0.27,0.35, f'OUR',fontsize = 30.0)
	legend = []
	for key in allOutcomes.keys():
		legend.append(f"{key} [{featRank1[key]}]")
	plt.legend(legend, loc ="upper left")
	plt.xlabel('Perturbation of feature Input')
	plt.ylabel('Absolute change in outcome')
	plt.title(f'{data_folder}-{kernel_name}')
	plt.show()
	#plt.savefig('line_plot.png') 
	#barPlot()
	

def exec():
	dataset_path = f"./{data_folder}/{training_name}"
	print(f"Creating {kernel_name}-SVM")
	# Trains model
	dataset_mapper1 = dataset_mapper.DatasetMapper()
	x, y = dataset_mapper1.read(dataset_path)
	
	trainer = svm.SVM(kernel_name, gamma, degree, coef0, reg_param)
	model = trainer.train(x, y)
	test_SVM(model)
	alloutcomeCurve(model)

exec()