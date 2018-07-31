#helper_fns.py
#
#by Joe Hahn
#joe.hahn@oracle.com
#3 July 2018
#
#these helper functions are called by something.ipynb

#do the following before importing this 
#import numpy as np
#rn_state = np.random.RandomState(seed=rn_seed)

#generate a dict containing a single record's facts: id, coordinates, class etc
import numpy as np
def make_xo_dict(x_half_width, radius, box_half_width, jitter, id=-1):
    #get dot's cartesian coordinates
    x = np.random.uniform(low=-box_half_width, high=box_half_width)
    y = np.random.uniform(low=-box_half_width, high=box_half_width)
    #get dot's class
    dot_class = 'B'
    r = np.sqrt(x**2 + y**2)
    if (r < radius):
        dot_class = 'O'
    if (np.abs(x) < x_half_width) or (np.abs(y) < x_half_width):
        dot_class = 'X'
    #rotate coordinate system by 45 degrees
    rot_angle = np.pi/4.0
    c = np.cos(rot_angle)
    s = np.sin(rot_angle)
    xr =  x*c + y*s
    yr = -x*s + y*c
    #add gaussian noise aka jitter to dots' positions
    xn = xr + np.random.normal(scale=jitter)
    yn = yr + np.random.normal(scale=jitter)
    #compute dot's polar coordinates
    r = np.sqrt(xn**2 + yn**2)
    angle = np.arctan2(yn, xn)
    xo = {'id':id, 'x':xn, 'y':yn, 'r':r, 'angle':angle, 'class':dot_class}
    return xo

#generate dataframe containing N_dots records
import pandas as pd
def make_xo_df(N_dots, initial_id, x_half_width, radius, box_half_width, jitter):
    #generate list of xo dictionaries
    xo_list = []
    for id in initial_id + np.arange(N_dots):
        xo = make_xo_dict(x_half_width, radius, box_half_width, jitter, id=id)
        xo_list += [xo]
    #generate dataframe and initialize records' ids
    cols = ['id', 'x', 'y', 'r', 'angle', 'class']
    df = pd.DataFrame(data=xo_list)[cols]
    df.index.name = 'record'
    #class scores
    df['X_score'] = 0.0
    df['O_score'] = 0.0
    df['B_score'] = 0.0
    df.loc[df['class'] == 'X', 'X_score'] = 1.0
    df.loc[df['class'] == 'O', 'O_score'] = 1.0
    df.loc[df['class'] == 'B', 'B_score'] = 1.0
    return df

#rebalance XO dataset so that all classes are equally represented
def rebalance_df(df, X_boost=None):
    num_class = df.groupby('class')['id'].count()
    num_O = num_class.min()
    num_B = num_O
    num_X = num_O
    if (X_boost):
        num_X = num_class['X']
        num_O = int(num_X/X_boost)
        num_B = num_O
    df_O = df[df['class'] == 'O'].sample(n=num_O)
    df_X = df[df['class'] == 'X'].sample(n=num_X)
    df_B = df[df['class'] == 'B'].sample(n=num_B)
    df = df_O.append(df_X).append(df_B)
    df['ran_num'] = np.random.uniform(size=len(df))
    df = df.sort_values('ran_num').reset_index(drop=True).drop(labels='ran_num', axis=1)
    return df
