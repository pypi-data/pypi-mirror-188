# -*- coding: utf-8 -*-
# file: test.py
# time: 15/03/2022
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import numpy as np
from metric_visualizer import MetricVisualizer

MV = MetricVisualizer()

trial_num = 5  # number of different trials,
repeat = 10  # number of repeats
metric_num = 3  # number of metrics

for trial in range(trial_num):
    for r in range(repeat):  # repeat the experiments to plot violin or box figure
        metrics = [(np.random.random() + n) for n in range(metric_num)]  # n is metric scale factor
        for i, m in enumerate(metrics):
            MV.add_metric('Metric-{}'.format(i + 1), round(m, 2))
    MV.next_trial()

save_path = None
MV.summary(save_path=save_path)  # save fig into .tex and .pdf format
MV.traj_plot(save_name=save_path, xlabel='Trials')  # save fig into .tex and .pdf format
MV.violin_plot(save_name=save_path)  # save fig into .tex and .pdf format
MV.box_plot(save_name=save_path)  # save fig into .tex and .pdf format
MV.avg_bar_plot(save_name=save_path)  # save fig into .tex and .pdf format
MV.sum_bar_plot(save_name=save_path)  # save fig into .tex and .pdf format

save_path = 'example'
MV.traj_plot(save_name=save_path, xlabel='Trials',
             xticks=['Trial-{}'.format(x + 1) for x in range(trial_num)])  # show the fig via matplotlib
MV.violin_plot(save_name=save_path, xlabel='Trials',
               xticks=['Trial-{}'.format(x + 1) for x in range(trial_num)])  # show the fig via matplotlib
MV.box_plot(save_name=save_path, xlabel='Trials',
            xticks=['Trial-{}'.format(x + 1) for x in range(trial_num)])  # show the fig via matplotlib
MV.avg_bar_plot(save_name=save_path, xlabel='Trials',
                xticks=['Trial-{}'.format(x + 1) for x in range(trial_num)])  # save fig into .tex and .pdf format
MV.sum_bar_plot(save_name=save_path, xlabel='Trials',
                xticks=['Trial-{}'.format(x + 1) for x in range(trial_num)])  # save fig into .tex and .pdf format
