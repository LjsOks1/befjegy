import matplotlib.dates as mdates
import matplotlib.pyplot as plt


class graph:
    lines=[]
    lined=dict()
    legend_vis=True
    def __init__(self,label):
        self.fig,self.ax=plt.subplots(1)
        self.fig.suptitle(label.decode('utf8'), fontsize=14, fontweight='bold')
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
#        if data is not None:
#            self.show(data)

    def onpress(self,event):
        print('press',event.key)
        if event.key=='l':
            if self.legend_vis==True:
                self.legend.set_visible(False)
                self.legend_vis=False
            else:
                self.legend.set_visible(True)
                self.legend_vis=True
            self.fig.canvas.draw()

    def onpick(self,event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        legline = event.artist

#        origline = self.lined[legline]
#        vis = not origline.get_visible()
#        origline.set_visible(vis)
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
 #       if vis:
 #           legline.set_alpha(1.0)
 #       else:
 #           legline.set_alpha(0.0)

        xdata=event.mouseevent.xdata
        ydata=event.mouseevent.ydata


        self.fig.canvas.draw()

    def show(self,data):
        for key,x in data.iteritems():
            line,=self.ax.plot( x[0],x[1],label=key)
            self.lines.append(line)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y %m/%d'))
        self.legend = self.ax.legend(loc='upper left', fancybox=True, shadow=True)

        for legline, origline in zip(self.legend.get_lines(), self.lines):
            legline.set_picker(5)  # 5 pts tolerance
            self.lined[legline] = origline

        self.legend.get_frame().set_alpha(0.4)    
        plt.grid()
        plt.show()

    def show_hist(self,data):
        for key,x in data.iteritems():
            line= plt.hist(x,bins=100,histtype="step",cumulative=-1,normed=True,label=key.decode('utf8'))
            self.lines.append(line)
        self.legend = self.ax.legend(loc='upper left', fancybox=True, shadow=True)

        for legline, origline in zip(self.legend.get_lines(), self.lines):
            legline.set_picker(5)  # 5 pts tolerance
            self.lined[legline] = origline

        self.legend.get_frame().set_alpha(0.4)    
        plt.grid()
        plt.show()

    def show_scatter(self,data):
        mn=[]
        std=[]
        lbl=[]
        for key,x in data.iteritems():
            mn.append(x[0])
            std.append(x[1])
            lbl.append(key) if key is not None else lbl.append("")
        sc=self.ax.scatter( mn,std,label=lbl,picker=5)
        for i, txt in enumerate(lbl):
            self.ax.annotate(txt[-6:], (mn[i],std[i]))
        plt.grid()
        plt.show()
    
    def show_boxplot(self,data):
        self.ax.boxplot(data.values())
        self.ax.set_ylim([-0.1, 0.5])
        plt.grid()
        for i in range(1,len(data.keys())+1):
            self.ax.text(i-0.5,0,data.keys()[i-1],rotation='vertical',verticalalignment='bottom')
        #plt.xticks(range(1,len(data.keys())+1), data.keys(),rotation='vertical')
        plt.show()
