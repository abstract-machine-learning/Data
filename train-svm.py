import sys
import dataset_mapper
import classifier_mapper
import svm


#Sanity check
if (len(sys.argv)) < 3:
    print("Usage: " + sys.argv[0] + " <dataset> <output> <kernel> [<gamma> <degree> <c> <C>]")
    sys.exit(-1)


# Reads parameters
dataset_path = sys.argv[1]
output_path = sys.argv[2]
kernel = sys.argv[3]
gamma = 1.0
if len(sys.argv) > 4:
    gamma = float(sys.argv[4])
degree = 2
if len(sys.argv) > 5:
    degree = int(sys.argv[5])
c = 0
if len(sys.argv)> 6:
    c = float(sys.argv[6])
C = 5
if len(sys.argv) > 7:
    C = float(sys.argv[7])


# Trains model
dataset_mapper = dataset_mapper.DatasetMapper()
x, y = dataset_mapper.read(dataset_path)

trainer = svm.SVM(kernel, gamma, degree, c, C)
model = trainer.train(x, y)

classifier_mapper = classifier_mapper.ClassifierMapper()
classifier_mapper.create(model, output_path)
