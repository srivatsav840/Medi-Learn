import flask
from flask import Flask, request, render_template, redirect, jsonify
import mysql.connector
import _mysql_connector
import os
import pandas as pd
from bardapi import Bard
import os
import time

var1 = Flask(__name__)


@var1.route("/", methods=['GET', 'POST'])
def zeropage():
    return render_template('hzero.html')


@var1.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username1 = request.form["username1"]
        password1 = request.form["password1"]
        mydb4 = mysql.connector.connect(host="localhost", user="root", passwd="sri@vatsav840", database="medico")
        myc4 = mydb4.cursor()
        q4 = "insert into medilogin(username,password) values(%s,%s)"
        values = (username1, password1)
        myc4.execute(q4, values)
        res4 = myc4.fetchone()
        mydb4.commit()
        mydb4.close()
        if res4:
            pop1 = "oops!Signup not successfull try again!"
        else:
            pop1 = "Signup successfull! You can login now"
        return render_template("hsignup.html", pop1=pop1)

    else:
        return render_template("hsignup.html")


@var1.route("/login", methods=["POST", "GET"])
def loginpage():
    if request.method == 'POST':
        s1 = request.form["username"]
        s2 = request.form["password"]
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="sri@vatsav840", database="medico")
        myc = mydb.cursor()
        q = "select * from medilogin where username=%s and password=%s"
        values = (s1, s2)
        myc.execute(q, values)
        res = myc.fetchone()
        if res:
            s = "login successfull"
            return redirect('/medico')
        else:
            s = "invalid credentials! try again"
            return render_template('hlogin.html', s=s)
    else:
        return render_template('hlogin.html')


@var1.route("/adminlogin", methods=["POST", "GET"])
def adlogin():
    if request.method == 'POST':
        sk = request.form["username"]
        sk1 = request.form["password"]
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="sri@vatsav840", database="medico")
        myc = mydb.cursor()
        q = "select * from medisignup where usename=%s and password=%s"
        values = (sk, sk1)
        myc.execute(q, values)
        res = myc.fetchone()
        if res:
            s = "login successfull"
            return redirect('/adwork')
        else:
            s = "invalid credentials! try again"
            return render_template('adminlog.html', s=s)
    else:
        return render_template('adminlog.html')


csv_file = "C:\\Users\\sriva\\OneDrive\\Desktop\\medilearn\\Medicine_Details.csv"
df = pd.read_csv(csv_file)
symptoms_data = df['Uses'].unique()


@var1.route("/medico", methods=["POST", "GET"])
def meddes():
    detailed_results = []

    if request.method == 'POST':
        selected_disease = request.form['disease_select']

        if selected_disease:

            result = df[df['Uses'].str.contains(selected_disease, case=False, na=False)]

            if not result.empty:

                for index, row in result.iterrows():
                    medicine_name = f"Medicine Name: {row['Medicine Name']}"
                    composition = f"Composition: {row['Composition']}"
                    uses = f"Disease: {row['Uses']}"
                    side_effects = f"Side Effects: {row['Side_effects']}"
                    image_url = f"Image URL: <a href='{row['Image URL']}' target='_blank'>{row['Image URL']}</a>"
                    manufacturer = f"Manufacturer: {row['Manufacturer']}"
                    excellent_review = f"Excellent Review %: {row['Excellent Review %']}"
                    average_review = f"Average Review %: {row['Average Review %']}"
                    poor_review = f"Poor Review %: {row['Poor Review %']}<p></p><p></p>"  # Added line break

                    detailed_results.extend(
                        [medicine_name, composition, uses, side_effects, image_url, manufacturer,
                         excellent_review, average_review, poor_review]
                    )

                return render_template('med.html', results=detailed_results)
            else:

                not_found_message = (
                    f"Oops! No information found for '{selected_disease}'."
                    "Why don't you ask the AI doctor?"
                )

                return render_template('med.html', error=not_found_message)

    unique_diseases = sorted(df['Uses'].unique())
    return render_template('med.html', unique_diseases=unique_diseases, results=None)


@var1.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get('query', '')

    if query:
        matches = df[df['Uses'].str.contains(query, case=False, na=False)]['Uses'].unique()
    else:
        matches = df['Uses'].unique()

    return jsonify(matches.tolist())


os.environ["REPLICATE_API_TOKEN"] = "r8_NJ8chjg5aQz0qX1qgnBH0u30qghhbPE17oD6b"


@var1.route("/aidoctor", methods=["POST", "GET"])
def aidoc():
    if request.method == 'POST':
        try:

            inputai = request.form.get("inputai")
            if not inputai:
                raise ValueError("Invalid input")

            # Define prompts and parameters
            pre_prompt = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
            model_prompt = f"can u tell me about {inputai} exactly in 200 words and must end with."

            # Call Replicate API
            output = replicate.run(
                'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                input={"prompt": model_prompt, "temperature": 0.1, "top_p": 0.9, "max_length": 500,
                       "repetition_penalty": 1}
            )
            full_response = "".join(output)

            return render_template('aidoc.html', full_response=full_response)
        except Exception as e:
            # Log the error for debugging
            print(f"Error: {str(e)}")
            return render_template('aidoc.html', error_message="An error occurred.")
    else:
        return render_template('aidoc.html')


@var1.route("/adwork", methods=["GET", "POST"])
def adwork():
    if request.method == 'POST':
        ef = pd.read_csv(
            "C:\\Users\\sriva\\OneDrive\\Desktop\\medilearn\\Medicine_Details.csv")
        medicinename = request.form['medicinename']
        composition = request.form['composition']
        uses = request.form['uses']
        sideeffects = request.form['sideeffects']
        imgurl = request.form['image']
        manufacturer = request.form['manufacturer']
        new_data = {
            'Medicine Name': medicinename,
            'Composition': composition,
            'Uses': uses,
            'Side_effects': sideeffects,
            'Image URL': imgurl,
            'Manufacturer': manufacturer
        }
        ef = ef._append(new_data, ignore_index=True)
        ef.to_csv("C:\\Users\\sriva\\OneDrive\\Desktop\\medilearn\\Medicine_Details.csv",
                  index=False)
        popmsg = "data uploaded successfully"
        return render_template('adworkk.html', popmsg=popmsg)
    else:
        return render_template('adworkk.html')


if __name__ == "__main__":
    var1.run(host="0.0.0.0", port=5001, debug=True)
