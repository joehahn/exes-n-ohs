# exes-n-ohs

by Joe Hahn,<br />
joe.hahn@oracle.com,<br />
5 July 2018<br />
git branch=master

This demo performs a simple machine-learning experiment in a datascience.com instance 
in the cloud, first using scikit-learn to fit a support vector machine (SVM) model
to a simple but rather noisy dataset, and then keras to fit a simple neural-net model
to that same data.

### decision boundaries

All records in this dataset are simple pairs of (x,y) coordinates, with each record
being labelled as a members of either the X, O, or B classes, depending
upon where those (x,y) coordinates reside within following decision boundary:<br />
![](figs/decision_boundary.png)<br />
Note that a record is designated as a member of the X class if its (x,y) coordinates
places it within the green X. Or else the record is a member of the
red O class, or perhaps the blue background class B. To generate this plot, execute the 
_decision_boundaries.ipynb_ notebook to manufacture the (x,y) data and to 
plot the system's decision boundaries.

### classifying noisy data

To make things more interesting and challenging, use the _svm_model.ipynb_ notebook
to add considerable noise to the pristine data seen above:<br />
![](figs/training_data.png)<br />
noting that system's X,O,B structure is still preserved despite considerable
bleed between adjacent classes. This notebook then trains an SVM classifier to predict
X,O,B membership on a similarly noise sample of training data. That model's
hyperparameters are optimized,  acheives
and accuracy of about 70%

### notes

1 blah blah blah...


