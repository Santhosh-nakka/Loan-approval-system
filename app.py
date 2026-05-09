from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# LOAD MODEL
model = pickle.load(open("logistic_regression_model.pkl", "rb"))

# HISTORY STORAGE
history = []

# HOME PAGE
@app.route('/')
def home():
    return render_template("home.html")


# DASHBOARD PAGE WITH REAL VALUES
@app.route('/dashboard')
def dashboard():

    total_predictions = len(history)

    approved_loans = len(
        [item for item in history if item["status"] == "Approved"]
    )

    rejected_loans = len(
        [item for item in history if item["status"] == "Rejected"]
    )

    return render_template(

        "dashboard.html",

        total_predictions=total_predictions,

        approved_loans=approved_loans,

        rejected_loans=rejected_loans
    )


# PREDICTION PAGE
@app.route('/predict-page')
def predict_page():
    return render_template("predict.html")


# ANALYTICS PAGE WITH REAL VALUES
@app.route('/analytics')
def analytics():

    total = len(history)

    approved = len(
        [item for item in history if item["status"] == "Approved"]
    )

    rejected = len(
        [item for item in history if item["status"] == "Rejected"]
    )

    # AVOID DIVISION ERROR

    if total == 0:

        approval_rate = 0

    else:

        approval_rate = round((approved / total) * 100)

    # INCOME ANALYTICS

    low = 0
    medium = 0
    high = 0

    for item in history:

        income = float(item["income"])

        if item["status"] == "Approved":

            if income < 3000:
                low += 1

            elif income < 7000:
                medium += 1

            else:
                high += 1

    return render_template(

        "analytics.html",

        total_customers=total,

        approved=approved,

        rejected=rejected,

        approval_rate=approval_rate,

        low=low,

        medium=medium,

        high=high
    )


# MODEL INFO PAGE
@app.route('/model-info')
def model_info():
    return render_template("model.html")


# HISTORY PAGE
@app.route('/history')
def prediction_history():

    return render_template(
        "history.html",
        history=history
    )


# PREDICTION ROUTE
@app.route('/predict', methods=['POST'])
def predict():

    features = [

        float(request.form['ApplicantIncome']),

        float(request.form['CoapplicantIncome']),

        float(request.form['LoanAmount']),

        float(request.form['Loan_Amount_Term']),

        float(request.form['Credit_History']),

        float(request.form['Gender_Male']),

        float(request.form['Married_Yes']),

        float(request.form['Dependents_1']),

        float(request.form['Dependents_2']),

        float(request.form['Dependents_3+']),

        float(request.form['Education_Not Graduate']),

        float(request.form['Self_Employed_Yes']),

        float(request.form['Property_Area_Semiurban']),

        float(request.form['Property_Area_Urban'])

    ]

    prediction = model.predict([features])

    # APPROVED / REJECTED RESULT

    if prediction[0] == 1:

        result = "✅ Loan Approved"

        result_image = "approved.png"

    else:

        result = "❌ Loan Rejected"

        result_image = "rejected.png"

    # SAVE HISTORY

    history.append({

        "income": request.form['ApplicantIncome'],

        "loan": request.form['LoanAmount'],

        "status": "Approved" if prediction[0] == 1 else "Rejected"

    })

    return render_template(

        "predict.html",

        prediction_text=result,

        result_image=result_image

    )


if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=5050,debug=True)