import streamlit as st
import os
from diet import bmi_calculater,bmr_calculater,tdee_calculater,calories_target
from rag import load_rag
from openai import OpenAI
from dotenv import load_dotenv
##----------------------------------------LLM--------------------------------------------

load_dotenv()
HF_token=os.getenv("HF_TOKEN")
client=OpenAI(base_url="https://router.huggingface.co/v1",
              api_key=HF_token)

##----------------------------------------LLM-----------------------------------------
st.set_page_config(layout="wide")
st.title("AI HEALTH ASSISTANT🏋️‍♀️")
st.write("personal Health Assistance and Diet Recommendation Agent")
st.header("health informatio")
st.sidebar.header("🤷‍♂️Your Information")



##----------------------------------------------------------------------------------------
gender=st.sidebar.selectbox("gender",["Male","Female"])
age=st.sidebar.number_input("age",1,100)
weight=st.sidebar.number_input("weight(kg)",1,120)
height=st.sidebar.number_input("height(cm)",100,200)
activity=st.sidebar._selectbox("Activity",["Sedentary","Lightly Active","Moderately Active","very active","Extra Active"])
aim=st.sidebar.selectbox("AIM",["weight maintain", "weight gain", "weight loss"])
diet_type=st.sidebar.selectbox("diet type",["vegetarian","non-vegetarian"])
allergies=st.sidebar.selectbox("allergies",["allergie","none"])




##--------------------------------------------------------------------------------------------
bmi=bmi_calculater(weight,height)
bmr=bmr_calculater(gender,age,weight,height)
tdee=tdee_calculater(bmi,activity)
calorie=calories_target(tdee,aim)


##-----------------------------------------------------------------------------------------------
col1,col2,col3,col4=st.columns(4)
col1.metric("BMI",bmi)
col2.metric("BMR",f"{bmr} kcal")
col3.metric("tdee",f"{tdee}kcal")
col4.metric("calorie target",f"{calorie}kcal")

tab1,tab2=st.tabs(['diet recomandation',"health assistance"])
if tab1:
    if st.button("recommend diet"):
        if client:
            with st.spinner("creating diet......"):
                try:
                    db=load_rag()
                    search_query=f"""diet_type"{diet_type}
                                    healthy food
                                    protien
                                    allergies{allergies}"""
                    docs=db.similarity_search(search_query,3)
                    context="\n\n".join([ doc.page_content for doc in docs])
                    prompt=f"""You are a helpful AI nutrition assistant.



Use the following nutrition knowledge

to create a simple one-day diet plan.



NUTRITION KNOWLEDGE:



{context}





USER INFORMATION:



Age: {age}



Gender: {gender}



Height: {height} cm



Weight: {weight} kg



Activity Level: {activity}



aim: {aim}



Diet Type: {diet_type}



Food Allergy: {allergies}



Estimated BMI: {bmi}



Estimated BMR: {bmr} kcal/day



Estimated TDEE: {tdee} kcal/day



Estimated Daily Calorie Target:

{calorie} kcal/day





Create the following:



1\. Breakfast

2\. Morning Snack

3\. Lunch

4\. Evening Snack

5\. Dinner





For every meal provide:



\- Food

\- Portion

\- Approximate calories

\- Approximate protein





IMPORTANT RULES:



\- Respect the user's diet type.

\- Do not recommend foods containing

&#x20; the stated allergy.

\- Use the provided nutrition knowledge

&#x20; when possible.

\- Keep the plan simple and practical.

\- Do not diagnose diseases.

\- Do not prescribe medicines.

\- Do not claim to cure diseases.

\- This is general wellness information,

&#x20; not medical advice."""
                    response=client.chat.complitions.create(model="openai/gpt-oss-120b",
                                                            message=[{"role":"user",
                                                                      "content": prompt
                                                                      }])
                    answer=response.choice[0].message.content
                    st.markdown(answer)
                except:
                    st.error("rag is not connected")
if tab2:
    question=st.text_area("ask about health",
                 placeholder="eg:good source of vegetraian protien")
    if st.button("ask ai"):
        db=load_rag()
        docs=db.similarity_search(question,3)
        context="\n\n".join([doc.page_content for doc in docs])
        prompt=f"""You are an AI health and nutrition

assistant.



Use the following knowledge to answer

the user's question.



NUTRITION KNOWLEDGE:



{context}





USER QUESTION:



{question}





INSTRUCTIONS:



\- Answer clearly.

\- Keep the explanation beginner-friendly.

\- Use the provided knowledge when possible.

\- Do not invent medical facts.

\- Do not diagnose diseases.

\- Do not prescribe medicines.

\- Do not claim to cure diseases.

\- If the question concerns a serious

&#x20; medical problem, recommend consulting

&#x20; a qualified healthcare professional.



This application provides general health

and nutrition information for educational

and wellness purposes.
"""
        response=client.chat.completions.create(model="openai/gpt-oss-120b",messages=[{"role":"user",
                                                                                   "content":prompt
                                                                                   }])
        answer=response.choices[0].message.content
        st.markdown(answer)
        
    