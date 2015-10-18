import pandas as pd
import numpy as np
import scipy.stats as stats
df = pd.read_csv('stroopdata.csv')
df

mean_con = df['Congruent'].mean()
mean_con
mean_incon = df['Incongruent'].mean()

mode_con = df['Congruent'].mode()
mode_con
mode_incon = df['Incongruent'].mode()

std_con = df['Congruent'].std()
std_con
std_incon = df['Incongruent'].std()

med_con = df['Congruent'].median()
med_incon = df['Incongruent'].median()
med_con
mean_con
mean_incon
med_incon
std_incon

import matplotlib.pyplot as plt
plt.hist(df['Congruent'], histtype = 'bar')
plt.show()

plt.hist(df['Incongruent'], histtype = 'bar')
plt.show()