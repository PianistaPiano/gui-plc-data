import matplotlib.pyplot as plt
import matplotlib.widgets
import numpy as np
from matplotlib.widgets import Slider


def plotcurrentLevelAndSetPoint(x, y, xLabel, yLabel, chartLabel, y1):
    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.suptitle(chartLabel)
    plt.plot(x, y, y1)
    plt.grid(True)
    plt.legend(['Current Level', 'Set Point'], loc='best')


def plotAlarmsAndParams(x, y, y1, y2, y3, y4, xLabel, yLabel, yLabel2, chartLabel, chartLabel2,
                        y5, y6, y7):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.autofmt_xdate()
    ax1.plot(x, y, y1, y2, y3, y4)
    ax1.plot(x, y3, y4)
    ax1.set_title(chartLabel)
    ax1.grid()
    ax1.set_xlabel(xLabel)
    ax1.set_ylabel(yLabel)
    ax1.legend(['HH', 'H', 'L', 'LL', 'Valve problem'], loc='best')
    if len(y7) == 0:
        ax2.plot(x, y5, y6)
        ax2.legend(['Szerokość histerezy', 'P_Przekaźnik'], loc='best')
    else:
        ax2.plot(x, y5, y6, y7)
        ax2.plot(x, y7)
        if chartLabel.find("Zbiornik_2"):
            ax2.legend(['P', 'I', 'D'], loc='best')
        elif chartLabel.find("Zbiornik_3"):
            ax2.legend(['P', 'I', 'P_Przekaźnik'], loc='best')
    ax2.set_title(chartLabel2)
    ax2.grid()
    ax2.set_xlabel(xLabel)
    ax2.set_ylabel(yLabel2)

def plotDisFlowAndControl(x, y, y1, xLabel, yLabel, yLabel2, chartLabel, chartLabel2):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        fig.autofmt_xdate()
        ax1.plot(x, y)
        ax1.set_title(chartLabel)
        ax1.grid()
        ax1.set_xlabel(xLabel)
        ax1.set_ylabel(yLabel)
        ax1.legend(['Current Flow'], loc='best')

        ax2.plot(x, y1)
        ax2.set_title(chartLabel2)
        ax2.grid()
        ax2.set_xlabel(xLabel)
        ax2.set_ylabel(yLabel2)
        ax2.legend(['Current Control'], loc='best')

def showCharts():
    plt.show()
