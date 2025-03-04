from flask import Flask,request,jsonify,render_template
import pickle
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail, Message



#flask\models\rfr_model.pkl

application= Flask(__name__)
app=Flask(__name__)
#model=pickle.load(open('models/cement.pkl','rb'))
m1=pickle.load(open('models/rfr_model.pkl','rb'))
sleep_model=pickle.load(open('models/sm.pkl','rb'))
userbehaviormodel=pickle.load(open('models/userbehavior.pkl','rb'))

@app.route("/")
def welcome():
    #a=Cem.query.all()
    #print(a)
    return render_template("w.html")
@app.route("/home")
def homeb():
    return render_template("home.html")
@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get("email")
        password=request.form.get("password")
        print(username,email,password)
    return render_template("signup.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/knm")
def knm():
    return render_template("knm.html")
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")
@app.route("/price")
def price():
    return render_template("price.html")

@app.route("/pred",methods=["GET","POST"])
def hello_word():
    if request.method=='POST':
        school=float(request.form.get('school'))
        gender=float(request.form.get('gender'))
        parentstatus=float(request.form.get('parentstatus'))
        mothereducation=float(request.form.get('mothereducation'))
        fathereducation=float(request.form.get('fathereducation'))
        motherjob=float(request.form.get('motherjob'))
        fatherjob=float(request.form.get('fatherjob'))
        traveltime=float(request.form.get('traveltime'))
        studytime=float(request.form.get('studytime'))
        failure=float(request.form.get('failure'))
        activities=float(request.form.get('activities'))
        internet=float(request.form.get('internet'))
        romantic=float(request.form.get('romantic'))
        freetime=float(request.form.get('freetime'))
        Walc=float(request.form.get('Walc'))
        health=float(request.form.get('health'))
        absences=float(request.form.get('absences'))
        G1=float(request.form.get('G1'))
        G2=float(request.form.get('G2'))
        result=m1.predict([[ school, gender,parentstatus,mothereducation,fathereducation,motherjob,fatherjob,traveltime,studytime, failure,activities,internet,romantic,freetime,Walc,health,absences,G1,G2]])
        if(result<0):
           result=-result
        return render_template('check.html',results=result[0])

    else:
        return render_template('check.html')
    


###################################################################
# Function to analyze strengths and weaknesses
# def analyze_sleep_efficiency(features, model):
#     prediction = sleep_model.predict([features])[0]
    
#     strengths = []
#     weaknesses = []
    
#     if features[3] >= 420:
#         strengths.append("Adequate time in bed")
#     else:
#         weaknesses.append("Not enough time in bed")
    
#     if 6 <= features[4] <= 8:
#         strengths.append("Consistent wake-up time")
#     else:
#         weaknesses.append("Irregular wake-up time")
    
#     if features[12] == 1:
#         weaknesses.append("Smoking may affect sleep efficiency")
#     else:
#         strengths.append("Non-smoker, good for sleep efficiency")
    
#     return prediction, strengths, weaknesses

# @app.route('/predictsleepeffecienct', methods=['GET', 'POST'])
# def predictsleepeffecienct():
#     if request.method == 'POST':
#         try:
#             bedtime = float(request.form.get('Bedtime'))
#             wakeup_time = float(request.form.get('WakeupTime'))
#             total_minutes_in_bed = float(request.form.get('TotalMinutesInBed'))
#             smoking_status = int(request.form.get('SmokingStatus'))
#             gender = int(request.form.get('Gender'))

#             features = [bedtime, wakeup_time, total_minutes_in_bed, smoking_status, gender]
#             prediction, strengths, weaknesses = analyze_sleep_efficiency(features, sleep_model)
            
#             return render_template('sleep_result.html', prediction=prediction, strengths=strengths, weaknesses=weaknesses)
#         except Exception as e:
#             return f"Error: {str(e)}"
    
#     return render_template('sleepefficieny.html')
def analyze_sleep_efficiency(features, model):
    prediction = model.predict([features])[0]
    strengths = []
    weaknesses = []

    age, gender, bedtime, wakeup, sleep_duration, rem, deep, light, awakenings, caffeine, alcohol, smoking, exercise = features
    
    # Analyze strengths
    if sleep_duration >= 420:
        strengths.append("Adequate sleep duration")
    if rem >= 20:
        strengths.append("Healthy REM sleep percentage")
    if deep >= 15:
        strengths.append("Good deep sleep percentage")
    if awakenings <= 2:
        strengths.append("Minimal awakenings during sleep")
    if exercise >= 3:
        strengths.append("Regular exercise routine")
    
    # Analyze weaknesses
    if sleep_duration < 360:
        weaknesses.append("Insufficient sleep duration")
    if rem < 15:
        weaknesses.append("Low REM sleep percentage")
    if deep < 10:
        weaknesses.append("Low deep sleep percentage")
    if awakenings > 4:
        weaknesses.append("Frequent awakenings during sleep")
    if caffeine > 2:
        weaknesses.append("High caffeine consumption may affect sleep")
    if alcohol > 2:
        weaknesses.append("Excessive alcohol consumption can disrupt sleep")
    if smoking == 1:
        weaknesses.append("Smoking may negatively impact sleep quality")
    if exercise < 2:
        weaknesses.append("Low physical activity may reduce sleep efficiency")
    
    return round(prediction * 100, 2), strengths, weaknesses

@app.route('/predictsleepeffecienct', methods=['GET', 'POST'])
def predictsleepeffecienct():
    if request.method == 'POST':
        try:
            age = int(request.form.get('age'))
            gender = int(request.form.get('gender'))
            bedtime = request.form.get('bedtime')
            wakeup = request.form.get('wakeup')
            sleep_duration = int(request.form.get('sleep_duration'))
            rem = float(request.form.get('rem'))
            deep = float(request.form.get('deep'))
            light = float(request.form.get('light'))
            awakenings = int(request.form.get('awakenings'))
            caffeine = int(request.form.get('caffeine'))
            alcohol = int(request.form.get('alcohol'))
            smoking = int(request.form.get('smoking'))
            exercise = int(request.form.get('exercise'))
            
            # Convert bedtime and wakeup time to minutes
            bedtime_hr, bedtime_min = map(int, bedtime.split(':'))
            wakeup_hr, wakeup_min = map(int, wakeup.split(':'))
            bedtime_in_minutes = bedtime_hr * 60 + bedtime_min
            wakeup_in_minutes = wakeup_hr * 60 + wakeup_min
            
            features = [age, gender, bedtime_in_minutes, wakeup_in_minutes, sleep_duration, rem, deep, light, awakenings, caffeine, alcohol, smoking, exercise]
            prediction, strengths, weaknesses = analyze_sleep_efficiency(features, sleep_model)
            
            return render_template('easy.html', results=prediction, strengths=strengths, weaknesses=weaknesses)
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template('easy.html')
def analyze_behavior(features):
    analysis = {"Strength": "No major strengths detected.", "Weakness": "No major weaknesses detected."}
    
    if features["App Usage Time (min/day)"] > 300:
        analysis["Strength"] = "Highly engaged with mobile apps, good at digital interaction."
        analysis["Weakness"] = "Excessive screen time might impact productivity or sleep."
    elif features["App Usage Time (min/day)"] < 100:
        analysis["Strength"] = "Minimal phone usage, better time management."
        analysis["Weakness"] = "May struggle with digital adaptation in tech-heavy tasks."

    if features["Battery Drain (mAh/day)"] > 1500:
        analysis["Weakness"] = "High battery drain suggests heavy usage, possibly inefficient apps."
    
    return analysis

# Flask route for prediction
@app.route("/userbehavior", methods=["GET", "POST"])
def userbehavior():
    predicted_category = None
    analysis = None

    if request.method == "POST":
        # Extract input data
        input_data = {
            "App Usage Time (min/day)": float(request.form["app_usage"]),
            "Screen On Time (hours/day)": float(request.form["screen_time"]),
            "Battery Drain (mAh/day)": float(request.form["battery_drain"]),
            "Number of Apps Installed": int(request.form["num_apps"]),
            "Data Usage (MB/day)": float(request.form["data_usage"]),
            "Age": int(request.form["age"]),
            "Gender": 1 if request.form["gender"] == "Male" else 0  # Encoding Gender
        }

        # Convert input to DataFrame for model
        input_df = pd.DataFrame([input_data])

        # Make prediction
        predicted_category = userbehaviormodel.predict(input_df)[0]

        # Analyze strengths & weaknesses
        analysis = analyze_behavior(input_data)

    return render_template("behaviou.html", category=predicted_category, analysis=analysis)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)