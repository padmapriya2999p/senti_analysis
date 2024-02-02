#Using tkinter to get the file from the user and genearate a downloadable pdf document with graphical data

from tkinter import *
from tkinter import filedialog
import tkinter
from textblob import TextBlob
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages 
import time
from PIL import ImageTk, Image
import shutil 
import os 

global pdfpath
pdfpath='graph.pdf'
start_time = time.time()

def openFile():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\",title="Open Review File",filetypes=(("CSV Files","*.csv"),))
    
    # Read the input .csv file
    global df1
    df1=pd.read_csv(filepath)
    
    window.destroy()
    analyze_fn(df1)
  

# To download file 
def download_file(): 
    # Ask the user for the destination file path
    destination_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

    if destination_path:
        # Copy the file to the selected destination
        shutil.copy(pdfpath, destination_path)
        tkinter.messagebox.showinfo("Download Complete", "File downloaded successfully.")
        window.destroy()

def create_window(first_run):
    global pdfpath
    global window

    window = Tk()
    window.geometry("500x400")
    window.title("Welcome to KG Coders")

    # Widgets
    label = Label(window, text='Sentiment Analysis', font=("Helvetica", 16), width=30, background='cadetblue')
    label.config(highlightbackground="cadetblue4", highlightthickness=4)
    label.pack()

    img = ImageTk.PhotoImage(Image.open("img.png"))
    image_label = Label(window, image=img)
    image_label.pack()

    if first_run:
        # Button to open file
        open_button = Button(window, text="Choose File", font=("Helvetica", 16), background='antiquewhite4', command=openFile)
        open_button.place(relx=0.5, rely=0.6, anchor=CENTER)

        label1 = Label(window, text='Please choose your file for analysis', font=("Georgia", 12), width=30, background='cornflowerblue')
        label1.config(highlightbackground="cadetblue4", highlightthickness=2)
        label1.place(relx=0.5, rely=0.7, anchor=CENTER)
    else:
        # Button to trigger file download (Note: 'pdfpath' needs to be defined before calling this function)
        download_button = Button(window, text="Download File", font=("Helvetica", 16), background='antiquewhite4',
                                 command=download_file)
        download_button.place(relx=0.5, rely=0.6, anchor=CENTER)

        label2 = Label(window, text='Please download your file. Thankyou :)', font=("Georgia", 12), width=30, background='cornflowerblue')
        label2.config(highlightbackground="cadetblue4", highlightthickness=2)
        label2.place(relx=0.5, rely=0.7, anchor=CENTER)

    window.mainloop()

def analyze_fn(df1):
        #Determining the Polarity 
    
    for ind, row in df1.iterrows():
        #for i in df1['reviewText'].head(5):
        
        p_1 = TextBlob(row['reviewText']).sentiment.polarity
        
        #adding new feedback column in the dataframe (1 as positive and 0 as negative)
        if(0<=p_1<=1):
            #p_1=1
            df1.loc[ind,"feedback"] = 1
        elif(-1<=p_1<0):
            #p_1=0
            df1.loc[ind,"feedback"] = 0
        else:
            df1.loc[ind,"feedback"] = None
    
    #copying the dataframe into a .csv file 
    df3=df1.to_csv('output.csv')
    
    #comparing input and output file reviews
    
    # Adding the no. of positive and negative feedback from the customer  
    count1 = df1['Positive'].value_counts()
    print("The sum of positive and negative feedback in input:",count1)
    
    count2 = df1['feedback'].value_counts()
    print("The sum of positive and negative feedback in output:",count2)
    
    #The percentage of positive and negative feedback
    freq1 = df1['Positive'].value_counts(normalize=True)
    print("Positive and Negative percentage in input:",freq1*100)
    
    freq2 = df1['feedback'].value_counts(normalize=True)
    print("Positive and Negative percentage in output:",freq2*100)
    
    #conerting the result into a pdf 
    #pdfpath='graph.pdf'
    with PdfPages(pdfpath) as pdfFile:
        #Preparing Graph for visual 
        fig, ax1 = plt.subplots(figsize=(11,6))
        ax1.plot(df1.index,df1['Positive'],color="blue")
        ax2=ax1.twinx()
        ax2.plot(df1.index,df1['feedback'],color="green")
        plt.xlim( 0, 99)
        #plt.show()
        
        #styling the graph
        ax1.set_title("Feedback comparision of first 100 reviews from input and output")
        ax1.set_xlabel("First 100 positive and negative feedback")
        ax1.set_ylabel("input vs output")
        fig.tight_layout(pad=4)
        pdfFile.savefig(fig)
        plt.close()
        
        fig, ax3 = plt.subplots(figsize=(11,6))
        x_bar=[0,1]
        y_bar=list(count1)
        color=['purple','pink']
        ax3.bar(x_bar,y_bar,color=color,width=0.2)
        ax3.set_title("Showing count of positive and negative reviews from input")
        ax3.set_xlabel("Ratio of positive and negative feedback of input review")
        ax3.set_ylabel("Count")
        #plt.show()
        pdfFile.savefig(fig)
        plt.close()
    
    
create_window(True)
create_window(False)

end_time=time.time()
print('Query complete. Execution time is %s sec/s.'%(round(end_time-start_time)))