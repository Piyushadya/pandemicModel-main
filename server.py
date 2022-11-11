from flask import Flask, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import pymysql
from sklearn.preprocessing import PolynomialFeatures
import pickle

from sqlalchemy import create_engine

# COVID-19 infectious period is ~10 days, so an infected person will infect 1.5 others in their 10-day period
ECONOMIC_CSV_FILE_NAME = 'sample_economic_data.csv'
FINALIZED_MODEL = 'finalized_model1.sav'

if __name__ == '__main__':
    app.run(debug=True)
# Load the trained model
LOADED_MODEL = pickle.load(open(FINALIZED_MODEL, 'rb'))


# INPUT PARAMETERS
# locR : initial local R factor (assumption in the code: an infected person will infect locR others in a 10-day infectious period)
# posRate : initial percentage of tests that are positive
# data : matrix containing business subsection, business type, number of businesses,
#        average population during non-covid, operating capacity percentage, relative risk factor
# days : how many days in the future we want to see (integer)
# maxPop : population of modeled local area
# infCycle : how long the infectious cycle is (COVID = 14 days)
# dynamicPR : 0 = static positivity rate, 1 = dynamic positivity rate
# dynamicR : 0 = static reproduction number, 1 = dynamic reproduction number (not yet set up)
#
# OUTPUT PARAMETERS:
# x : timeline
# y_new: new cases
# y_total: total cases
# y_active : active case (assumption: the average case recovers in 20 days)

def eng():
    eng=create_engine("mysql+mysqldb://root:root1234@localhost/CovidProject")
    return eng

def ConnectSql():
    dbConn = eng()
    data=pd.read_sql_query('''select * from sample_covid_data''',dbConn)
    cases_df = pd.DataFrame(data)
    return cases_df

def updateCasesTable(cases_df):
    global engine,dbconnection
    cases_df = cases_df.set_index('id')
    engine=eng()
    cases_df.to_sql("ChangedRows",engine,if_exists="replace",index = True)
    dbconnection=engine.connect()
    trans=dbconnection.begin()
    engine.execute('delete from sample_covid_data where id in (select id from ChangedRows)')
    engine.execute('Drop table ChangedRows')
    cases_df.to_sql('sample_covid_data', engine, if_exists="append", index = True)
    trans.commit()

def analyzeRisk(locR, posRate, data, days, maxPop, infCycle=14, dynamicPR=1, dynamicR=0):
    column_names = ['PR', 'R', 'GrowthRate', 'NewStoreInfections', 'NewInfectionsByPrev', 'DailyNew', 'Cumulative',
                    'Active', 'Healthy', 'Recovered']
    df = pd.DataFrame(index=np.arange(days + 1), columns=column_names)

    # Calculate the total infected population of each store
    storesInfected = data.Quantity * data.AvgPop * posRate * (
            data.RelRisk / data.SubsectionCount) * data.RelChange * data.OpCapacity
    infected = np.sum(storesInfected)

    # Predict Daily New Cases using the machine learning model
    positivityRate = np.array(posRate).reshape(-1, 1)

    polyFeature = PolynomialFeatures(degree=5)
    X_predict = polyFeature.fit_transform(positivityRate)
    predicted_Y = LOADED_MODEL.predict(X_predict)

    # Day 0 cases = (input population from user / Canadian population) * model predicted cases
    predicted_Y = predicted_Y[0][0] * (maxPop / 38000000)

    # Update the first row
    df.loc[0, column_names] = [posRate, locR, 0, infected, 0, predicted_Y, predicted_Y, predicted_Y,
                               maxPop - predicted_Y, 0]

    for i in range(1, days + 1):

        # New Store Infections
        storesInfected = data.Quantity * data.AvgPop * df.at[i - 1, 'PR'] * (
                data.RelRisk / data.SubsectionCount) * data.RelChange * data.OpCapacity
        infected = np.sum(storesInfected)
        df.at[i, 'NewStoreInfections'] = infected
        print(posRate, df.at[i - 1, 'PR'])

        # Recovered
        if (i < 14):
            df.at[i, 'Recovered'] = 0
        else:
            df.at[i, 'Recovered'] = df.at[i - infCycle, 'DailyNew']

        # New Cases by Previously Infected
        df.at[i, 'NewInfectionsByPrev'] = df.at[i - 1, 'Active'] * df.at[i - 1, 'R'] / infCycle

        # Total New Cases: limits between 0 and maxPop
        df.at[i, 'DailyNew'] = df.at[i, 'NewInfectionsByPrev'] + df.at[i, 'NewStoreInfections']

        if (df.at[i, 'DailyNew'] > maxPop):
            df.at[i, 'DailyNew'] = maxPop

        if (df.at[i, 'DailyNew'] < 0):
            df.at[i, 'DailyNew'] = 0

        # Active Cases: limits between 0 and maxPop
        df.at[i, 'Active'] = df.at[i - 1, 'Active'] + df.at[i, 'DailyNew'] - df.at[i, 'Recovered']

        if (df.at[i, 'Active'] > maxPop):
            df.at[i, 'Active'] = maxPop

        if (df.at[i, 'Active'] < 0):
            df.at[i, 'Active'] = 0

        # Cumulative Cases
        df.at[i, 'Cumulative'] = df.at[i, 'Active'] + df.at[i, 'DailyNew']

        # Healthy Population: limits between 0 and maxPop
        df.at[i, 'Healthy'] = maxPop - df.at[i, 'Active']

        if (df.at[i, 'Healthy'] > maxPop):
            df.at[i, 'Healthy'] = maxPop

        if (df.at[i, 'Healthy'] < 0):
            df.at[i, 'Healthy'] = 0

        # PR: limits between 0 and 1
        if (dynamicPR == 0):
            df.at[i, 'PR'] = posRate
        else:
            df.at[i, 'PR'] = df.at[i, 'DailyNew'] / maxPop

        if (df.at[i, 'PR'] < 0):
            df.at[i, 'PR'] = 0

        if (df.at[i, 'PR'] > 1):
            df.at[i, 'PR'] = 1

        # Growth Rate
        df.at[i, 'GrowthRate'] = 0  # np.ln(df.at[i,'DailyNew']/df.at[i-1,'DailyNew'])

        # R
        if (dynamicR == 0):
            df.at[i, 'R'] = locR
        else:
            df.at[i, 'R'] = np.exp(df.at[i, 'GrowthRate'])

    # return days, total, new, active
    total = df['Cumulative'].to_numpy()
    new = df['DailyNew'].to_numpy()
    active = df['Active'].to_numpy()
    x = np.arange(0, days + 1)
    return x, total, new, active


# INPUT PARAMETERS
# lockdownIntensity : Intensity of restrictions - 100% implies full lockdown, 0% implies no restrictions
# data : matrix
def analyzeEconomicRisk():
    economic_df = pd.read_csv(ECONOMIC_CSV_FILE_NAME)

    economic_impact_df = pd.DataFrame()
    economic_impact_df['id'] = economic_df['id']
    economic_impact_df['Sector'] = economic_df['Sector']
    economic_impact_df['JobsChanged'] = (economic_df['NumEmployees']) * (
        economic_df['JobsChangeFactor']) * economic_df['RestrictionsIntensity']
    economic_impact_df['GDPImpact'] = economic_df['GDPImpactFactor'] * \
                                      economic_df['RestrictionsIntensity']
    economic_impact_df['BusinessesClosed'] = (economic_df['NumBusinesses']) * (
        economic_df['BusinessesClosedFactor']) * economic_df['RestrictionsIntensity']

    return economic_impact_df, economic_impact_df['JobsChanged'].sum(), economic_impact_df['GDPImpact'].mean(), \
           economic_impact_df['BusinessesClosed'].sum()


app = Flask(__name__)
CORS(app)


@app.route("/cases", methods=['POST'])
def cases():
    if request.method == 'POST':
        client_data = request.get_json()
        cases_df = ConnectSql()
        x, y_total, y_new, y_active = analyzeRisk(
            client_data["rValue"], client_data["positivityRate"], cases_df, client_data["numDays"],
            client_data["population"])

        return {'x': x.tolist(), 'y_total': y_total.tolist(), 'y_new': y_new.tolist(), 'y_active': y_active.tolist()}


@app.route("/metrics", methods=['GET', 'POST'])
def metrics():
    if request.method == 'GET':
        cases_df = ConnectSql()
        return cases_df.to_json(orient="records")


subsection_to_industry_map = {
    'Sports and Rec': 13, 'Self Care': 12, 'School': 11, 'Social Gathering': 13, 'Religious Gathering': 15,
    'Shopping': 6, 'Restaurants': 14, 'Entertainment': 13, 'University/College': 11,
    'Health Care': 12, 'Self Care': 15, 'Economic': 8, 'Personal Services': 15, 'Nature': 13, 'Community Services': 15,
    'Attractions and Heritage': 13, 'Animal Services': 15}


@app.route("/setEconomyMetrics", methods=['POST'])
def set_economy_metrics():
    if request.method == 'POST':
        new_economic_metric = request.get_json()
        economy_df = pd.read_csv(ECONOMIC_CSV_FILE_NAME)

        economy_df.loc[[new_economic_metric["id"] - 1], [new_economic_metric["field"]]
        ] = float(new_economic_metric["newVal"])

        economy_df.to_csv(ECONOMIC_CSV_FILE_NAME, index=False)

        return "economic metric updated"


@app.route("/setCasesMetrics", methods=['POST'])
def set_cases_metrics():
    if request.method == 'POST':
        new_cases_metric = request.get_json()
        cases_df = ConnectSql()
        cases_df.loc[[new_cases_metric["id"] - 1], [new_cases_metric["field"]]
        ] = float(new_cases_metric["newVal"])
        updateCasesTable(cases_df)
        return "cases metric updated"


@app.route("/opCapacity", methods=['POST'])
def set_op_capacity():
    if request.method == 'POST':
        # calculate new cases
        new_op_capacity = request.get_json()
        print(type(new_op_capacity.get("OpCapacity")))
        cases_df = ConnectSql()

        cases_df.loc[[new_op_capacity["id"] - 1], ["OpCapacity"]
        ] = float(new_op_capacity["OpCapacity"])
        updateCasesTable(cases_df)
        # calculate new restrictions intensity for economic impact
        # get new average over the sectors
        subsection = cases_df.at[new_op_capacity["id"] - 1, "Subsection"]
        op_capacity_mean = (
            cases_df[cases_df["Subsection"] == subsection]["OpCapacity"]).mean()

        economic_df = pd.read_csv(ECONOMIC_CSV_FILE_NAME)
        economic_df.loc[[subsection_to_industry_map[subsection] - 1], ["RestrictionsIntensity"]
        ] = float(1 - op_capacity_mean)
        economic_df.to_csv(ECONOMIC_CSV_FILE_NAME, index=False)

        return "operational capacity and restriction intensity updated"


@app.route("/economy/data", methods=['POST'])
def economicImpact():
    if request.method == 'POST':
        (economic_impact_df, jobs_changed, gdp_impact,
         businesses_closed) = analyzeEconomicRisk()
        result_dict = {
            'metrics': economic_impact_df.to_json(orient="records"),
            'total_impact': {
                'JobsChanged': jobs_changed,
                'GDPImpact': gdp_impact,
                'BusinessesClosed': businesses_closed
            }
        }
        return result_dict


@app.route("/economy/metrics", methods=['GET'])
def economicMetrics():
    if request.method == 'GET':
        economic_metrics_df = pd.read_csv(ECONOMIC_CSV_FILE_NAME)

        return economic_metrics_df.to_json(orient="records")
