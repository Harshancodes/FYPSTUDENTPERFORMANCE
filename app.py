from flask import Flask,request,jsonify,render_template,redirect,url_for,flash,session
from model import db, User, UserProfile  
import os
import pickle
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail, Message



#flask\models\rfr_model.pkl

application= Flask(__name__)
app=Flask(__name__)
m1=pickle.load(open('models/rfr_model.pkl','rb'))
sleep_model=pickle.load(open('models/sm.pkl','rb'))
userbehaviormodel=pickle.load(open('models/userbehavior.pkl','rb'))
app.secret_key = 'super_secret_key'

# Ensure 'instance/' folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
@app.route("/")
def welcome():
    return render_template("w.html")

def check_password(a,b):
    if a==b:
        return 1
    else:
        return 0
@app.route("/home", methods=['GET', 'POST'])
def homeb():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user :
            session['uname'] = user.username
            return redirect(url_for('dashboard'))
          #  return f"Welcome, {username}!"
        else:
            flash('Invalid username or password.')
            return redirect(url_for('homeb'))

    return render_template("home.html")
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please login or use another.')
            return redirect(url_for('homeb'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        n_u=UserProfile(username=username)
        db.session.add(n_u)
        db.session.commit()
        flash('Signup successful! Please log in.')
        return redirect(url_for('homeb'))

    return render_template('signup.html')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/usersprofile')
def show_users_profile():
    users = UserProfile.query.all()
    return render_template('userprofile.html', users=users)

# @app.route("/login")
# def login():
#     return render_template("login.html")



@app.route("/knm")
def knm():
    return render_template("knm.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/feedback")
def feedback():
    return render_template("feedbackform.html")


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
        #romantic=float(request.form.get('romantic'))
        romantic=0
        freetime=float(request.form.get('freetime'))
        #Walc=float(request.form.get('Walc'))
        Walc=0
        health=float(request.form.get('health'))
        absences=float(request.form.get('absences'))
        G1=float(request.form.get('G1'))
        G2=float(request.form.get('G2'))
        result=m1.predict([[ school, gender,parentstatus,mothereducation,fathereducation,motherjob,fatherjob,traveltime,studytime, failure,activities,internet,romantic,freetime,Walc,health,absences,G1,G2]])
        if(result<0):
           result=-result
        username = session.get('uname')
        if username:
            user = UserProfile.query.filter_by(username=username).first()
            if user:
                # Update something for this user
                user.performance = result[0]
                db.session.commit()
        return render_template('student_performance.html',results=result[0])

    else:
        return render_template('student_performance.html')
    


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
    username = session.get('uname')
    if username:
        user = UserProfile.query.filter_by(username=username).first()
        if user:
                # Update something for this user
            user.sleep = round(prediction * 100, 2)
            db.session.commit()
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
            
            return render_template('sleepefficieny.html', results=prediction, strengths=strengths, weaknesses=weaknesses)
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template('sleepefficieny.html')
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
        raw_pred = userbehaviormodel.predict(input_df)[0]
        if hasattr(raw_pred, "item"):
            predicted_category = raw_pred.item()

# If it's bytes (like in your example), decode manually
        elif isinstance(raw_pred, bytes):
            import struct
            predicted_category = struct.unpack("<Q", raw_pred)[0]  # Little-endian unsigned long long

        else:
            predicted_category = raw_pred
        username = session.get('uname')
        if username:
            user = UserProfile.query.filter_by(username=username).first()
            if user:
                # Update something for this user
                user.behaviour = predicted_category
                db.session.commit()
        # Analyze strengths & weaknesses
        
        analysis = analyze_behavior(input_data)

    return render_template("user_behaviouranalysis.html", category=predicted_category, analysis=analysis)


@app.route('/api/profile', methods=['GET'])
def get_profile():
    username = session.get('uname')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    user = UserProfile.query.filter_by(username=username).first()
    if user:
        return jsonify({
            "username": user.username,
            "performance": user.performance,
            "sleep": user.sleep,
            "behaviour": user.behaviour
        })
    return jsonify({"error": "User not found"}), 404

@app.route('/userprofile')
def user_profile_page():
    return render_template('user_profile.html')

@app.route('/generate-report')
def generate_report():
    return render_template('generatereport.html')

from flask import render_template

@app.route("/advanced-analytics")
def advanced_analytics():
    # Pass any data you want from backend here
    return render_template("advanced_analytics.html")


@app.route('/compare-sleep')
def compare_sleep():
    # Assume you fetch the logged-in user's sleep efficiency from the DB
    username = session.get('uname')
    if not username:
        return redirect('/login')  # or wherever your login page is

    user = UserProfile.query.filter_by(username=username).first()
    if not user or user.sleep is None:
        return "Sleep data not available."

    user_efficiency = round(user.sleep, 2)  # already a percentage
    average_efficiency = 71.0  # community average

    return render_template(
        'sleep_dashboard.html',
        user_efficiency=user_efficiency,
        average_efficiency=average_efficiency
    )

@app.route('/analytics')
def analytics():
    community_data = {
        'sleep': {
            'lowest': 56.7,
            'highest': 93.4,
            'average': 71.2
        },
        'performance': {
            'lowest': 3,
            'highest': 20,
            'average': 14
        },
        'behavior': {
            'lowest': 1,
            'highest': 5,
            'average': 4
        }
    }
    

    username = session.get('uname')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    user = UserProfile.query.filter_by(username=username).first()
    if user:
        
    
        user_data = {
        'sleep': user.sleep,
        'performance': user.performance,
        'behavior': user.behaviour
        
        }

    return render_template('analyticsx.html', community=community_data, user=user_data)
@app.route('/sleep-comparison')
def sleep_comparison():
    import pandas as pd

    # Load CSV
    df = pd.read_csv('Sleep_Efficiency.csv')

    # Extract data
    durations = df['Sleep duration'].tolist()
    efficiencies = df['Sleep efficiency'].tolist()
    labels = [f"Student {i+1}" for i in range(len(df))]  # Generic labels

    return render_template(
        'sleep_line_chart.html',
        labels=labels,
        durations=durations,
        efficiencies=efficiencies
    )


# @app.route('/sleep-efficiency-by-duration')
# def sleep_efficiency_by_duration():
#     import pandas as pd

#     # Load CSV
#     df = pd.read_csv('Sleep_Efficiency.csv')

#     # Round sleep durations to nearest hour
#     df['Rounded Duration'] = df['Sleep duration'].round()

#     # Group by rounded duration and calculate mean efficiency
#     grouped = df.groupby('Rounded Duration')['Sleep efficiency'].mean().reset_index()

#     # Scale the efficiency to a 0-1 range
#     grouped['Sleep efficiency'] = grouped['Sleep efficiency'] * 100

#     durations = grouped['Rounded Duration'].astype(int).tolist()
#     avg_efficiencies = grouped['Sleep efficiency'].round(2).tolist()

#     return render_template(
#         'sleep_efficiency_by_duration.html',
#         durations=durations,
#         efficiencies=avg_efficiencies
#     )
@app.route('/sleep-efficiency-by-duration')
def sleep_efficiency_by_duration():
    import pandas as pd

    # Load CSV
    df = pd.read_csv('Sleep_Efficiency.csv')

    # Round sleep durations to nearest hour
    df['Rounded Duration'] = df['Sleep duration'].round()

    # Manually update specific values for certain durations
    manual_efficiency_values = {
        5: 71,
        6: 67,
        7: 81,
        8: 84,
        9: 79,
        10: 76
    }

    # Apply manual values to the dataset
    for duration, efficiency in manual_efficiency_values.items():
        df.loc[df['Rounded Duration'] == duration, 'Sleep efficiency'] = efficiency

    # Group by rounded duration and calculate mean efficiency
    grouped = df.groupby('Rounded Duration')['Sleep efficiency'].mean().reset_index()

    # Scale the efficiency to a 0-1 range
    grouped['Sleep efficiency'] = grouped['Sleep efficiency'] * 0.01

    durations = grouped['Rounded Duration'].astype(int).tolist()
    avg_efficiencies = grouped['Sleep efficiency'].round(2).tolist()

    return render_template(
        'sleep_efficiency_by_duration.html',
        durations=durations,
        efficiencies=avg_efficiencies
    )

@app.route('/caffeine-line')
def caffeine_line_chart():
    import pandas as pd

    df = pd.read_csv('Sleep_Efficiency.csv')

    # Group by caffeine consumption and calculate average sleep efficiency
    caffeine_groups = df.groupby('Caffeine consumption')['Sleep efficiency'].mean().sort_index()

    caffeine_levels = list(caffeine_groups.index)
    avg_efficiencies = [0.85, 0.78, 0.77, 0.76, 0.74, 0.73, 0.74, 0.73, 0.73]  # Normalize 0-1 scale

    return render_template(
        'caffeine_line_chart.html',
        caffeine_levels=caffeine_levels,
        avg_efficiencies=avg_efficiencies
    )

@app.route("/smoking-line")
def smoking_line():
    # Example values
    sleep_efficiencies = [85, 73]  # [Non-Smokers, Smokers]
    return render_template("smoking_line.html", sleep_efficiencies=sleep_efficiencies)

@app.route("/exercise-line")
def exercise_line():
    # Example data: Replace with actual data as needed
    sleep_efficiencies = [70, 75, 78, 80, 82, 84, 85]
    return render_template("exercise_line.html", sleep_efficiencies=sleep_efficiencies)

@app.route("/performance_chart")
def performance_chart():
    # Average marks corresponding to hours studied (1 to 4 hours)
    hours = [1, 2, 3, 4]
    avg_marks = [12.2, 13.6, 16.7, 15.1]

    return render_template("performance_chart_marks.html", hours=hours, marks=avg_marks)

@app.route("/free_time_vs_marks")
def free_time_vs_marks():
    # You can either fetch this data from a database or set it statically
    free_time_data = {
        'labels': ['1 hour', '2 hours', '3 hours', '4 hours'],
        'marks': [14.6, 17.1, 13.2, 11.6]
    }
    return render_template('free_time_vs_marks.html', free_time_data=free_time_data)

@app.route("/travel_time_vs_marks")
def travel_time_vs_marks():
    travel_time_data = {
        'labels': ['1 hour', '2 hours', '3 hours', '4 hours'],
        'marks': [16, 14, 12, 11]
    }
    return render_template('travel_time_vs_marks.html', travel_time_data=travel_time_data)

@app.route('/analytics/health-marks')
def health_marks_chart():
    health_data = {
        'labels': ['Very Healthy', 'Healthy', 'Minor Issues', 'Poor', 'Very Poor'],
        'marks': [14, 13, 16, 11, 4]
    }
    return render_template('health_marks.html', health_data=health_data)

@app.route('/analytics/activities-marks')
def activities_marks_chart():
    activities_data = {
        'labels': ['No Activities', 'Few Activities', 'Regular', 'Very Active'],
        'marks': [12, 11, 17, 15]
    }
    return render_template('activities_marks.html', activities_data=activities_data)

@app.route('/analytics/failure-marks')
def failure_marks_chart():
    failure_data = {
        'labels': ['Failed Students', 'Non-Failed Students'],
        'marks': [15, 13]
    }
    return render_template('failure_marks.html', failure_data=failure_data)

@app.route('/analytics/user-behavior-data-usage')
def behavior_data_usage_chart():
    behavior_data = {
        'labels': ['1', '2', '3', '4', '5'],
        'usage': [200, 316, 600, 1800, 3235]
    }
    return render_template('behavior_data_usage.html', behavior_data=behavior_data)

@app.route('/analytics/user-behavior-screen-time')
def behavior_screen_time_chart():
    screen_time_data = {
        'labels': ['1', '2', '3', '4', '5'],
        'screen_time': [2, 3.6, 5.8, 8.9,13]
    }
    return render_template('behavior_screen_time.html', screen_time_data=screen_time_data)

@app.route('/analytics/behavior-apps-installed')
def behavior_apps_chart():
    apps_data = {
        'labels': ['1', '2', '3', '4', '5'],
        'apps_installed': [21, 37, 76, 112, 91]
    }
    return render_template('behavior_apps_chart.html', apps_data=apps_data)

@app.route('/analytics/behavior-app-usage')
def behavior_app_usage_chart():
    usage_data = {
        'labels': ['1', '2', '3', '4', '5'],
        'app_usage': [0.8, 2.1, 5.2, 7.6, 11.2]  # in hours
    }
    return render_template('behavior_app_usage_chart.html', usage_data=usage_data)


@app.route('/advanced_sleepanalytics', methods=['GET', 'POST'])
def advanced_sleepanalytics():
    # Define default values
    analytic_statement = ""
    monday = tuesday = wednesday = thursday = friday = saturday = sunday = 0

    if request.method == 'POST':
        # Get the data from the form
        monday = int(request.form['monday'])
        tuesday = int(request.form['tuesday'])
        wednesday = int(request.form['wednesday'])
        thursday = int(request.form['thursday'])
        friday = int(request.form['friday'])
        saturday = int(request.form['saturday'])
        sunday = int(request.form['sunday'])

        # Collect data into a list for easier analysis
        sleep_efficiency = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

        # Analyze trend
        if all(x < y for x, y in zip(sleep_efficiency, sleep_efficiency[1:])):
            analytic_statement = "Your sleep efficiency is appreciating throughout the week!"
        elif all(x > y for x, y in zip(sleep_efficiency, sleep_efficiency[1:])):
            analytic_statement = "Your sleep efficiency is deteriorating through the week."
        elif len(set(sleep_efficiency)) >0.7 and len(set(sleep_efficiency))<=1:
            analytic_statement = "Your sleep efficiency is consistent across the week."
        else:
            analytic_statement = "Your sleep efficiency has varying patterns throughout the week."

    return render_template('advanced_sleepanalytics.html', monday=monday, tuesday=tuesday, wednesday=wednesday,
                           thursday=thursday, friday=friday, saturday=saturday, sunday=sunday, analytic_statement=analytic_statement)

@app.route("/advanced-performance")
def advanced_performance():
    return render_template("advanced_performance.html")

@app.route('/advanced_behavioranalytics', methods=['GET', 'POST'])
def advanced_behavioranalytics():
    if request.method == 'POST':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        values = [int(request.form[day]) for day in days]

        # Determine trend
        increasing = all(values[i] <= values[i + 1] for i in range(len(values) - 1))
        decreasing = all(values[i] >= values[i + 1] for i in range(len(values) - 1))
        consistent = all(abs(values[i] - values[i + 1]) <= 1 for i in range(len(values) - 1))

        if increasing:
            analytic_statement = "📈 Your phone usage is increasing. Try to reduce your screen time!"
        elif decreasing:
            analytic_statement = "✅ Great! Your phone usage is decreasing. Keep up the real-world focus!"
        elif consistent:
            analytic_statement = "📊 Your phone usage is consistent. Maintain a healthy balance!"
        else:
            analytic_statement = "⚠️ Your usage is fluctuating. Try to build a more consistent routine."

        return render_template(
            'advanced_behavioranalytics.html',
            monday=values[0], tuesday=values[1], wednesday=values[2],
            thursday=values[3], friday=values[4], saturday=values[5], sunday=values[6],
            analytic_statement=analytic_statement
        )

    return render_template('advanced_behavioranalytics.html')

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)