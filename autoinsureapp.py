import pandas as pd
import streamlit as st
import numpy as np
import pickle as pk
#from streamlit_option_menu import option_menu
#import matplotlib.pyplot as plt
import base64
#from sklearn import svm
#import seaborn as sns


st.set_page_config(page_title='Auto Insurance Fraud Claim',layout='centered')


#selection=option_menu(menu_title="Main Menu",options=["Single Prediction","Multi Prediction"],icons=["cast","book","cast"],menu_icon="house",default_index=0)
with st.sidebar:
    st.title("Home Page")
    selection=st.radio("select your option",options=["One user Prediction", "Multi User Prediction"])


# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download your prediction</a>'
    return href


def FraudStatus(givendata):
    
    loaded_model=pk.load(open("EnnieSinglePredict.sav", "rb"))
    input_data_as_numpy_array = np.asarray(givendata)# changing the input_data to numpy array
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1) # reshape the array as we are predicting for one instance
    prediction = loaded_model.predict(input_data_reshaped)
    if prediction=="Y":
      return "Fraud"
    else:
      return "Not Fraud"


def main():
    st.header("Predict Fraud Claim")
    
    #getting user input
    option = st.selectbox("what is the user policy_csl ?",("",'100/300', '250/500',"500/1000"),key="policycsl")
    if (option=='100/300'):
        policy_csl="0"
    elif (option=="250/500"):
        policy_csl="1"
    else:
        policy_csl="2"


    option1 = st.selectbox('Gender',("",'Male', 'Female'),key="gender")
    if (option1=='Male'):
        insured_sex="1"
    else:
        insured_sex="0"
    
    option2 = st.selectbox('Eductaion Level', ("",'MD','PhD','Associate','Masters','High School','College','JD'),key="debt")
    if (option2=='MD'):
        insured_education_level="0"
    elif (option2=="PhD"):
        insured_education_level="1"
    elif (option2=="Associate"):
        insured_education_level="2"
    elif (option2=="Masters"):
        insured_education_level="3"
    elif (option2=="High School"):
        insured_education_level="4"
    elif (option2=="College"):
        insured_education_level="5"
    else:
        insured_education_level="6"
    

    
    
    option3 = st.text_input("occupation",key="registered")
    if option3 is not None:
        insured_occupation="1"
    else:
        insured_occupation="0"
    #RegisteredPhoneNumber=st.text_input("Has number been registered ?")


    option4 = st.selectbox("Incident Type",("",'Single Vehicle Collision','Vehicle Theft','Multi-vehicle Collision','Parked Car'),key="icidenttype")
    if (option4=='Single Vehicle Collision'):
        incident_type=0
    elif (option4=="Vehicle Theft"):
        incident_type="1"
    elif (option4=="Multi-vehicle Collision"):
        incident_type="2"
    else:
        incident_type="3"
    #ActiveFor3monthsAndAbove=st.text_input("Been active for three months and above ?")
    # code for Prediction
    

    option5 = st.selectbox("collision_type",("",'NO','Side Collision','Rear Collision','Front Collision'),key="activemonths")
    if (option5=='NO'):
        collision_type="0"
    elif (option5=="Side Collision"):
        collision_type="1"
    elif (option5=="Rear Collision"):
        collision_type="2"
    else:
        collision_type="3"


    option6 = st.selectbox("incident_severity",("",'Minor Damage','Major Damage','Total Loss','Trivial Damage'),key="incidentseverity")
    if (option6=='Minor Damage'):
        incident_severity="0"
    elif (option6=="Major Damage"):
        incident_severity="1"
    elif (option6=="Total Loss"):
        incident_severity="2"
    else:
        incident_severity="3"




    option7 = st.selectbox("authorities_contacted",("",'None','Police','Fire','Ambulance','Other'),key="authoritiescontacted")
    if (option7=='None'):
        authorities_contacted="0"
    elif (option7=="Police"):
        authorities_contacted="1"
    elif (option7=="Fire"):
        authorities_contacted="2"
    elif (option7=="Ambulance"):
        authorities_contacted="3"
    else:
        authorities_contacted="4"





    option8 = st.selectbox("property_damage",("","Yes","No"),key="property_damage")
    if (option8=='Yes'):
        property_damage="0"
    else:
        property_damage="1"
    

    bodily_injuries=st.number_input("bodily injuries",step=1 )
    witnesses=st.number_input("witnesses",step=1)

    option9 = st.selectbox("police_report_available",("","Yes","No"),key="police_report_available")
    if (option9=='No'):
        police_report_available="0"
    else:
        police_report_available="1"

    
    number_of_vehicles_involve=st.number_input("number of vehicle involved",step=1)
    injury_claim =st.number_input("injury claim amount")
    property_claim =st.number_input("property claim amount")
    vehicle_claim=st.number_input("vehicle claim amount")

    Eligible = ''#for displaying result
    
    # creating a button for Prediction
    if option!="" and option1!=""  and option2!=""  and option3!=""  and option4!="" and option5!="" and option6!="" and option7 !="" and option8 !="" and option9 !="" and st.button('Predict'):
        Eligible = FraudStatus([policy_csl,insured_sex,insured_education_level,insured_occupation,incident_type,collision_type,incident_severity,authorities_contacted,property_damage,bodily_injuries,witnesses,police_report_available,number_of_vehicles_involve,injury_claim,property_claim,vehicle_claim])
        st.success(Eligible)
    


def multi(input_data):
    loaded_model=pk.load(open("EnnieMultiPredict.sav", "rb"))
    dfinput = pd.read_csv(input_data)
    
    st.header('A view of the uploaded dataset')
    st.markdown('')
    st.dataframe(dfinput)

    forLoanId=dfinput["policy_number"]
    
    dfinput=dfinput.drop(columns=["policy_number","policy_deductable","policy_bind_date","policy_state","months_as_customer","insured_zip","insured_hobbies","incident_date","incident_state","incident_city","incident_location","incident_hour_of_the_day","auto_make","auto_model","auto_year"],axis=1)

  #replace some column values
    for name in dfinput["collision_type"]:
        if name == "?":
            dfinput.replace({"collision_type":{"?":np.nan}},inplace=True)
    #if "?" in df["property_damage"]:
    for name in dfinput["property_damage"]:
        if name == "?":
            dfinput.replace({"property_damage":{"?":np.nan}},inplace=True)
    #if "?" in df["police_report_available"]:
    for name in dfinput["police_report_available"]:
        if name == "?":
            dfinput.replace({"police_report_available":{"?":np.nan}},inplace=True)

  #encoding the results
  #df=encodingBinaries(df,"property_damage","YES")
  #df=encodingBinaries(df,"police_report_available","YES")
  #df=encodingBinaries(df,"insured_sex","YES")
    dfinput.replace({'police_report_available':{'NO':0,'YES':1},'property_damage':{'NO':1,'YES':0},'insured_sex: ':{'FEMALE':0,'MALE':1}},inplace=True)

  

#df.replace({'policy_csl':{'100/300':0,'250/500':1,'500/1000':2 }},inplace=True)


  #listpolicy_csl=['100/300','250/500','500/1000']
  #endoding the ordinals
  #df=ordinals(df,"policy_csl",numorder=listpolicy_csl)


#listpolicy_deductable={500:0,1000:1,2000:2}
#df["policy_deductable"]=df["policy_deductable"].replace(listpolicy_deductable)

    listinsured_education_level={'MD':0,'PhD':1,'Associate':2,'Masters':3,'High School':4,'College':5,'JD':6}
    dfinput["insured_education_level"]=dfinput["insured_education_level"].replace(listinsured_education_level)

    listinsured_relationship={'husband':0,'other-relative':1,'own-child':2,'unmarried':3,'wife':4,'not-in-family':5}
    dfinput["insured_relationship"]=dfinput["insured_relationship"].replace(listinsured_relationship)


    listincident_type={'Single Vehicle Collision':0,'Vehicle Theft':1,'Multi-vehicle Collision':2,'Parked Car':3}
    dfinput["incident_type"]=dfinput["incident_type"].replace(listincident_type)


    listcollision_type={'NO':0,'Side Collision':1,'Rear Collision':2,'Front Collision':3}
    dfinput["collision_type"]=dfinput["collision_type"].replace(listcollision_type)


    listincident_severity={'Minor Damage':0,'Major Damage':1,'Total Loss':2,'Trivial Damage':3}
    dfinput["incident_severity"]=dfinput["incident_severity"].replace(listincident_severity)


    listauthorities_contacted={'None':0,'Police':1,'Fire':2,'Ambulance':3,'Other':4}
    dfinput["authorities_contacted"]=dfinput["authorities_contacted"].replace(listauthorities_contacted)

    mappolicy_csl={'100/300':0,'250/500':1,'500/1000':2}
    dfinput["policy_csl"]=dfinput["policy_csl"].replace(mappolicy_csl)

    mapinsured_sex={"MALE":1,"FEMALE":0}
    dfinput["insured_sex"]=dfinput["insured_sex"].replace(mapinsured_sex)

  #for colums in [""]:

  
    for values in dfinput["insured_occupation"]:
        if values is not None :
            dfinput["insured_occupation"]=1
    else:
        dfinput["insured_occupation"]=0
    X_getam=dfinput.drop(["fraud_reported","age","policy_annual_premium","capital-gains","capital-loss","umbrella_limit","insured_relationship","total_claim_amount"],axis=1)



    X_getam["collision_type"].fillna(dfinput["collision_type"].mode()[0],inplace=True)
    X_getam["police_report_available"].fillna(dfinput["police_report_available"].mode()[0],inplace=True)
    X_getam["property_damage"].fillna(dfinput["property_damage"].mode()[0],inplace=True)
    #X_getam["collision_type"].fillna(X["police_report_available"].mode()[0],inplace=True)
    X_getam = np.asarray(X_getam)
    
    #dfinput = dfinput.drop(columns=['Loan_ID'],axis=1)
    

    #selectionList=["confusion Matrix","Predict","Visualization"]
    #selectionw=option_menu(menu_title=None,options=["Predict your result","Visualization","confusion Matrix"],icons=["cast","book","cast"],default_index=1, orientation="horizontal")
    
    #selectiond=st.selectbox("Predict, Visualize, and check confusion Matrix",selectionList)
    #st.write(Y)
    
    predict=st.button("predict")


    if predict:
        prediction = loaded_model.predict(X_getam)
        interchange=[]
        for i in prediction:
            if i=="Y":
                newi="Fraud"
                interchange.append(newi)
            elif i=="N":
                newi="Not Fraud"
                interchange.append(newi)
            
        st.subheader('Here is your prediction')
        prediction_output = pd.Series(interchange, name='Fraud Report')
        prediction_id = pd.Series(forLoanId)
        dfresult = pd.concat([prediction_id, prediction_output], axis=1)
        st.dataframe(dfresult)
        st.markdown(filedownload(dfresult), unsafe_allow_html=True)
        

if selection =="One user Prediction":
    main()

if selection == "Multi User Prediction":
    st.set_option('deprecation.showPyplotGlobalUse', False)
    #---------------------------------#
    # Prediction
    #--------------------------------
    #---------------------------------#
    # Sidebar - Collects user input features into dataframe
    st.header('Upload your csv file here')
    uploaded_file = st.file_uploader("", type=["csv"])
    #--------------Visualization-------------------#
    # Main panel
    
    # Displays the dataset
    if uploaded_file is not None:
        #load_data = pd.read_table(uploaded_file)
        multi(uploaded_file)
    else:
        st.info('Upload your dataset !!')
    






