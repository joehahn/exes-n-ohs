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
model, exposing that model via an API, publishing a report that plots some output, and
using environmental variables to keep passwords confidential.

### session settings:

These settings are used when launching a datascience.com session:

    tool=jupyter
    #compute resource=m4.xlarge
    compute resource=always on, 8GB/1CPU
    environment=keras & tensorflow
    add requirement > pip=pip_install.txt


### decision boundary

After the datascience.com instance becomes available, use the Jupyter notebook _decision_boundaries.ipynb_
to generate the mock (x,y) cartesian data, and plot the mock data's system's decision boundaries.
All records in this dataset contain simple pairs of (x,y) coordinates, with each record
also labelled as being a member of either the X, O, or B classes depending
upon where its (x,y) coordinates reside within following decision boundary:<br />
![](figs/decision_boundary.png)<br />
with record designated a member of the X class if its (x,y) coordinates
places it within the green X, or else it can be a member of the
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

### build CNET neural net with keras

Now build and then train a simple convolution neural network (CNET) model using
keras. Keras is my preferred tensorflow-based library, mostly because it is much
easier to build and deploy neural network models using keras than with any
other such library. Execute the _cnet_model.ipynb_ notebook to generate
the following summary report that describes the CNET model built here:<br />
![](figs/cnet_summary.png)<br />
so this neural net is a pair of convolution + pooling layers,
and such networks are typically used on image data. Note that our task--which is
to classify a pair of (x,y) coordinates--is akin to performing image classification
on images having a single nonzero pixel, and is why a CNET model is used here.
But our CNET model also has a singe dense input layer having N=100^2 neurons that
is then reshaped into a 100x100 grid, and its purpose is to onehot-encode
the (x,y) input across that 100x100 grid. 
The CNET model is then trained on the XO dataset,
and that trained model is then used to compute its decision boundary:<br />
![](figs/cnet_decision_boundary.png)<br />
which is an improvement since the CNET does recover a complete green X pattern
that had eluded the SVM model. But the width of the X is still too wide, and the CNET
model's overall accuracy is about the same as the SVM model.


### deploy model API

Now use the script _cnet_model_api.py_ to wrap an API around the CNET model's predict method,
with that API deployed using these settings:

    API Name=exes-n-ohs-api
    description=API for calling the CNET model built by the exes-n-ohs demo
    model to deploy=cnet_model_api.py
    compute resource=always on, 0.5GB 0.5CPU
    environment=keras & tensorflow
    Specify Function=api_predict
    Example Data={"data":{"x":1.0, "y":2.0}}

Then test that API by using curl to feed a pair of jsonized x,y coordinates into that API's url:

    curl -L -X POST -d '{"data":{"x":1.0, "y":2.0}}' -H 'Content-Type: application/json' \
        -H 'Cookie: datascience-platform=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkNDE5MmNhZS00ZGMxLTQ0MjUtOWIwNy0wMmZjNGE5YzQxODEiLCJzZXJ2aWNlTmFtZSI6ImRlcGxveS1leGVzLW4tb2hzLWFwaS0zNDI5MDEtdjEiLCJpYXQiOjE1MzMxNDU5MzZ9.CODpoPRdWzYa3hlv1osArKrYsv3AB4gTuwOX_S2WGpY' \
        https://demo-next.datascience.com/deploy/deploy-exes-n-ohs-api-342901-v1/

which should report something like

    {
      "class_pred": "X", 
      "class_prob": "0.537"
    }

which says that the model thinks that a record having (x,y)=(1,2) is most likely class X
with confidence score 53.7%.

But if you get "curl: (60) SSL certificate problem: unable to get local issuer certificate"
just add -k option to that curl command.


### publish a report

Execute _confidence_levels.ipynb_ to generate the report's contents, which includes a plot of the distribution of
the MLP model's confidence scores<br />
![](figs/cnet_confidence_scores.png)<br />
As expected,  predictions having confidence scores > 0.9 can still be incorrect about 20% of the time,
while those having scores < 0.6 are correct only about half of the time.
And below we redraw of the model's decision boundaries with dot intensity indicating model confidence:<br />
![](figs/cnet_confidence_boundary.png)<br />
with the densest dots having confidence score > 0.85, intermediate dots have 0.60 < score < 0.85,
and the lightest dots have score < 0.60. As expected, the model is most confident about its
predictions in regions where the XOB classes are well seperated and class confusion is minimal.

To publish that notebook's contents, click Publish a Report and use these settings:

    file=confidence_levels.ipynb
    Title=CNET Confidence Levels
    Description=CNET model's confidence levels
    
which can then be shared via a URL like

    https://demo-next.datascience.com/project/exes-n-ohs/outputs/report/cnet-confidence-levels-UG9zdFR5cGU6MjU3/versions/2


### jupyter dashboard

Jupyter-dashboard is an extension that was added on launch via pip_install.txt. To manually
turn it on, start a terminal and then tell jupyter notebook about the jupyter dashboards:

    sudo jupyter dashboards quick-setup --sys-prefix

and then restart the _confidence_levels.ipynb_ notebnook
and click its new dashboard icon:<br />
![](figs/dashboard.png)<br />


### environmental variables

To avoid exposing confidential info via git, like hardcoded database passwords and AWS keys,
instead store them in the datascience.com platform as environment variables:
click Settings > Environment Variables and enter Key=PASSWORD and Value=Larry's last name.
Then execute _test_password.ipynb_ to confirm that notebook is aware of the password.


### notes


1 install jupyter-tensorboard ...didnt work

    pip install jupyter-tensorboard
    #get external ip address:
    pip install ipgetter
    python -m ipgetter 
    #start tensorboard:
    cd exes-n-ohs
    tensorboard --logdir=tf_logs/
    http://52.89.99.15:6006

4 to install install jupyter_dashboards:

    pip install jupyter_dashboards
    sudo jupyter dashboards quick-setup --sys-prefix

5 force a git pull:

    git fetch --all
    git reset --hard origin/master


### todo

1 get tensorboard up and running on datascience.com, and use it to peek at the CNET
layers to for example see whether its topmost dense layer is in fact onehot encoding
the input (x,y) data

