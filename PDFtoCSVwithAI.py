import fitz
from openai import OpenAI
import re
import pandas as pd

client = OpenAI(
    api_key= #,
)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text()
            text += page_text + "\n"  # Add a newline to separate pages
    text = re.sub(r'\b\d+\b', '', text).strip()
    return text

def split_text_into_segments(text, max_length=3000):
    lines = text.split('\n')
    segments = []
    current_segment = ""
    next_segment_prefix = ""

    def is_speaker_label(line):
        """Check if the line is a speaker label."""
        return re.match(r'^\w+:\s*$', line.strip()) is not None

    for line in lines:
        # Check if adding this line would exceed the max length
        if len(current_segment) + len(line) + 1 > max_length:
            # Split current segment into lines and check if the last line is a speaker label
            segment_lines = current_segment.strip().split('\n')
            if segment_lines and is_speaker_label(segment_lines[-1]):
                # Move speaker label to next segment
                next_segment_prefix = segment_lines[-1]
                # Remove speaker label from the current segment
                current_segment = '\n'.join(segment_lines[:-1]).strip()
            else:
                next_segment_prefix = ""
            
            # Add the current segment to the list if it's not empty
            if current_segment:
                segments.append(current_segment.strip())
            
            # Start the next segment with the saved speaker label
            current_segment = next_segment_prefix + "\n" + line
        else:
            current_segment += line + "\n"
    
    # Handle the last segment
    if current_segment:
        segment_lines = current_segment.strip().split('\n')
        if segment_lines and is_speaker_label(segment_lines[-1]):
            # Remove trailing speaker label if present
            segment_with_no_label = '\n'.join(segment_lines[:-1]).strip()
            if segment_with_no_label:
                segments.append(segment_with_no_label)
        else:
            segments.append(current_segment.strip())
    
    return segments
    

def process_text_with_openai(segments):
    responses = []
    for segment in segments:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a pdf to df converter which specializes in converting psychiatric transcipts to dfs structured with the consecutive rows of text between the Client and the Therapist. Do not provie anything other than the DF and ignore any annotations in the text, simply continue with the same speaker if annotations interrupt a text. Do not add text, if the dialogue starts with the Therapist, make the first row of the ClientText an X, likewise if the dialogue ends with the Client. Do not add quotations around any text. The DF should have the columns: ClientText | TherapistText "},
                {"role": "system", "content": f"{segment}"}
            ]
        )
        responses.append(response.choices[0].message.content)
    return responses

def predict_mental_illness(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a diagnostic tool to predict the most likely mental illness from psychiatric transcripts. Only return the most likely mental-illness and no other text."},
            {"role": "system", "content": f"{text}"}
        ]
    )
    return(response.choices[0].message.content)

def predict_age_range(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a diagnostic tool to predict the most likely age range of the Client from psychiatric transcripts. Only return the most likely age-range and no other text."},
            {"role": "system", "content": f"{text}"}
        ]
    )
    return(response.choices[0].message.content)

def create_dataframe(processed_texts,mental_illness,age_range,i,pdf_path):
    data = []
    pending_row = None
    for processed_text in processed_texts:
        lines = processed_text.strip().split('\n')
        #print(lines)
        columns = [col.strip() for col in lines[0][1:].split('|')]
        columns.insert(0,"ID")
        columns.insert(1,"MentalIllness")
        columns.insert(2,"AgeRange")
        for line in lines[2:]:
            if line[0]=="|":
                line=line[1:]
            if line[-1]=="|":
                line=line[:-1]

            row = [col.strip() for col in line.split('|')]
            if len(row) == 2 and (row[0] == '' or row[1] == ''):
                if pending_row != None:
                    # Combine pending row with current row
                    if row[0] == '':
                        pending_row[1] += ' ' + row[1]
                    else:
                        pending_row[0] += ' ' + row[0]
                    
                    pending_row.insert(0, i)
                    pending_row.insert(1, mental_illness)
                    pending_row.insert(2, age_range)
                    data.append(pending_row)
                    pending_row = None
                else:
                    pending_row = row
            else:
                if pending_row != None:
                    # Handle pending row before current row
                    pending_row.insert(0, i)
                    pending_row.insert(1, mental_illness)
                    pending_row.insert(2, age_range)
                    data.append(pending_row)
                    pending_row = None

                row.insert(0, i)
                row.insert(1, mental_illness)
                row.insert(2, age_range)
                data.append(row)

        # Handle any remaining pending row
        if pending_row != None:
            pending_row.insert(0, i)
            pending_row.insert(1, mental_illness)
            pending_row.insert(2, age_range)
            pending_row.extend([''] * (len(columns) - 3 - len(pending_row)))  # Add empty strings for missing columns
            data.append(pending_row)
            pending_row = None

                
    df = pd.DataFrame(data, columns=[columns])
    df.to_csv(pdf_path[:-3]+"csv")
    print(df)
    return df

def process_pdfs(pdf_paths):
    all_dfs = []
    for i,pdf_path in enumerate(pdf_paths):
        text = extract_text_from_pdf(pdf_path)
        segments=split_text_into_segments(text)
        
        processed_text = process_text_with_openai(segments)
        mental_illness = predict_mental_illness(text)
        age_range = predict_age_range(segments)
        df = create_dataframe(processed_text,mental_illness,age_range,i+1,pdf_path)
        all_dfs
    return pd.concat(all_dfs, ignore_index=True)

# Example usage
pdf_paths = ['BB3-Session-10-Annotated-Transcript.pdf'] 
process_pdfs(pdf_paths)
