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

These settings are used when launching a datascience.com session:

    tool=jupyter
    #compute resource=m4.xlarge
    compute resource=always on, 8GB/1CPU
    environment=keras & tensorflow
    add requirement > pip=pip_install.txt


### decision boundary

After the datascience.com instance becomes available, use the Jupyter notebook _decision_boundaries.ipynb_
to generate the mock (x,y) cartesian data, and then plot the mock data's system's decision boundaries.
All records in this dataset contain simple pairs of (x,y) coordinates, with each record
also labelled as being a member of either the X, O, or B classes depending
upon where its (x,y) coordinates reside within following decision boundary:<br />
![](figs/decision_boundary.png)<br />
A record is designated a member of the X class if its (x,y) coordinates
places it within the green X. Or else it can be a member of the
red O class, or the blue background B class. 

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
an accuracy of about 68%, with the model's inferred decision boundary shown below:<br />
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
to receive each record's (x,y) coordinates, three densely-connected
hidden layers composed of N=16, 32, and then 12 neurons,
followed by an N=3 neuron layer that outputs
each record's class probabilities. And to manage any overfitting, dropout
layers are also sandwiched between some of the hidden layers with
dropout fractions of 0.2 and 0.1

The MLP model is then trained on a much larger sample of records, 2 million,
and that trained  model is then used to compute its decision boundary:<br />
![](figs/mlp_decision_boundary.png)<br />
which looks quite similar to that produced by the SVM model with similar
accuracy.

This MLP model's hyperparameters are the number of hidden layers (currently 3) and
the number of neurons in each hidden layer (16, 32, and 12) as well as the dropout_fractions.
Manually exploring many such models having more or less layers and neurons, as well as
taller & narrower neural nets (which have fewer neurons spread across more layers)
reveals that taller/narrow nets are more performant than shorter/fatter ones.
Nonetheless the MLP model user here does not outperform the SVM model, which is kinda dissapointing.
Bitmapping the input (x,y) coordinates and using a convolution neural net (rather than MLP)
might yield a more accurate model.


### deploy model API

The script _mlp_model_api.py_ also wraps an API around the MLP model's predict method,
and that API is deployed with these settings:

    API Name=exes-n-ohs-api
    description=API for calling the MLP model built by the exes-n-ohs demo
    model to deploy=mlp_model_api.py
    compute resource=always on, 0.5GB 0.5CPU
    environment=keras & tensorflow
    Specify Function=api_predict
    Example Data={"data":{"x":1.0, "y":2.0}}

To test that API, use curl to feed a pair of jsonized x,y coordinates into that API's url:

    curl -L -X POST -d '{"data":{"x":1.0, "y":2.0}}' -H 'Content-Type: application/json' \
        -H'Cookie: datascience-platform=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MWI5YmM4YS0xMmI0LTRiOTgtYTNmNy00NzcxYmJhZGIyMzEiLCJzZXJ2aWNlTmFtZSI6ImRlcGxveS1leGVzLW4tb2hzLWFwaS0xOTY2LXYyIiwiaWF0IjoxNTMxNTA2NzAyfQ.4fEiEYjBFHj9MxeW5SyYMg9FQrp9glvN8D6GAh9rrco' \
        https://demo-next.datascience.com/deploy/deploy-exes-n-ohs-api-1966-v2/

which should report something like

    {
      "class_pred": "O", 
      "class_prob": "0.592"
    }

so the model reports that a record having (x,y)=(1,2) is most likely class O, with confidence score 54.7%.

If instead you get "curl: (60) SSL certificate problem: unable to get local issuer certificate"
add -k option to curl command.


### publish a report

Execute _confidence_levels.ipynb_ to generate the report's contents, which includes a plot of the distribution of
the MLP model's confidence scores<br />
![](figs/mlp_confidence_scores.png)<br />
and a redraw of the model's decision boundaries but dot intensity indicating model confidence:<br />
![](figs/mlp_confidence_boundary.png)<br />

To publish that notebook's contents, click Publish a Report and use these settings:

    file=confidence_levels.ipynb
    Title=MLP Confidence Levels
    Description=MLP model's confidence levels
    

### jupyter dashboard

Jupyter-dashboard is an extension that was added on launch via pip_install.txt. To manually
turn it on, a terminal and then tell jupyter notebook about the jupyter dashboards:

    sudo jupyter dashboards quick-setup --sys-prefix

and then execute _confidence_levels.ipynb_ and click the new dashboard icon

### todo


3 add hashed password


### notes

1 The MLP model was first trained on the (x,y) cartesian coordinates, and that model
was as accurate as the SVM model. Then MLP was trained on the (r,angle) polar
coordinates, that model was less accurate. Current MLP model is now trained on 
the redundant set of (x,y,r,angle) data, and is as good as SVM.

2 training MLP model on bit-mapped (x,y) input data might improve model accuracy. 
Using bit-mapped input + convolution neural net (rather than MLP) might be even better

3 install jupyter-tensorboard ...didnt work

    pip install jupyter-tensorboard
    #get external ip address:
    pip install ipgetter
    python -m ipgetter 
    #start tensorboard:
    cd exes-n-ohs
    tensorboard --logdir=tf_logs/
    http://52.89.99.15:6006

4 to install pip install jupyter_dashboards:

    pip install jupyter_dashboards

5 force a git pull:

    git fetch --all
    git reset --hard origin/master



