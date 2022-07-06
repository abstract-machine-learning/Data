import dataset_mapper
import svm
import statistics
import Perturbation
import matplotlib.pyplot as plt

#kernel_name = 'poly'
#reg_param = 0.01
#gamma = 0.01
#degree = 6 
#coef0 = 3



featRank = {'people_liable_for': 6.0, 'telephone_A192': 6.0, 'sex_male': 6.0, 'residence_since': 7.4, 'status=A11': 7.4, 'credit_history=A30': 7.4, 'purpose=A40': 7.4, 'savings=A61': 7.4, 'employment=A71': 7.4, 'other_debtors=A101': 7.4, 'property=A121': 7.4, 'installment_plans=A141': 7.4, 'housing=A151': 7.4, 'skill_level=A171': 7.4, 'foreign_worker_A202': 7.6, 'investment_as_income_percentage': 8.0, 'number_of_credits': 8.6, 'credit_amount': 8.8, 'age': 8.8, 'months': 10.0}  
featColor = {'residence_since': 'b', 'people_liable_for': 'g', 'telephone_A192': 'y', 'sex_male': 'c', 'investment_as_income_percentage': 'm', 'number_of_credits': 'r', 'foreign_worker_A202': 'orange', 'months': 'cyan', 'age': 'pink', 'credit_amount': 'peru',}
#line_color = ['b','g','y','c','m','r','orange','cyan','pink','peru','lawngreen'];

kernel_name = 'poly'
reg_param = 0.01
gamma = 0.01
degree = 6
coef0 = 3

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
			if cols[cid] in featRank.keys():
				input_mid[cid] = 1.0
			else:
				input_mid[cid] = 0.0
		else:
			input_mid[cid] = 0.5
	input_mid = [0.20588236,0.22724771,0.6666667,1.0,0.2857143,0.0,1.0,1,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0]
	#input_mid = [0.29411766,0.1141741,0.33333334,0.6666667,0.23214285,0.0,0.0,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0]
	for feat in featRank.keys():
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
		plt.plot(x, y,'--bo', color = featColor[legend])
		
		pos11,pos12 = (x[-1],y[-1])
		pos21,pos22 = (x[0],y[0])
		if(legend in ["foreign_worker_A202","people_liable_for"]):
			pos11,pos12 = (x[-1],y[-1]+0.015)
		if(legend in ["telephone_A192"]):
			pos11,pos12 = (x[-1],y[-1]-0.015)
		plt.text(pos11-0.1,pos12, f'{featRank[legend]}',fontsize = 30.0)
		#plt.text(pos21,pos22, f'{featRank[legend]}',fontsize = 30.0)
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