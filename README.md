# exes-n-ohs

by Joe Hahn,<br />
joe.hahn@oracle.com,<br />
5 July 2018<br />
git branch=master

This demo performs a simple machine-learning experiment on a datascience.com instance 
in the cloud, first using scikit-learn to fit a support vector machine (SVM) model
to a simple but rather noisy dataset, and then keras to fit a simple neural-net model
to that same data. The main purpose of this demo is illustrate usage of all the
key elements of the datascience.com platform, namely, to use a notebook to train a predictive
model, exposing that model via an API, and ...

### session settings:

Use these setting when launching a session:

    tool=jupyter
    compute resource=m4.xlarge
    environment=keras & tensorflow
    add requirement > pip=pip_install.txt


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
other such library. Execute the _mlp_model.ipynb_ notebook to generate
the following summary report that describes the MLP model built here:<br />
![](figs/mlp_summary.png)<br />
which shows that this neural net has five layers, an input layer having N=2 neurons
that receive each record's (x,y) coordinates, three densely-connected
hidden layers composed of N=10, 60, and then 20 neurons,
followed by an N=3 neuron layer that outputs
each record's class probabilities. And to manage any overfitting, dropout
layers are also sandwiched between each of the above dense layers
with dropout_fraction=0.1

The MLP model is then trained on a much larger sample of records, 10 million,
and that trained  model is then used to compute its decision boundary:<br />
![](figs/mlp_decision_boundary.png)<br />
which looks quite similar to that produced by the SVM model. However the MLP model's
accuracy, 61%, is a bit lower than SVM.

Adding another layer might boost MLP accuracy on the green X class. Or maybe
boosting the green's representation in the training dataset. Still in progress...

### deploy model API

The script _mlp_model_api.py_ also wraps an API around the MLP model's predict method,
and that API is then deployed with these settings:

    API Name=exes-n-ohs-api
    description=API that calls the MLP model built by the exes-n-ohs demo
    model to deploy=mlp_model_api.py
    compute resource=m4.xlarge
    environment=keras & tensorflow
    add requirement > pip=pip_install.txt
    Specify Function=api_predict
    Example Data={"data":{"x":1.0, "y":2.0}}

Then curl that API to generate a prediction from a jsonized pair of x,y coordinates:

curl -L -X POST -d '{"data":{"x":1.0, "y":2.0}}' -H 'Content-Type: application/json' \
    -H'Cookie: datascience-platform=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MWI5YmM4YS0xMmI0LTRiOTgtYTNmNy00NzcxYmJhZGIyMzEiLCJzZXJ2aWNlTmFtZSI6ImRlcGxveS1leGVzLW4tb2hzLWFwaS0xOTY2LXYyIiwiaWF0IjoxNTMxNTA2NzAyfQ.4fEiEYjBFHj9MxeW5SyYMg9FQrp9glvN8D6GAh9rrco' \
     https://demo-next.datascience.com/deploy/deploy-exes-n-ohs-api-1966-v2/

which should report something like

    {
      "class_pred": "O", 
      "class_prob": "0.547"
    }


### todo

1 publish a report or dashboard

3 add hashed password

4 try training model on polar rather than cartesian coordinates, that might boost
model accuracy

### notes

1 train the SVM model on polar coordinates rather than cartesian coordinates,
i suspect model accuracy will improve

2 install jupyter-tensorboard ...didnt work

    pip install jupyter-tensorboard
    #get external ip address:
    pip install ipgetter
    python -m ipgetter 
    #start tensorboard:
    cd exes-n-ohs
    tensorboard --logdir=tf_logs/
    http://52.89.99.15:6006

3 force a git pull:

    git fetch --all
    git reset --hard origin/master



