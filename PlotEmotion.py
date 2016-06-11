import matplotlib.pyplot as plt
#######plot
def plotEmotions(plotBuffer):
        color_sequence = ['#aec7e8','#d62728','#c49c94','#2ca02c','#c7c7c7','#1f77b4','#9467bd','#ff7f0e']
        emotions = ['Neutral','Anger','Contempt','Disgust','Fear','Happy','Sadness','Surprise']

        fig, ax = plt.subplots(1, 1, figsize=(12, 9),facecolor='#eeeeee')

# Remove the plot frame lines. They are unnecessary here.
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
# Ticks on the right and top of the plot are generally unnecessary.
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
# Avoid unnecessary whitespace.
        plt.xlim(0, len(plotBuffer[0])*0.5)
        plt.ylim(-0.25, 1.20)

# Make sure your axis ticks are large enough to be easily read.
# You don't want your viewers squinting to read your plot.
#plt.xticks(range(1970, 2011, 10), fontsize=14)
        plt.yticks(range(0, 101, 10), ['{0}%'.format(x)
                                      for x in range(0, 101, 10)], fontsize=14)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
        for y in range(0, 101, 10):
            plt.plot(range(0, 1000,20), [y] * len(range(0, 1000,20)), '--',
                     lw=0.5, color='black', alpha=0.3)

        plt.title('Emotion Scores', fontsize=18, ha='center')

######

        for rank, column in enumerate(emotions):

            line = plt.plot( [ e*0.5 for e in range(len(plotBuffer[rank]))],
                            [elem*100 for elem in plotBuffer[rank]],
                            lw=2.5,
                            color=color_sequence[rank])

    # Add a text label to the right end of every line. Most of the code below
    # is adding specific offsets y position because some labels overlapped.
            y_pos = plotBuffer[rank][-1]*100-1

    # Again, make sure that all labels are large enough to be easily read
    # by the viewer.
            plt.text(len(plotBuffer[0])*0.5, y_pos , column, fontsize=14, color=color_sequence[rank])
        
        plt.show()
#######