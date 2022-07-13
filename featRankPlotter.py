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



featRank1 = {'residence_since': 5, 'purpose=A410': 5, 'purpose=A44': 5, 'purpose=A45': 5, 'property=A122': 5, 'people_liable_for': 6, 'telephone_A192': 6, 'sex_male': 6, 'status=A12': 6, 'status=A13': 6, 'credit_history=A32': 6, 'purpose=A42': 6, 'purpose=A43': 6, 'purpose=A49': 6, 'savings=A61': 6, 'savings=A62': 6, 'savings=A63': 6, 'savings=A64': 6, 'employment=A71': 6, 'employment=A72': 6, 'employment=A73': 6, 'employment=A75': 6, 'other_debtors=A101': 6, 'other_debtors=A102': 6, 'property=A121': 6, 'property=A123': 6, 'property=A124': 6, 'installment_plans=A141': 6, 'installment_plans=A142': 6, 'installment_plans=A143': 6, 'housing=A152': 6, 'housing=A153': 6, 'skill_level=A171': 6, 'skill_level=A172': 6, 'skill_level=A173': 6, 'skill_level=A174': 6, 'number_of_credits': 7, 'status=A11': 7, 'status=A14': 7, 'credit_history=A31': 7, 'credit_history=A33': 7, 'purpose=A41': 7, 'purpose=A48': 7, 'savings=A65': 7, 'employment=A74': 7, 'other_debtors=A103': 7, 'housing=A151': 7, 'investment_as_income_percentage': 8, 'foreign_worker_A202': 8, 'credit_history=A30': 8, 'credit_history=A34': 8, 'purpose=A46': 8, 'credit_amount': 9, 'age': 9, 'purpose=A40': 9, 'months': 10} 
featRank2 = {'credit_history=A31': 5, 'other_debtors=A101': 5, 'other_debtors=A102': 5, 'housing=A151': 5, 'housing=A152': 5, 'skill_level=A172': 5, 'people_liable_for': 6, 'foreign_worker_A202': 6, 'status=A12': 6, 'status=A13': 6, 'credit_history=A30': 6, 'credit_history=A34': 6, 'purpose=A410': 6, 'purpose=A42': 6, 'purpose=A44': 6, 'purpose=A45': 6, 'purpose=A46': 6, 'purpose=A48': 6, 'purpose=A49': 6, 'savings=A63': 6, 'savings=A64': 6, 'employment=A72': 6, 'employment=A75': 6, 'other_debtors=A103': 6, 'property=A122': 6, 'property=A123': 6, 'installment_plans=A141': 6, 'installment_plans=A142': 6, 'installment_plans=A143': 6, 'housing=A153': 6, 'skill_level=A171': 6, 'skill_level=A174': 6, 'residence_since': 7, 'age': 7, 'number_of_credits': 7, 'sex_male': 7, 'credit_history=A33': 7, 'purpose=A41': 7, 'purpose=A43': 7, 'savings=A61': 7, 'savings=A62': 7, 'savings=A65': 7, 'employment=A71': 7, 'employment=A73': 7, 'employment=A74': 7, 'property=A121': 7, 'property=A124': 7, 'credit_amount': 8, 'investment_as_income_percentage': 8, 'telephone_A192': 8, 'status=A14': 8, 'credit_history=A32': 8, 'purpose=A40': 8, 'skill_level=A173': 8, 'status=A11': 9, 'months': 10} 
 
 


#line_color = ['b','g','y','c','m','r','orange','cyan','pink','peru','lawngreen'];

kernel_name = 'poly'
reg_param = 0.01
gamma = 0.01
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
	input_mid = [0.8235294,0.36238584,0.6666667,1.0,0.78571427,0.33333334,0.0,1,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0]
	#input_mid = [0.29411766,0.1141741,0.33333334,0.6666667,0.23214285,0.0,0.0,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0]
	for feat in featRank1.keys():
		if '=' in feat:
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
		plt.plot(x, y,'--bo')#, color = featColor[legend])
		
		pos11,pos12 = (x[-1],y[-1])
		pos21,pos22 = (x[0],y[0])
		plt.text(pos11,pos12, f'{featRank1[legend]}',fontsize = 30.0)
		plt.text(pos21,pos22, f'{featRank2[legend]}',fontsize = 30.0)
		i += 1
	legend = []
	#for key in allOutcomes.keys():
		#legend.append(f"{key} [{featRank[key]}]")
	#plt.legend(legend, loc ="upper left")
	plt.xlabel('Perturbation of feature Input')
	plt.ylabel('Absolute change in outcome')
	plt.title(f'{data_folder}-{kernel_name}')
	plt.show()
	#plt.savefig('line_plot.png') 
	barPlot()
	

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