# exes-n-ohs

by Joe Hahn,<br />
joe.hahn@oracle.com,<br />
5 July 2018<br />
git branch=master

This demo performs a simple machine-learning experiment on a datascience.com instance 
in the cloud, first using scikit-learn to fit a support vector machine (SVM) model
to a simple but rather noisy dataset, and then keras to fit a simple neural-net model
to that same data.

### decision boundary

All records in this dataset are simple pairs of (x,y) coordinates, with each record
being labelled as a members of either the X, O, or B classes depending
upon where its (x,y) coordinates resides within following decision boundary:<br />
![](figs/decision_boundary.png)<br />
Note that a record is designated as a member of the X class if its (x,y) coordinates
places it within the green X. Or else it can be a member of the
red O class, or the blue background B class. To produce this plot, execute the 
_decision_boundaries.ipynb_ notebook to generate the (x,y) data and to 
plot this system's decision boundaries.

### classifying noisy data

To make things more interesting and challenging, use the _svm_model.ipynb_ notebook
to add considerable noise to the pristine data shown above:<br />
![](figs/training_data.png)<br />
noting that system's X,O,B structure is still preserved despite considerable
bleed between the adjacent classes. This notebook then trains an SVM classifier to predict
X,O,B membership using a similarly noise sample of training data. That model's
hyperparameters are optimized, and the resulting classifier has
an accuracy of about 67%.

### using keras to build simple MLP neural net

blah blah blah...

### notes

1 blah blah blah...


