#Using tkinter to get the file from the user and genearate a downloadable pdf document with graphical data

from tkinter import *
from tkinter import filedialog,messagebox
import tkinter
from textblob import TextBlob
import pandas as pd 
#import matplotlib.pyplot as plt  
import time
#from PIL import ImageTk, Image
import os 
from wordcloud import WordCloud
import zipfile
import emoji 

#start_time = time.time()

def openFile():
    #to get the input file
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\",title="Open Review File",filetypes=(("CSV Files","*.csv"),))
    
    # Read the input .csv file
    global df1
    df1=pd.read_csv(filepath)
    
    #window.destroy()
    
  
def submit_fn():
    global input1
    #to get the review column name from the user
    input1 = txt_input.get()
    #print(input1)
    #to close window
    window.destroy()
    analyze_fn()

# To download file 
def download_file(): 

    # Prompt the user to select a destination folder
    destination_folder = filedialog.askdirectory()
    if destination_folder:

        # Save WordCloud images as PNG files
        positive_wordcloud.to_file("positive_wordcloud.png")
        negative_wordcloud.to_file("negative_wordcloud.png")

        # Read PNG files
        with open("positive_wordcloud.png", "rb") as f:
            positive_img_data = f.read()

        with open("negative_wordcloud.png", "rb") as f:
            negative_img_data = f.read()

        # Create a dictionary to store CSV data
        csv_data = {
            'review_rating.csv': df1.to_csv(index=False).encode('utf-8'),
            'postive_review.csv': df2.to_csv(index=False).encode('utf-8'),
            'negative_review.csv': df3.to_csv(index=False).encode('utf-8'),
            'positive_wordcloud.png': positive_img_data,
            'negative_wordcloud.png': negative_img_data
        }
        
        # Write CSV data directly to zip file
        with zipfile.ZipFile(destination_folder + '/report.zip', 'w') as zipf:
            for filename, data in csv_data.items():
                zipf.writestr(filename, data)

        # Remove temporary files
        os.remove("positive_wordcloud.png")
        os.remove("negative_wordcloud.png")

        messagebox.showinfo("Download Complete", "File downloaded successfully.")

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

    labl = Label(window, text=f'{emoji.emojize(":grinning_face:")} {emoji.emojize(":expressionless_face:")} {emoji.emojize(":disappointed_face:")}', font=("Helvetica", 50), bg='yellow')
    labl.config(highlightbackground="antiquewhite4", highlightthickness=4)
    labl.place(relx=0.5, rely=0.3, anchor=CENTER)

    #img = ImageTk.PhotoImage(Image.open("img.png"))
    #image_label = Label(window, image=img)
    #image_label.pack()

    if first_run:
        # Button to open file
        open_button = Button(window, text="Choose File", font=("Helvetica", 10), background='antiquewhite4', command=openFile)
        open_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        global txt_input
        txt_input=Entry(window,width=30)
        txt_input.config(highlightbackground="antiquewhite4", highlightthickness=2)
        txt_input.place(relx=0.5, rely=0.6, anchor=CENTER)

        label3 = Label(window, text='Please enter your review column name', font=("Times", 8,"bold"))
        label3.place(relx=0.5, rely=0.67, anchor=CENTER)

        open_button = Button(window, text="Submit", font=("Helvetica", 10), background='antiquewhite4', command=submit_fn)
        open_button.place(relx=0.5, rely=0.75, anchor=CENTER) 

    else:
        # Button to trigger file download (Note: 'pdfpath' needs to be defined before calling this function)
        download_button = Button(window, text="Download File", font=("Helvetica", 16), background='antiquewhite4',
                                 command=download_file)
        download_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        label2 = Label(window, text='Please download your file. Thankyou :)', font=("Georgia", 8), background='cornflowerblue')
        label2.config(highlightbackground="cadetblue4", highlightthickness=2)
        label2.place(relx=0.5, rely=0.6, anchor=CENTER)

        positive_count = "The total positive feedback : "+str(len(df2.axes[0]))
        #print("The sum of positive feedback in input:",positive_count)

        neg_count = "The total negative feedback : "+str(len(df3.axes[0]))
        #print("The sum of negative feedback in input:",neg_count)  

        label2 = Label(window, text=positive_count,font=("Helvetica", 10,"bold"), width=30)
        #label2.config(highlightbackground="cadetblue4", highlightthickness=2)
        label2.place(relx=0.5, rely=0.7, anchor=CENTER)

        label2 = Label(window, text=neg_count, font=("Helvetica", 10,"bold"), width=30)
        #label2.config(highlightbackground="cadetblue4", highlightthickness=2)
        label2.place(relx=0.5, rely=0.8, anchor=CENTER)

    window.mainloop()

def analyze_fn():
    #print(df1.head(5))
    #print(input1)
    
    # Separate positive and negative reviews
    positive_reviews = []
    negative_reviews = []

    #Determining the Polarity
    for ind, row in df1.iterrows():
        #for i in df1['reviewText'].head(5):
        
        p_1 = TextBlob(row[input1]).sentiment.polarity
        
        #adding new feedback column in the dataframe (1 as positive and 0 as negative)
        if(0<=p_1<=1):
            #p_1=1
            df1.loc[ind,"feedback"] = 1
            positive_reviews.append(df1.loc[ind,:])
        elif(-1<=p_1<0):
            #p_1=0
            df1.loc[ind,"feedback"] = 0
            negative_reviews.append(df1.loc[ind,:])
        else:
            df1.loc[ind,"feedback"] = None
    
    #copying the dataframe into a .csv file 
    #df1.to_csv('output.csv')
    global df2
    df2=pd.DataFrame(positive_reviews) 
    #df2.to_csv('positive_reviews.csv')
    global df3
    df3=pd.DataFrame(negative_reviews) 
    #df3.to_csv('negative_reviews.csv')

    # Generate word clouds for positive and negative reviews (with error handling)
    if positive_reviews:
        positive_text = ' '.join(str(review) for review in df2[input1])
        global positive_wordcloud
        positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_text)
        #plt.figure(figsize=(12, 6))
        #plt.subplot(1, 2, 1)
        #plt.imshow(positive_wordcloud, interpolation='bilinear')
        #plt.title('Positive Reviews Word Cloud',fontsize='20',color='green',pad=50)
        #plt.axis('off')
    else:
        print("No positive reviews to generate word cloud.")
    
    if negative_reviews:
        negative_text = ' '.join(str(review) for review in df3[input1])
        global negative_wordcloud
        negative_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_text)
        #plt.subplot(1, 2, 2)
        #plt.imshow(negative_wordcloud, interpolation='bilinear')
        #plt.title('Negative Reviews Word Cloud',fontsize='20',color='red',pad=50)
        #plt.axis('off')
    else:
        print("No negative reviews to generate word cloud.")
    
    #aspect based analysis
    #need to proceed

print("Welcome to KG Coders")
print("Please Wait")
create_window(True)
print("Thank You for your patience")
create_window(False)

#end_time=time.time()
#print('Query complete. Execution time is %s sec/s.'%(round(end_time-start_time)))
print("Thank You for your time and support")