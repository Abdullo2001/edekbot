import numpy as np
import matplotlib.pyplot as plt

fig_background_color = 'skyblue'
fig_border = 'skyblue'
# data =  [
#             [         'India', 'China', 'Russia', 'USA', 'Australia'],
#             [ '1980',  696828385,982372466,  138257420,  223140018,  14706322],
#             ['1990',  870452165, 1153704252,  148005704,   248083732, 17048003],
#             ['2000',  1059633675,  1264099069,  146844839,  282398554, 19017963],
#             ['2010',  1240613620,  1348191368,  143242599,  311182845, 22019168],
#             ['2020', 1396387127, 1424929781, 145617329,  335942003,  25670051],
#         ]
def chizma(msg,data,title_text):
    #the headers from the data array
    column_headers = data.pop(0)
    row_headers = [x.pop(0) for x in data]

    cell_text = []
    for row in data:
        cell_text.append([f'{x}' for x in row])


    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.01))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.01))

    #Creating the figure. Setting a small pad on the tight layout

    plt.figure(linewidth=1,
            edgecolor=fig_border,
            facecolor=fig_background_color,
            tight_layout={'pad':1})

    #Adding a table at the bottom of the axes

    the_table = plt.table(cellText=cell_text,
                        rowLabels=row_headers,
                        rowColours=rcolors,
                        rowLoc='left',
                        colColours=ccolors,
                        colLabels=column_headers,
                        loc='center')

    # Scaling influences the top and bottom cell padding.
    the_table.scale(1, 1.5)

    # Hiding axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Hiding axes border
    plt.box(on=None)
    

    plt.suptitle(title_text)

    # Without plt.draw() here, the title will center on the axes and not the figure.
    plt.draw()

    # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
    fig = plt.gcf()
    plt.savefig(f'{msg.chat.id}.png',
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                dpi=150
                )