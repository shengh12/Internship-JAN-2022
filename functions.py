import matplotlib.pyplot as plt
from datetime import date
import numpy as np
import tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()
      
def add_timeline_to_tab(tab, dates, labels, project_name):
    min_date = date(np.min(dates).year - 2, np.min(dates).month, np.min(dates).day)
    max_date = date(np.max(dates).year + 2, np.max(dates).month, np.max(dates).day)

    # labels with associated dates
    new_list = []
    for i in range (len(dates)):
        new_list.append(str(dates[i]) + ':\n' + labels[i])
    labels = new_list

    #labels = ['{0:%d %b %Y}:\n{1}'.format(d, l) for l, d in zip (labels, dates)]
    
    fig, ax = plt.subplots(figsize=(6, 1.5), constrained_layout=True)
    #bar1 = FigureCanvasTkAgg(fig, tab)
    #bar1.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    _ = ax.set_ylim(-2, 1.75)
    _ = ax.set_xlim(min_date, max_date)
    _ = ax.axhline(0, xmin=0.05, xmax=0.95, c='deeppink', zorder=1)

    _ = ax.scatter(dates, np.zeros(len(dates)), s=120, c='palevioletred', zorder=2)
    _ = ax.scatter(dates, np.zeros(len(dates)), s=30, c='darkmagenta', zorder=3)

    label_offsets = np.zeros(len(dates))
    label_offsets[::2] = 1.0
    label_offsets[1::2] = -1.4
    for i, (l, d) in enumerate(zip(labels, dates)):
        _ = ax.text(d, label_offsets[i], l, ha='center', fontfamily='serif', fontweight='bold', color='royalblue',fontsize=4.3)
        
    stems = np.zeros(len(dates))
    stems[::2] = 0.8
    stems[1::2] = -1.0  
    markerline, stemline, baseline = ax.stem(dates, stems, use_line_collection=True)
    _ = plt.setp(markerline, marker=',', color='darkmagenta')
    _ = plt.setp(stemline, color='darkmagenta')
                
    # hide lines around chart
    for spine in ["left", "top", "right", "bottom"]:
        _ = ax.spines[spine].set_visible(False)

    # hide tick labels
    _ = ax.set_xticks([])
    _ = ax.set_yticks([])

    _ = ax.set_title(project_name+ ' Timeline', fontweight="bold", fontfamily='serif', fontsize=9, color='royalblue')

    canvas = FigureCanvasTkAgg(fig, master = tab)  
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,tab)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

#----------------------------------------------------------------------------------------

def find_all_index_of_substring(string, substring):
    return_list = []
    for i in range (len(string)):
        if string[i] == substring:
            return_list.append(i)
    return return_list

def find_string_blocks(string):
    index = find_all_index_of_substring(string, '\n')
    index.insert(0,0)
    index.append(len(string))
    returned_blocks = []
    for i in range (len(index)-1):
        returned_blocks.append(string[index[i]:index[i+1]])
    return returned_blocks 

def clean_blocks(string):
    unclean_list = find_string_blocks(string)
    returned_list = []
    for i in range (len(unclean_list)):
        if unclean_list[i] == '\n':
            i+=1
        elif unclean_list[i][0] == '\n':
            unclean_list[i] = unclean_list[i][1:]
            returned_list.append(unclean_list[i])
        else:
            returned_list.append(unclean_list[i])
    return returned_list

def find_objectives_and_dates(string):
    block_list = clean_blocks(string)
    objectives = []
    dates = []
    for i in range (len(block_list)):
        found_index = block_list[i].find('-')
        new_objective = block_list[i][0:found_index-1]
        new_date = block_list[i][found_index+2:]
        objectives.append(new_objective)
        dates.append(new_date)
    return [objectives, dates]
    
def find_correct_dates(string):
    list_1 = find_objectives_and_dates(string)
    objective_list = list_1[0]
    dates_list = list_1[1]
    year_list = []
    month_list = []
    days_list = []
    for i in range (len(dates_list)):
        date = dates_list[i]
        index = find_all_index_of_substring(date,'/')
        index.insert(0, -1)
        index.append(len(date)-2)
        month = date[index[0]+1:index[1]]
        day = date[index[1]+1: index[2]]
        year = date[index[2]+1:]
        year_list.append(year)
        month_list.append(month)
        days_list.append(day)
    return [objective_list,year_list,month_list,days_list]

def transform_dates(string):
    list_1 = find_correct_dates(string)
    year_list = list_1[1]
    month_list = list_1[2]
    day_list = list_1[3]
    dates = []
    for i in range (len(year_list)):
        new_date = date(int(year_list[i]),int(month_list[i]),int(day_list[i]))
        dates.append(new_date)
    return [list_1[0], dates]

def get_correct_award_date(string):
    index = string.find(' ')
    date = string[0:index]
    return date.strip()

def get_objectives(string):
    str_1 = ',.<>?/:;[]|-_+=()*&^%$#@!~`'
    if string[-1] in str_1:
        string = string[0:len(string)-1]
    index = find_all_index_of_substring(string, ',')
    index.insert(0,-1)
    index.append(len(string))
    objectives = []
    for i in range (len(index)-1):
        comma_position = index[i]
        new_objective = string[comma_position+1:index[i+1]]
        objectives.append(new_objective)
    for i in range (len(objectives)):
        found_objective = objectives[i]
        if found_objective[0] == ' ':
            objectives[i] = objectives[i][1:]
    return objectives

def get_correct_project(string):
    string = string.strip()
    index = find_all_index_of_substring(string, substring='\n')
    index.insert(0,-1)
    index.append(len(string))
    projects = []
    for i in range(len(index)-1):
        new_project = string[index[i]+1:index[i+1]]
        projects.append(new_project)
    return projects

def find_project_prices(string):
    projects = get_correct_project(string)
    projects_strips = []
    correct_projects = []
    for i in range (len(projects)):
        new_projects = projects[i].split()
        projects_strips.append(new_projects)
    
    for i in range (len(projects_strips)):
        about_project = projects_strips[i]
        about_project.pop(-2)
        about_project.pop(-3)
        new_project_string = ''
        for j in range (len(about_project)-2):
            if j == len(about_project)-3:
                new_project_string+=about_project[j]
            else:
                new_project_string+=about_project[j] + ' '
        correct_projects.append([new_project_string, about_project[-2], about_project[-1]])
    return correct_projects
                                    