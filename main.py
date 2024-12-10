import streamlit as st
import pandas as pd

st.title("File Upload with Grading and Scaling")

stud_grade1 = st.file_uploader("Choose a file", type=["xlsx", "xls"])

st.sidebar.title("Check Your Result")
option = st.sidebar.radio("Select", ["Student_Data", "Student_Grade", "Grading_System"])

if stud_grade1 is not None:
    stud_grade = pd.read_excel(stud_grade1)

    
    stud_grade['Total Marks'] = 0.0
    stud_grade['grade'] = ''
    stud_grade['scaled_grade'] = ''

    
    for i in range(2, len(stud_grade)):
        total_mark = (
            (stud_grade['Mid Sem'][i] * stud_grade['Mid Sem'][1]) / stud_grade['Mid Sem'][0] +
            (stud_grade['Endsem'][i] * stud_grade['Endsem'][1]) / stud_grade['Endsem'][0] +
            (stud_grade['Quiz 1'][i] * stud_grade['Quiz 1'][1]) / stud_grade['Quiz 1'][0] +
            (stud_grade['Quiz 2'][i] * stud_grade['Quiz 2'][1]) / stud_grade['Quiz 2'][0]
        )
        stud_grade.at[i, 'Total Marks'] = total_mark.round(3)

    
    stud_grade.at[0, 'Total Marks'] = ''
    stud_grade.at[1, 'Total Marks'] = ''
    stud_grade.at[0, 'Name'] = ''
    stud_grade.at[1, 'Name'] = ''

    
    grading_sys = {
        'grade': ['AA', 'AB', 'BB', 'BC', 'CC', 'CD', 'DD', 'F', 'I', 'PP', 'NP'],
        'old iapc reco': ['5', '15', '25', '30', '15', '5', '5', '0', '0', '0', '0'],
        'Counts': ['' for _ in range(11)],
        'Round': ['' for _ in range(11)],
        'Count verified': ['' for _ in range(11)]
    }

    
    df = pd.DataFrame(grading_sys)
    df['old iapc reco'] = pd.to_numeric(df['old iapc reco'])
    df['Counts'] = 102 * df['old iapc reco'] / 100
    df['Round'] = df['Counts'].round(0)

    
    stud_grade_after = stud_grade.iloc[2:]
    stud_grade_after_sorted = stud_grade_after.sort_values(by='Total Marks', ascending=True)
    stud_grade_sorted = pd.concat([stud_grade.iloc[:2], stud_grade_after_sorted], ignore_index=True)

    
    for i in range(2, len(stud_grade_sorted)):
        if stud_grade_sorted['Total Marks'][i] >= 90:
            stud_grade_sorted.at[i, 'grade'] = 'AA'
        elif stud_grade_sorted['Total Marks'][i] >= 80:
            stud_grade_sorted.at[i, 'grade'] = 'AB'
        elif stud_grade_sorted['Total Marks'][i] >= 70:
            stud_grade_sorted.at[i, 'grade'] = 'BB'
        elif stud_grade_sorted['Total Marks'][i] >= 60:
            stud_grade_sorted.at[i, 'grade'] = 'BC'
        elif stud_grade_sorted['Total Marks'][i] >= 50:
            stud_grade_sorted.at[i, 'grade'] = 'CC'
        elif stud_grade_sorted['Total Marks'][i] >= 40:
            stud_grade_sorted.at[i, 'grade'] = 'CD'
        elif stud_grade_sorted['Total Marks'][i] >= 30:
            stud_grade_sorted.at[i, 'grade'] = 'DD'
        else:
            stud_grade_sorted.at[i, 'grade'] = 'F'

    
    for i in range(2, len(stud_grade_sorted)):
        grade = stud_grade_sorted['grade'][i]
        if grade in df['grade'].values:
            grade_row = df[df['grade'] == grade]
            a = 90 if grade == 'AA' else grade_row['Counts'].values[0]
            b = grade_row['old iapc reco'].values[0]
            scaled = ((stud_grade_sorted['Total Marks'][i] - 30) * (b - a) / 60) + a
            stud_grade_sorted.at[i, 'scaled_grade'] = scaled.round(2)

    
    grade_counts = stud_grade_sorted['grade'].value_counts()
    for grade in df['grade']:
        df.at[df[df['grade'] == grade].index[0], 'Count verified'] = grade_counts.get(grade, 0)

    
    if option == "Student_Data":
        vip = st.button("View Input")
        if vip:
            st.write(pd.read_excel(stud_grade1))  

    elif option == "Student_Grade":
        vip1 = st.button("Generate Output")
        if vip1:
            st.write(stud_grade_sorted)  

    elif option == "Grading_System":
        st.write(df)  

    
    sort_by_roll = st.checkbox("Sort by Roll Number")
    if sort_by_roll:
        stud_grade_sorted = stud_grade_sorted.sort_values(by='Roll', ascending=True)
        st.write(stud_grade_sorted)

    
    sort_by_grade = st.checkbox("Sort by Grade")
    if sort_by_grade:
        
        grade_order = ['PP','I','AA','AB','BB','BC','CC','CD','DD','F','NP']
        stud_grade_sorted['grade'] = pd.Categorical(stud_grade_sorted['grade'], categories=grade_order, ordered=True)
        stud_grade_sorted = stud_grade_sorted.sort_values(by='grade', ascending=True)
        st.write(stud_grade_sorted)

    
    st.write("Scaled Grades")
    st.write(stud_grade_sorted[['Roll', 'Name', 'Total Marks', 'grade', 'scaled_grade']])


    