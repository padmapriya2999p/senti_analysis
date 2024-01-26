from textblob import TextBlob
import pandas as pd 


df1=pd.read_csv(r'E:\Programming\vscode_python\senti_analysis\input.csv')
df2=pd.read_csv(r'E:\Programming\vscode_python\senti_analysis\data.csv')

#Determining the Polarity 
for ind, row in df1.iterrows():
    #for i in df1['reviewText'].head(5):
    
    p_1 = TextBlob(row['reviewText']).sentiment.polarity
    
    if(0<=p_1<=1):
        #p_1=1
        df1.loc[ind,"feedback"] = 1
    elif(-1<=p_1<0):
        #p_1=0
        df1.loc[ind,"feedback"] = 0
    else:
        df1.loc[ind,"feedback"] = None

df3=df1.to_csv('output.csv')

# Compare DataFrames
are_equal = df1['feedback'].equals(df2['Positive'])

if not are_equal:
    # Find Percentage Difference
    percentage_difference = (abs(df1['feedback'] - df2['Positive'])) * 100
    
    
    #print("Percentage Difference:")
    #print(percentage_difference)
else:
    print("DataFrames are equal.") 

sum=0
for i in percentage_difference:
    sum+=i
print(sum)
print("The overall percentage difference between sample and output is", (sum/df1['feedback'].count()))

