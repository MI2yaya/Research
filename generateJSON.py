
import json

def generateJSON(df,type,name):
    
    
    
    
    
    defaultMessage = f"You are a factual chatbot which aims to replicate a simulated patient for use in training residents to become psychotherapists."
    defaultMessage+=f" Your name is Bot1 and your age is between {df['AgeRange'][0]} with the mental illness: {df['MentalIllness'][0]}"
    
    if (type.lower()=="chatgpt"):
        with open(f"{name}.json", "w") as outfile:
            outfile.write("")
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
            with open(f"{name}.json", "a") as outfile: 
                outfile.write(json.dumps(openaiMessage) + "\n")
        return(defaultMessage)
    elif (type.lower()=='vertex'):
        with open(f"{name}.jsonl", "w") as outfile:
            outfile.write("")
            for index in range(len(df) - 1): 

                systemInstruction = {
                    "role": "",
                    "parts": [{"text": defaultMessage}]
                }
                

                contents = [
                    {
                        "role": "user",
                        "parts": [{"text": df['TherapistText'][index]}]
                    },
                    {
                        "role": "model",
                        "parts": [{"text": df['ClientText'][index + 1]}]
                    }
                ]
                
                json.dump({"systemInstruction": systemInstruction, "contents": contents}, outfile)
                outfile.write("\n") 
        
        
    
    elif (type.lower()=='gemini'):
        with open(f"{name}.json", "w") as outfile:
            outfile.write("")
            
        messages=[]
        
        for index in range(len(df)-1):
            
            tempMessageDict={'text_input':df['TherapistText'][index],'output': df['ClientText'][index+1]}
            messages.append(tempMessageDict)

            
        with open(f"{name}.json", "a") as outfile: 
            outfile.write(json.dumps(messages))