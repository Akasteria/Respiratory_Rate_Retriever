import matplotlib.pyplot as plt
# Need to create as global variable so our callback(on_plot_hover) can access
fig = plt.figure()
plot = fig.add_subplot(111)
# create some curves
for i in range(4):
    # Giving unique ids to each data member
    plot.plot(
        [i*1,i*2,i*3,i*4],
        gid=i)
def on_plot_hover(event):
    # Iterating over each data member plotted
    for curve in plot.get_lines():
        # Searching which data member corresponds to current mouse position
        if curve.contains(event)[0]:
            print ("over %s" % curve.get_gid())
fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)           
plt.show()