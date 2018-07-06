# exes-n-ohs

by Joe Hahn,<br />
joe.hahn@oracle.com,<br />
5 July 2018<br />
git branch=master

This demo performs a simple machine-learning experiment in the datascience.com
cloud, using scikit-learn to fit a support vector machine (SVM) model
to a simple but rather noisy dataset, and then keras to fit a simple neural-net model
to that same data.

### decision boundaries

All records in this dataset include a simple pair of (x,y) coordinates, and each record
in this dataset is then labelled as a members of either the X, O, or B classes, depending
upon where those (x,y) coordinates reside within following decision boundary:<br />
![](figs/decision_boundary.png)<br />
noting that a record is designated as a member of the X class if its (x,y) coordinates
place it within the green X, or is perhaps a member of the red O class, or blue background
B class. To generate this plot, execute the 
_decision_boundaries.ipynb_ notebook to manufacture the (x,y) data and to 
plot the system's decision boundaries.

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


