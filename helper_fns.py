#helper_fns.py
#
#by Joe Hahn
#joe.hahn@oracle.com
#3 July 2018
#
#these helper functions are called by something.ipynb

import numpy as np
rn_state = np.random.RandomState(seed=rn_seed)
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

import pandas as pd
def make_xo_df(N_dots, initial_id, x_half_width, radius, box_half_width, jitter, rn_seed, debug=debug):
    
    #generate dataframe and initialize records' ids
    df = pd.DataFrame()
    df.index.name = 'idx'
    df['id'] = initial_id + np.arange(N_dots)
    
    #generate random x,y positions
    rn_state = np.random.RandomState(seed=rn_seed)
    df['x'] = np.random.uniform(low=-box_half_width, high=box_half_width, size=N_dots)
    df['y'] = np.random.uniform(low=-box_half_width, high=box_half_width, size=N_dots)
    df['r'] = np.sqrt(df.x**2 + df.y**2)

    #classify dots as members of X, O, or B=background classes
    df['class'] = 'B'
    idx = df['r'] < radius
    df.loc[idx, 'class'] = 'O'
    idx = (df.x.abs() < x_half_width) | (df.y.abs() < x_half_width)
    df.loc[idx, 'class'] = 'X'
    idx_x = df['class'] == 'X'
    idx_o = df['class'] == 'O'
    idx_not = df['class'] == 'B'
    
    #class scores
    df.loc[idx_x, 'Xscore'] = 1.0
    df.loc[idx_x, 'Oscore'] = 0.0
    df.loc[idx_x, 'Bscore'] = 0.0
    df.loc[idx_o, 'Xscore'] = 0.0
    df.loc[idx_o, 'Oscore'] = 1.0
    df.loc[idx_o, 'Bscore'] = 0.0
    df.loc[idx_not, 'Xscore'] = 0.0
    df.loc[idx_not, 'Oscore'] = 0.0
    df.loc[idx_not, 'Bscore'] = 1.0

    #rotate coordinate system by 45 degrees = pi/4 radians
    phi = np.pi/4.0
    c = np.cos(phi)
    s = np.sin(phi)
    df['xr'] =  df.x*c + df.y*s
    df['yr'] = -df.x*s + df.y*c
    
    #add gaussian noise/jitter to dots' (x,y) positions:
    df['xrn'] = df.xr + np.random.normal(scale=jitter, size=N_dots)
    df['yrn'] = df.yr + np.random.normal(scale=jitter, size=N_dots)
    
    #add a column of random numbers 
    df['ran_num'] = np.random.uniform(size=N_dots)
    if (debug):
        print df.head(5)
    
    #return selected columns
    cols = ['id', 'ran_num', 'class', 'Xscore', 'Oscore', 'Bscore', 'xr', 'yr', 'xrn', 'yrn']
    df_select = df[['id', 'ran_num', 'class', 'Xscore', 'Oscore', 'Bscore', 'xr', 'yr', 'xrn', 'yrn']]
    df_select.columns = ['id', 'ran_num', 'class', 'Xscore', 'Oscore', 'Bscore', 'x0', 'y0', 'x', 'y']
    if (debug):
        print df_select.head(5)
    return df_select
