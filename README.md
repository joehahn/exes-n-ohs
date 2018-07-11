# exes-n-ohs

by Joe Hahn,<br />
joe.hahn@oracle.com,<br />
5 July 2018<br />
git branch=master

This demo performs a simple machine-learning experiment on a datascience.com instance 
in the cloud, first using scikit-learn to fit a support vector machine (SVM) model
to a simple but rather noisy dataset, and then keras to fit a simple neural-net model
to that same data.

### session settings:

Use these setting when launching a session:

    tool=jupyter
    compute resource=m4.xlarge
    environment=keras & tensorflow


### decision boundary

All records in this dataset are simple pairs of (x,y) coordinates, with each record
being labelled as a members of either the X, O, or B classes depending
upon where its (x,y) coordinates resides within following decision boundary:<br />
![](figs/decision_boundary.png)<br />
Note that a record is designated as a member of the X class if its (x,y) coordinates
places it within the green X. Or else it can be a member of the
red O class, or the blue background B class. To produce this plot, execute the 
_decision_boundaries.ipynb_ notebook to generate the mock (x,y) data and to 
plot this system's decision boundaries.

### classifying noisy data

To make things more interesting and challenging, execute the _svm_model.ipynb_ notebook
to add considerable noise to the pristine mock data shown above:<br />
![](figs/training_data.png)<br />
Look closely to confirm
that the system's X,O,B structure is still preserved despite the noise that
causes considerable bleed between adjacent classes. 
This notebook then trains an SVM classifier to predict
X,O,B membership using a similarly noisy sample of training data. The notebook
also optimizes that model's hyperparameters, and that optimized classifier achieves
an accuracy of about 67%, with the model's inferred decision boundary shown below:<br />
![](figs/svm_decision_boundary.png)<br />
Comparing the model-inferred decision boundary (above) to the system's actual decision
boundary (topmost plot) shows that the SVM model consistently overestimates the width
of the green X, and it also mis-classifies some actual green X records as nearby red O records.

### build MLP neural net with keras

Now build and then train a simple multilayer perceptron (MLP) model using
keras. Keras is my preferred tensorflow-based library, mostly because it is much
easier to build and deploy neural network models using keras than with any
other such library.
tbc...

### todos

1 train the SVM model on polar coordinates rather than cartesian coordinates,
i suspect model accuracy will improve

2 install jupyter-tensorboard?

    pip install jupyter-tensorboard

3 get external ip address:

    pip install ipgetter
    python -m ipgetter 

4 start tensorboard:

     cd exes-n-ohs
     tensorboard --logdir=tf_logs/
     http://52.89.99.15:6006




