
import json

def generateJSON(df,type,name):
    
    
    
    with open("name.json", "w") as outfile:
        outfile.write("")
    if (type.lower=="chatgpt"):
        defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
        defaultMessage+=f"Your name is Bot1 and your age is between {df['AgeRange'][0]} with the mental illness: {df['MentalIllness'][0]}"
        
        for index in range(len(df)-1):
            
            messageList=[]
            tempMessageDict = {"role": "system", "content": defaultMessage}
            messageList.append(tempMessageDict)
        
            
            tempMessageDict = {"role": "user", "content": df['TherapistText'][index]}
            if df['TherapistText'][index]=="X":
                tempMessageDict['weight']=0
            messageList.append(tempMessageDict)
            tempMessageDict = {"role": "assistant", "content": df['ClientText'][index+1]}
            if df['ClientText'][index+1]=="X":
                tempMessageDict['weight']=0
            messageList.append(tempMessageDict)
            
            openaiMessage = {"messages":messageList}
            with open("fine-tuning.json", "a") as outfile: 
                outfile.write(json.dumps(openaiMessage) + "\n")
        return(defaultMessage)
    elif (type.lower=='gemini'):
        for index in range(len(df)-1):
            
            messageList=[]
            tempMessageDict = {"text_input": df['TherapistText'][index], "output": df['ClientText'][index+1]}
            messageList.append(tempMessageDict)
            
            with open("fine-tuning.json", "a") as outfile: 
                outfile.write(json.dumps(messageList) + ",\n")
        