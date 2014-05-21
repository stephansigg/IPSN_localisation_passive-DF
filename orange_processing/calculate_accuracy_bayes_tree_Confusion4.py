# -*- coding: utf-8 -*-
# Category:    evaluation
# Description: Set a number of learners, split data to train and test set, learn models from train set and estimate classification accuracy on the test set
# Uses:        voting.tab
# Classes:     MakeRandomIndices2
# Referenced:  c_performance.htm

import orange, orngTree
######################
# import for svm:
from Orange.classification import svm
from Orange.evaluation import testing, scoring
######################
# For Confusion matrix:
import orngTest, orngStat
######################
import Orange

#import pdb ## DEBUGGING  pdb.set_trace()

def accuracy(test_data, classifiers):
    correct = [0.0]*len(classifiers)
    for ex in test_data:
        for i in range(len(classifiers)):
            if classifiers[i](ex) == ex.getclass():
                correct[i] += 1
    for i in range(len(correct)):
        correct[i] = correct[i] / len(test_data)
    return correct

def accuracy2(test_data, classifiers, classCount):
    correct = [0.0]*len(classifiers)
    classes = []
    # now, find all classes in the set.
    counter = 0
    for ex in train_data:
        found = 'nothing'
        for j in range(counter):
            if ex.getclass() == classes[j]:
                found = 'found'
        if found == 'nothing':
            counter += 1
            classes.append(ex.getclass())
    # initialise confusion matrix
    confusionMatrix = [0]*classCount*classCount # this is a concatenation of 'classCount' arrays of size 'classCount' to represent the respective entries in the confusion matrix.
    # Problem still: I have to have all classes in order to identify which one was predicted for which.
    # The diagonal is easy, but what about the other entries?
    # Find all classes and put them in a matrix
    # other solution: provide the class count as a parameter
        # now fill confusion matrix
    for ex in test_data:
        truth = 'nothing'
        predicted = 'nothing'
        firstIndex=0
        secondIndex=0
        for j in range(counter):
            if ex.getclass() == classes[j]:
                truth = classes[j]
                firstIndex=j
            if classifiers[0](ex) == classes[j]:
                predicted = classes[j]
                secondIndex=j
        # fill the matrix
        confusionMatrix[firstIndex*classCount+secondIndex] +=1
    return confusionMatrix



# set up the classifiers
###data = orange.ExampleTable("voting")
###selection = orange.MakeRandomIndices2(data, 0.5)
###train_data = data.select(selection, 0)
###test_data = data.select(selection, 1)
filename_train = "../../src/tests/data.tab"
filename_test = "../../src/tests/data.tab"
train_data = orange.ExampleTable(filename_train)
test_data = orange.ExampleTable(filename_test)
#train_data = Orange.data.Table("WS70_Features_0.5-annotated_[directoryNamesIM]")
#test_data = Orange.data.Table("WS70_Features_0.5-NOTannotated_[directoryNamesIM]")

### comment out if not required
## Old ? Train-Data vs. Test-data
#######bayes = orange.BayesLearner(train_data)
#######tree = orngTree.TreeLearner(train_data)
#######knnLearner = orange.kNNLearner(train_data)
#######svm = svm.SVMLearner(train_data)
#######bayes.name = "bayes"
#######tree.name = "tree"
#######knnLearner.name = "knn"
#######svm.name = "svm"

#######for j in range(2,20):
    #######knnLearner.k = j
    
    #######print "train_data:"
    #######print filename_train
    #######print "test_data:"
    #######print filename_test
    #######print "k=="
    #######print knnLearner.k
    
    #######classes = test_data.domain.class_var.values
    #######print "\t" + "\t".join(classes)

    #######classifiers = [bayes, tree, knnLearner, svm]
    #######classifiersConfusion = [knnLearner]
    ######## compute accuracies
    #######acc = accuracy(test_data, classifiers)
    #######print "Classification accuracies:"
    #######for i in range(len(classifiers)):
	#######print classifiers[i].name, acc[i]
    ########
    #######acc2 = accuracy2(test_data, classifiersConfusion, 11)
    #######print "confusion matrix for the "+classifiersConfusion[0].name+" classifier:"
    #######for i in range(len(acc2)):
	#######print acc2[i]


###################################################
### Now: Confusion Matrix!!!
###################################################

bayes2 = orange.BayesLearner()
tree2 = orngTree.TreeLearner()
knnLearner2 = orange.kNNLearner()
knnLearner2.k = 10 # k == 18 seems to be best (at least for 2-3)
#svm2 = svm.SVMLearner()
bayes2.name = "bayes2"
tree2.name = "tree2"
knnLearner2.name = "knn2"
#svm2.name = "svm2"

learners = [bayes2, tree2, knnLearner2]

results = orngTest.crossValidation(learners, train_data, folds=10)

# output the results
print "train_data:"
print filename_train
print "k=="
print knnLearner2.k
print "Learner  CA     IS     Brier    AUC"
for i in range(len(learners)):
    print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, \
        orngStat.CA(results)[i], orngStat.IS(results)[i],
        orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])
######################
### Now the confusion matrix:
###cm = orngStat.computeConfusionMatrices(results,
   ###     classIndex=data.domain.classVar.values.index('democrat'))
#cm = orngStat.computeConfusionMatrices(results,classIndex=-1)

print
cm = Orange.evaluation.scoring.confusion_matrices(results)[0]
classes = test_data.domain.class_var.values
print "\t" + "\t".join(classes)
#pdb.set_trace()
for className, classConfusions in zip(classes, cm):
    print ("%s" + ("\t%i" * len(classes))) % ((className,) + tuple(classConfusions))
cm = Orange.evaluation.scoring.confusion_matrices(results)[1]
classes = test_data.domain.class_var.values
print "\t" + "\t".join(classes)
for className, classConfusions in zip(classes, cm):
    print ("%s" + ("\t%i" * len(classes))) % ((className,) + tuple(classConfusions))
cm = Orange.evaluation.scoring.confusion_matrices(results)[2]
classes = test_data.domain.class_var.values
print "\t" + "\t".join(classes)
for className, classConfusions in zip(classes, cm):
    print ("%s" + ("\t%i" * len(classes))) % ((className,) + tuple(classConfusions))


## loop over k:

for i in range(11,21):
	# output the results
	knnLearner2.k = i
	results = orngTest.crossValidation(learners, train_data, folds=10)
	print "train_data:"
	print filename_train
	print "k=="
	print knnLearner2.k
	print "Learner  CA     IS     Brier    AUC"
	for i in range(len(learners)):
		print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, \
			orngStat.CA(results)[i], orngStat.IS(results)[i],
			orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])
	######################
	### Now the confusion matrix:
	###cm = orngStat.computeConfusionMatrices(results,
	###     classIndex=data.domain.classVar.values.index('democrat'))
	#cm = orngStat.computeConfusionMatrices(results,classIndex=-1)

	print
	cm = Orange.evaluation.scoring.confusion_matrices(results)[0]
	classes = test_data.domain.class_var.values
	print "\t" + "\t".join(classes)
	for className, classConfusions in zip(classes, cm):
		print ("%s" + ("\t%i" * len(classes))) % ((className,) + tuple(classConfusions))
	cm = Orange.evaluation.scoring.confusion_matrices(results)[1]
	classes = test_data.domain.class_var.values
	print "\t" + "\t".join(classes)
	for className, classConfusions in zip(classes, cm):
		print ("%s" + ("\t%i" * len(classes))) % ((className,) + tuple(classConfusions))
	cm = Orange.evaluation.scoring.confusion_matrices(results)[2]
	classes = test_data.domain.class_var.values
	print "\t" + "\t".join(classes)
	for className, classConfusions in zip(classes, cm):
		print ("%s" + ("\t%i" * len(classes))) % ((className,) + tuple(classConfusions))


