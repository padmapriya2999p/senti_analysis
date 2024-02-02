#Python script to analyse the positive and negative feedback from the customers and generate an output

from textblob import TextBlob
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages 
import time

start_time = time.time()

# Read the input .csv file
df1=pd.read_csv(r'E:\Programming\vscode_python\senti_analysis\data.csv')

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
with PdfPages('graph.pdf') as pdfFile:
    #Preparing Graph for visual 
    fig, ax1 = plt.subplots(figsize=(11,6))
    ax1.plot(df1.index,df1['Positive'],color="blue")
    ax2=ax1.twinx()
    ax2.plot(df1.index,df1['feedback'],color="green")
    plt.xlim( 0, 99)
    plt.show()
    
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
    plt.show()
    pdfFile.savefig(fig)
    plt.close()

end_time=time.time()
print('Query complete. Execution time is %s sec/s.'%(round(end_time-start_time)))
