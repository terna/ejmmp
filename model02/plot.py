import matplotlib.pyplot as plt
import commonVar as cmv

def plot(y1lim,y1values,y11abel,y2lim,y2values,y2label):
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor0 = 'tab:green'
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig, ax1 = plt.subplots()
    ax1.set_ylim(y1lim)
    t=range(1,cmv.ncycles+1)
    ax1.plot(t, y1values, label=y11abel, color=myColor1)
    ax1.tick_params(axis='y', labelcolor=myColor1)
    ax1.plot([1,cmv.ncycles],[0,0], label="zero line", color=myColor0, linestyle='dashed')

    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylim(y2lim)
    ax2.plot(t, y2values, label=y2label, color=myColor2)
    ax2.tick_params(axis='y', labelcolor=myColor2)
    fig.legend()
    plt.show()
