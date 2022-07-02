import dataset_mapper
import svm
import statistics
import Perturbation
import matplotlib.pyplot as plt

featRank = {'residence_since': 7.0, 'people_liable_for': 7.0, 'sex_male': 7.0, 'status=A11': 7.0, 'credit_history=A30': 7.0, 'purpose=A40': 7.0, 'savings=A61': 7.0, 'employment=A71': 7.0, 'other_debtors=A101': 7.0, 'property=A121': 7.0, 'installment_plans=A141': 7.0, 'housing=A151': 7.0, 'skill_level=A171': 7.0, 'telephone_A192': 7.2, 'number_of_credits': 7.8, 'investment_as_income_percentage': 8.6, 'foreign_worker_A202': 9.0, 'age': 9.2, 'months': 10.0, 'credit_amount': 10.0} 
kernel_name = 'rbf'
reg_param = 10
gamma = 0.01
degree = 6
coef0 = 15
data_folder = "german"	
training_name = "dataset/training-set.csv"
test_name = "dataset/test-set.csv"

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
		#	continue	
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
			if cols[cid] in featRank.keys():
				input_mid[cid] = 1.0
			else:
				input_mid[cid] = 0.0
		else:
			input_mid[cid] = 0.5
	#input_mid = [0.20588236,0.22724771,0.6666667,1.0,0.2857143,0.0,1.0,1,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0]
	for feat in featRank.keys():
		if '=' in feat:
			continue
		allOutcomes[feat] = outcomeCurve(model,feat,input_mid)
	
	print(allOutcomes)

	for legend,data in allOutcomes.items():
		x = list(data.keys())
		y = list(data.values())
		#print(f"{legend} --> {y}")
		plt.plot(x, y)
		plt.text(x[-1], y[-1], f'{featRank[legend]}')
		plt.text(x[0], y[0], f'{featRank[legend]}')
	legend = []
	for key in allOutcomes.keys():
		legend.append(f"{key} [{featRank[key]}]")
	plt.legend(legend, loc ="upper right")
	plt.xlabel('Perturbation of feature Input')
	plt.ylabel('Absolute change in outcome')
	plt.title(f'{data_folder}-{kernel_name}')
	plt.show()
	

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