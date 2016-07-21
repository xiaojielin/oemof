# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# global plotting options
plt.rcParams.update(plt.rcParamsDefault)
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 1.2
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 10})
plt.rcParams['image.cmap'] = 'Spectral'

# read file
df_raw = pd.read_csv('results/results_dispatch_prices_DE_nep_2014_aggr.csv')
df_raw.head()
df_raw.columns


# prepare dataframe for fit
residual_load = df_raw['DE_load'] + df_raw['AT_load'] + df_raw['LU_load'] - \
                df_raw['DE_wind'] - df_raw['AT_wind'] - df_raw['LU_wind'] - \
                df_raw['DE_solar'] - df_raw['AT_solar'] - df_raw['LU_solar']
df_polyfit = pd.concat([residual_load, df_raw['eex_day_ahead_2014'],
                       df_raw['power_price_model']], axis=1)
df_polyfit.columns = ['res_load', 'price_real', 'price_model']

# fit polynom of 3rd degree
z = np.polyfit(df_polyfit['res_load'], df_polyfit['price_real'], 3)
p = np.poly1d(z)

# save and plot results
df_polyfit['price_regression_res_load'] = p(df_polyfit['res_load'])

p2 = np.poly1d(np.polyfit(df_polyfit['price_model'],
                          df_polyfit['price_real'], 2))

# show values
df_polyfit.plot(kind='scatter', x='res_load', y='price_real')
df_polyfit.plot(kind='scatter', x='price_model', y='price_real')


df_polyfit['price_regression_price_model'] = p2(df_polyfit['price_real'])

df_polyfit[0:24*31][['price_real',
                     'price_model']].plot(linewidth=1.2, subplots=True,
                                          drawstyle='steps', ylim=[-100, 100])

df_polyfit[0:24*31][['price_real',
                     'price_regression_res_load']].plot(linewidth=1.2,
                                                        subplots=True,
                                                        drawstyle='steps',
                                                        ylim=[-100, 100])

df_polyfit[0:24*31][['price_real',
                     'price_regression_price_model']].plot(linewidth=1.2,
                                                           subplots=True,
                                                           drawstyle='steps',
                                                           ylim=[-100, 100])

df_bla = pd.DataFrame(p2(range(10, 80, 1)))
df_bla.plot()
plt.show()
