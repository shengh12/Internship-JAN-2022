from tkinter import *
from matplotlib.pyplot import text
from numpy.core.multiarray import WRAP
from ttkthemes import themed_tk as tk
from tkinter import ttk
from tabs import Page
from tkinter import filedialog
import pandas as pd
from functions import *
from tkinter import messagebox

#create a new window and set parameters
window = tk.ThemedTk()
window.title('Data About Organization')
window.geometry('1230x500')

#list of tabs
list_of_categories = ['Org Info','Objectives' , 'Project Expenditure', 'Publicity', 'Experience Stories', 'Additional Info']

#create frame for tabs
frame_1 = Frame(window)
frame_1.pack()
tab_control = ttk.Notebook(frame_1)

org_info_tab = ttk.Frame(tab_control)
project_expenditure_tab = ttk.Frame(tab_control)
publicity_tab = ttk.Frame(tab_control)
experience_stories_tab = ttk.Frame(tab_control)
additional_info_tab = ttk.Frame(tab_control)
objectives_tab = ttk.Frame(tab_control)

list_of_tabs = [org_info_tab, objectives_tab , project_expenditure_tab, publicity_tab, experience_stories_tab, additional_info_tab]

for i in range (len(list_of_tabs)):
  tab_control.add(list_of_tabs[i], text=list_of_categories[i])
tab_control.pack(expand=1, fill='both')

#reading excel file data
#----------------------------------------
def read_rows_from_excel_file(file_path):
  df = pd.read_excel(file_path, engine='openpyxl', header=None)
  l = df.values.tolist()
  return l

def read_columns_from_excel_file(file_path, column_name):
  df = pd.read_excel(file_path)
  my_list = df[column_name].tolist()
  return my_list
#----------------------------------------

#the fun stuff
def prep_app():
  test_button = ttk.Button(org_info_tab, text='Select File', command= lambda: browse_file())
  test_button.pack()
  
  #opening the .xlsx file and translating each column into a list
  def browse_file():
    file_name = filedialog.askopenfilename(initialdir='/', title='select a file', filetypes=[('Excel files', '*.xlsx')])    
    list_1 = read_rows_from_excel_file(file_name)
    all_column_headings = list_1[0]
    test_button.destroy()
    data_list = []
    for heading in all_column_headings:
      l = read_columns_from_excel_file(file_name, heading)
      data_list_to_append = [heading, l]
      #print (data_list_to_append)
      data_list.append(data_list_to_append)
    
    #just some organization stuff so I don't have to keep writing data_list[#][#]
    organization_name_list = data_list[1][1]
    contact_person_list = data_list[2][1]
    title_list = data_list[3][1]
    phone_number_list = data_list[4][1]
    email_list = data_list[5][1]
    grant_title_list = data_list[6][1]
    grant_amount_list = data_list[7][1]
    award_date_list = data_list[8][1]
    timeline_list = data_list[9][1]
    project_overview_list = data_list[10][1]
    completed_objective_list = data_list[11][1]
    uncompleted_objective_list = data_list[12][1]
    unanticipated_successes_list = data_list[13][1]
    project_expenditure_list = data_list[14][1]
    publicity_list = data_list[15][1]
    experience_stories_list = data_list[16][1]
    additional_info_list = data_list[17][1]
    date_grant_completed_list = data_list[18][1]
    
    page_list = []
    
    #create different pages for each seperate organization
    #easier to track stuff
    for i in range (len(organization_name_list)):
      new_page = Page(organization_name=organization_name_list[i],contact_person=contact_person_list[i], title=title_list[i], phone_number=phone_number_list[i], email=email_list[i], grant_title=grant_title_list[i], grant_amount=grant_amount_list[i],award_date=award_date_list[i],timeline=timeline_list[i],project_overview=project_overview_list[i], completed_objectives=completed_objective_list[i], uncompleted_objective=uncompleted_objective_list[i], unanticipated_successes=unanticipated_successes_list[i], project_expenditure=project_expenditure_list[i],publicity=publicity_list[i],experience_stories=experience_stories_list[i],additional_information=additional_info_list[i],date_completed_report=date_grant_completed_list[i])
      
      page_list.append(new_page)
    
    #------------------------------------------------------
    #TABS STUFF
    switched_org_frame = ttk.Frame(org_info_tab)
    switched_org_frame.grid(row=0, columnspan=2)
    
    #created a new window called timeline window because the matplot graph keeps 
    #shrinking in the original tkinter window
    timeline_window = tk.ThemedTk()
    timeline_window.title('Project Timeline')
    
    #making sure that the user knows that if he/she quits out of the application, then 
    #the entire application quits since the app will crash if only one window quit
    def on_closing():
        if messagebox.askokcancel("Quit", "Quitting this will quit entire app."):
            timeline_window.destroy()
            window.destroy()

    timeline_window.protocol("WM_DELETE_WINDOW", on_closing)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    #default timeline for when the window first opens up
    #everything down from here is default. 
    first_timeline = transform_dates(page_list[0].timeline)       
    add_timeline_to_tab(timeline_window, first_timeline[1], first_timeline[0], page_list[0].title)
    
    about_project_frame = ttk.Frame(org_info_tab)
    about_project_frame.grid(row=1, column=0, sticky='w')
    project_overview_frame = ttk.Frame(org_info_tab)
    project_overview_frame.grid(row=1, column=1, sticky='E')
    
    def blank_box(row, column, window):
      blank = ttk.Label(window, text=' ')
      blank.grid(row=row, column=column)
    
    def insert_information(row, text_1, text_2, window):
      blank_box(row,0,window)
      placement_name_label = ttk.Label(window, text=text_1, font=('helvetica bold', 20))
      placement_name_label.grid(row=row, column=1, sticky='w')
      label_text = StringVar()
      label_text.set(text_2)
      placement_name_answer_label = ttk.Label(window,textvariable=label_text)
      placement_name_answer_label.grid(row=row, column=2)
      blank_box(0,4,window)
      return label_text
    
    def insert_blank_line(row, columnspan, window):
      placement_row = ttk.Label(window, text=' ')
      placement_row.grid(row=row, columnspan=columnspan)
      
    organization_label = insert_information(row=0, text_1='Organization Name:', text_2=page_list[0].organization_name, window=about_project_frame)
    
    insert_blank_line(row=1, columnspan=4, window=about_project_frame)
    
    contact_person_label = insert_information(row=2, text_1='Contact Person:', text_2=page_list[0].contact_person, window=about_project_frame)
    
    insert_blank_line(row=3, columnspan=4, window=about_project_frame)
                      
    title_label = insert_information(row=4, text_1='Project Title:', text_2=page_list[0].title, window=about_project_frame)
    
    insert_blank_line(row=5, columnspan=4, window=about_project_frame)
                      
    phone_number_label = insert_information(row=6, text_1='Phone Number:', text_2=page_list[0].phone_number, window=about_project_frame)
    
    insert_blank_line(row=7, columnspan=4, window=about_project_frame)
    
    email_label = insert_information(row=8, text_1='Organization Email:', text_2=page_list[0].email, window=about_project_frame)
    
    insert_blank_line(row=9, columnspan=4, window=about_project_frame)
    
    grant_title_label = insert_information(row=10, text_1='Grant Title:', text_2=page_list[0].grant_title, window=about_project_frame)
    
    insert_blank_line(row=11, columnspan=4, window=about_project_frame)
    
    grant_amount_label = insert_information(row=12, text_1='Grant Amount:', text_2=page_list[0].grant_amount, window=about_project_frame)
    
    insert_blank_line(row=13, columnspan=4, window=about_project_frame)
    
    award_date_label = insert_information(row=14, text_1='Award Date:', text_2=get_correct_award_date(str(page_list[0].award_date)), window=about_project_frame)
    
    insert_blank_line(row=15, columnspan=4, window=about_project_frame)
    
    report_complete_date_label = insert_information(row=16, text_1='Report Completed On:', text_2=get_correct_award_date(str(page_list[0].date_completed_report)), window=about_project_frame)
    
    project_overview_label = ttk.Label(project_overview_frame, text='Project Overview', font=('helvetica bold', 20))
    project_overview_label.grid(row=0, column=0, sticky='E')
    
    insert_blank_line(row=1, columnspan=1, window=project_overview_frame)
    
    project_overview_answer_frame = ttk.Frame(project_overview_frame)
    project_overview_answer_frame.grid(row=2, column=0)
    
    #very useful function. Creates a textbook widget in a particular window and 
    #now I don't have to keep creating textboxes for paragraphs. Just need to use 
    #this function
    def set_paragraph_view(text, window):
      label = Label(window)
      label.grid()
      p_text = tkinter.Text(label, wrap=WORD)
      p_text.grid(row=0, column=0)
      scrollbar = tkinter.Scrollbar(label, command=p_text.yview)
      p_text.config(yscrollcommand=scrollbar.set)
      scrollbar.grid(row=0, column=1, sticky=NSEW)
      p_text.insert(tkinter.END, text)
      p_text.configure(state='disabled')
      #need to change to #enabled to change text inside widget
      return p_text
    
    project_overview_answer_text = set_paragraph_view(page_list[0].project_overview, project_overview_answer_frame)
    
    #new label function for this specific frame
    def add_label(row, column, text_1, window, font_size):
      new_label = ttk.Label(window, text = text_1, font=('helvetica', font_size), wraplength=350, justify='left')
      new_label.grid(row=row, column=column, sticky='w', padx=(15))
      return new_label
    
    switch_org_obj_frame = ttk.Frame(objectives_tab)
    switch_org_obj_frame.grid(row=0, column=0)
    
    rest_frame = ttk.Frame(objectives_tab)
    rest_frame.grid(row=1, column=0)
    
    completed_obj_frame = ttk.Frame(rest_frame)
    completed_obj_frame.grid(row=0, column=0)
    uncompleted_obj_frame = ttk.Frame(rest_frame)
    uncompleted_obj_frame.grid(row=0, column=1)
    unanticipated_successes_frame = ttk.Frame(rest_frame)
    unanticipated_successes_frame.grid(row=0, column=2)
    
    completed_objectives_label = add_label(row=0, column=0, window=completed_obj_frame, text_1='Completed Objectives', font_size=20)
    insert_blank_line(row=1, columnspan=1, window=completed_obj_frame)
    default_completed_obj = get_objectives(page_list[0].completed_objectives)
    
    def add_label_to_frame(list_of_obj, window):
      for i in range (len(list_of_obj)):
        new_obj = list_of_obj[i]
        new_label = add_label(row=i+2, column=0, window=window, text_1=str(i+1) + '. ' + new_obj, font_size=14)

    add_label_to_frame(default_completed_obj, completed_obj_frame)
    
    uncompleted_objectives_label = add_label(row=0, column=0, window=uncompleted_obj_frame, text_1='Uncompleted Objectives', font_size=20)
    insert_blank_line(row=1, columnspan=1, window=uncompleted_obj_frame)
    default_uncompleted_obj = get_objectives(page_list[0].uncompleted_objective)
    
    add_label_to_frame(default_uncompleted_obj, uncompleted_obj_frame)
    
    unanticipated_label = add_label(row=0, column=0, window=unanticipated_successes_frame, text_1='Unanticipated Successes / Challenges', font_size=20)
    default_unanticipated_para = page_list[0].unanticipated_successes
    
    unanticipated_text = set_paragraph_view(text=default_unanticipated_para, window=unanticipated_successes_frame)
    
    project_expenditure_frame = ttk.Frame(project_expenditure_tab)
    project_expenditure_frame.grid(row=1, column=0)
    project_expenditure_buttons_frame = ttk.Frame(project_expenditure_tab)
    project_expenditure_buttons_frame.grid(row=0,column=0)
    projects = find_project_prices(page_list[0].project_expenditure)
    projects.insert(0, ['Project Title', 'Proposed Price', 'Actual Price'])
    
    def insert_project_labels(project_list):
      for i in range (len(project_list)):
        for j in range (len(project_list[0])):
          new_label = ttk.Label(project_expenditure_frame, text=projects[i][j], wraplength=350, font=('helvetica', 20))
          new_label.grid(row=i, column=j, sticky='', padx=(15))
          
    insert_project_labels(projects)
    
    def paragraph(window):
      buttons_frame = ttk.Frame(window)
      buttons_frame.grid(row=0, column=0)
      info_frame = ttk.Frame(window)
      info_frame.grid(row=1, column=0)
      default = page_list[0].publicity
      text = set_paragraph_view(text=default, window=info_frame)
      return [buttons_frame, text]
    
    publicity = paragraph(window=publicity_tab)
    experience_stories = paragraph(window=experience_stories_tab)
    additional_info = paragraph(window=additional_info_tab)
    
    clicked = StringVar()
    clicked.set(organization_name_list[0])
    
    def switch():
      new_org_name = clicked.get()
      clear_frame(timeline_window)
      for i in range (len(page_list)):
        if page_list[i].organization_name == new_org_name:
          new_timeline = transform_dates(page_list[i].timeline)
          add_timeline_to_tab(timeline_window, new_timeline[1], new_timeline[0], page_list[i].title)

          organization_label.set(page_list[i].organization_name)
          contact_person_label.set(page_list[i].contact_person)
          title_label.set(page_list[i].title)
          phone_number_label.set(page_list[i].phone_number)
          email_label.set(page_list[i].email)
          grant_title_label.set(page_list[i].grant_title)
          grant_amount_label.set(page_list[i].grant_amount)
          award_date_label.set(get_correct_award_date(str(page_list[i].award_date)))
          report_complete_date_label.set(get_correct_award_date(str(page_list[i].date_completed_report)))
          
          def change_text(text, text_widget):
            text_widget.configure(state='normal')
            text_widget.delete(1.0, END)
            text_widget.insert(tkinter.END, text)
            text_widget.configure(state='disabled')
          
          change_text(text=page_list[i].project_overview,text_widget=project_overview_answer_text)
          
          completed_obj = get_objectives(page_list[i].completed_objectives)
          uncompleted_obj = get_objectives(page_list[i].uncompleted_objective)
          
          clear_frame(completed_obj_frame)
          clear_frame(uncompleted_obj_frame)
          
          completed_objectives_label = add_label(row=0, column=0, window=completed_obj_frame, text_1='Completed Objectives', font_size=20)
          insert_blank_line(row=1, columnspan=1, window=completed_obj_frame)
          complete_list = add_label_to_frame(completed_obj, completed_obj_frame)
                
          uncompleted_objectives_label = add_label(row=0, column=0, window=uncompleted_obj_frame, text_1='Uncompleted Objectives', font_size=20)
          insert_blank_line(row=1, columnspan=1, window=uncompleted_obj_frame)
          uncomplete_list = add_label_to_frame(uncompleted_obj, uncompleted_obj_frame)
          
          change_text(text=page_list[i].unanticipated_successes,text_widget=unanticipated_text)
          
          clear_frame(project_expenditure_frame)
          new_projects = find_project_prices(page_list[i].project_expenditure)
          new_projects.insert(0, ['Project Title', 'Proposed Price', 'Actual Price'])
          insert_project_labels(new_projects)

          change_text(text=page_list[i].publicity,text_widget=publicity[1])
          change_text(text=page_list[i].experience_stories, text_widget=experience_stories[1])
          change_text(text=page_list[i].additional_information, text_widget=additional_info[1])
          
    def set_button_on_window(window):
      org_drop_menu = OptionMenu(window, clicked, *organization_name_list)
      org_drop_menu.grid(row=0, column=0)
      org_drop_menu.config(width=50)
      
      switch_org_button = Button(window, text='Switch Orgs', command=lambda:switch()).grid(row=0, column=1)
      
    set_button_on_window(switched_org_frame)
    set_button_on_window(switch_org_obj_frame)
    set_button_on_window(project_expenditure_buttons_frame)
    set_button_on_window(publicity[0])
    set_button_on_window(experience_stories[0])
    set_button_on_window(additional_info[0])
    
    timeline_window.mainloop()
    
prep_app()

window.mainloop()    