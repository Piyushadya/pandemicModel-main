from flask import Flask, request
from flask_cors import CORS
from sklearn.preprocessing import PolynomialFeatures
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import mysql.connector as mysql
import pymysql
import pickle

# COVID-19 infectious period is ~10 days, so an infected person will infect 1.5 others in their 10-day period
ECONOMIC_CSV_FILE_NAME = "Final.csv"
GDP_CSV_FILE_NAME = "GDP.csv"
FINALIZED_MODEL = 'finalized_model.sav'
# Enter your database credentials according to your system.
hostname="localhost"
dbname="CovidProject"
uname="root"
pwd="root1234"

# Load the trained model
LOADED_MODEL = pickle.load(open(FINALIZED_MODEL, 'rb'))

def eng():
    eng = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))
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

def analyzeRisk(locR, posRate, data, days, maxPop, infCycle=14, dynamicPR=1, dynamicR=0):
    column_names = ['PR', 'R', 'GrowthRate', 'NewStoreInfections', 'NewInfectionsByPrev', 'DailyNew', 'Cumulative', 'Active', 'Healthy', 'Recovered']
    df = pd.DataFrame(index=np.arange(days+1) , columns = column_names)

    # Calculate the total infected population of each store
    storesInfected = data.Quantity * data.AvgPop * posRate * (data.RelRisk / data.SubsectionCount) * data.RelChange * data.OpCapacity
    infected = np.sum(storesInfected)

    # Predict Daily New Cases using the machine learning model
    positivityRate = np.array(posRate).reshape(-1, 1)

    polyFeature = PolynomialFeatures(degree=5)
    X_predict = polyFeature.fit_transform(positivityRate)
    predicted_Y = LOADED_MODEL.predict(X_predict)

    # Day 0 cases = (input population from user / Canadian population) * model predicted cases
    predicted_Y = predicted_Y[0][0] * (maxPop / 38000000)

    # Update the first row
    df.loc[0, column_names] = [posRate,locR,0,infected,0,predicted_Y,predicted_Y,predicted_Y,maxPop-predicted_Y,0]

    for i in range(1,days+1):

        # New Store Infections
        storesInfected = data.Quantity * data.AvgPop * df.at[i-1,'PR'] * (data.RelRisk / data.SubsectionCount) * data.RelChange * data.OpCapacity
        infected = np.sum(storesInfected)
        df.at[i, 'NewStoreInfections'] = infected
        print(posRate, df.at[i-1,'PR'])


        # Recovered
        if (i<14):
            df.at[i,'Recovered'] = 0
        else:
            df.at[i,'Recovered'] = df.at[i-infCycle, 'DailyNew']


        # New Cases by Previously Infected
        df.at[i,'NewInfectionsByPrev'] = df.at[i-1,'Active'] * df.at[i-1,'R'] / infCycle


        # Total New Cases: limits between 0 and maxPop
        df.at[i,'DailyNew'] = df.at[i,'NewInfectionsByPrev'] + df.at[i,'NewStoreInfections']

        if (df.at[i,'DailyNew'] > maxPop):
            df.at[i,'DailyNew'] = maxPop

        if (df.at[i,'DailyNew'] < 0):
            df.at[i,'DailyNew'] = 0


        # Active Cases: limits between 0 and maxPop
        df.at[i,'Active'] = df.at[i-1,'Active'] + df.at[i,'DailyNew'] - df.at[i,'Recovered']

        if (df.at[i,'Active'] > maxPop):
            df.at[i,'Active'] = maxPop

        if (df.at[i,'Active'] < 0):
            df.at[i,'Active'] = 0


        # Cumulative Cases
        df.at[i,'Cumulative'] = df.at[i,'Active'] + df.at[i,'DailyNew']


        # Healthy Population: limits between 0 and maxPop
        df.at[i,'Healthy'] = maxPop - df.at[i,'Active']

        if (df.at[i,'Healthy'] > maxPop):
            df.at[i,'Healthy'] = maxPop

        if (df.at[i,'Healthy'] < 0):
            df.at[i,'Healthy'] = 0


        # PR: limits between 0 and 1
        if (dynamicPR == 0):
            df.at[i,'PR'] = posRate
        else:
            df.at[i,'PR'] = df.at[i,'DailyNew'] / maxPop

        if (df.at[i,'PR'] < 0):
            df.at[i,'PR'] = 0

        if (df.at[i,'PR'] > 1):
            df.at[i,'PR'] = 1

        # Growth Rate
        df.at[i,'GrowthRate'] = 0 #np.ln(df.at[i,'DailyNew']/df.at[i-1,'DailyNew'])

        # R
        if (dynamicR == 0):
            df.at[i,'R'] = locR
        else:
            df.at[i,'R'] = np.exp(df.at[i,'GrowthRate'])

    # return days, total, new, active
    total = df['Cumulative'].to_numpy()
    new = df['DailyNew'].to_numpy()
    active = df['Active'].to_numpy()
    x = np.arange(0,days+1)
    return x, total, new, active


# INPUT PARAMETERS
# lockdownIntensity : Intensity of restrictions - 100% implies full lockdown, 0% implies no restrictions
# data : matrix
def analyzeEconomicRisk():

    SQL_Query = pd.read_sql_query(
        '''select * from final''', eng())

    economic_df = pd.DataFrame(SQL_Query)
    economic_impact_df = pd.DataFrame()
    column_name = ['Total']
    economy_total = pd.DataFrame(index=np.arange(14) , columns = column_name)
    economic_impact_df['id'] = economic_df['id']
    economic_impact_df['Sector'] = economic_df['Sector']

    economic_impact_df['JobsChanged_1']= (economic_df['NumEmployees']) * (
        economic_df['April_20']) * economic_df['RestrictionsIntensity']

    economic_impact_df['JobsChanged_2']= (economic_df['NumEmployees'])/(1-(
        economic_df['May_20'])/100) * (
        economic_df['May_20']) * economic_df['RestrictionsIntensity']

    a = (economic_df['NumEmployees'])/(1-( economic_df['May_20'])/100)

    economic_impact_df['JobsChanged_3']= (a)/(1-(
        economic_df['June_20'])/100) * (
        economic_df['June_20']) * economic_df['RestrictionsIntensity']

    b = (a)/(1-(economic_df['June_20'])/100)

    economic_impact_df['JobsChanged_4']= (b)/(1-(
        economic_df['July_20'])/100) * (
        economic_df['July_20']) * economic_df['RestrictionsIntensity']
    c = (b)/(1-(economic_df['July_20'])/100)

    economic_impact_df['JobsChanged_5']= (c)/(1-(
        economic_df['August_20'])/100) * (
        economic_df['August_20']) * economic_df['RestrictionsIntensity']

    d = (c)/(1-(economic_df['August_20'])/100)

    economic_impact_df['JobsChanged_6']= (d)/(1-(
        economic_df['September_20'])/100) * (
        economic_df['September_20']) * economic_df['RestrictionsIntensity']

    e=(d)/(1-(economic_df['September_20'])/100)

    economic_impact_df['JobsChanged_7']= (e)/(1-(
        economic_df['October_20'])/100) * (
        economic_df['October_20']) * economic_df['RestrictionsIntensity']

    f = (e)/(1-(economic_df['October_20'])/100)

    economic_impact_df['JobsChanged_8']= (f)/(1-(
        economic_df['November_20'])/100) * (
        economic_df['November_20']) * economic_df['RestrictionsIntensity']
    g = (f)/(1-(economic_df['November_20'])/100)
    economic_impact_df['JobsChanged_9']= (g)/(1-(
        economic_df['December_20'])/100) * (
        economic_df['December_20']) * economic_df['RestrictionsIntensity']

    h = (g)/(1-(economic_df['December_20'])/100)

    economic_impact_df['JobsChanged_10']= (h)/(1-(
        economic_df['January_21'])/100) * (
        economic_df['January_21']) * economic_df['RestrictionsIntensity']
    i = (h)/(1-(economic_df['January_21'])/100)
    economic_impact_df['JobsChanged_11']= (i)/(1-(
        economic_df['February_21'])/100) * (
        economic_df['February_21']) * economic_df['RestrictionsIntensity']
    j = (i)/(1-(economic_df['February_21'])/100)
    economic_impact_df['JobsChanged_12']= (j)/(1-(
        economic_df['March_21'])/100) * (
        economic_df['March_21']) * economic_df['RestrictionsIntensity']

    k = (j)/(1-(economic_df['March_21'])/100)
    economic_impact_df['JobsChanged_13']= (k)/(1-(
        economic_df['April_21'])/100) * (
        economic_df['April_21']) * economic_df['RestrictionsIntensity']
    l =(k)/(1-(economic_df['April_21'])/100)

    economic_impact_df['JobsChanged_14']= (l)/(1-(
        economic_df['May_21'])/100) * (
        economic_df['May_21']) * economic_df['RestrictionsIntensity']

    #Jobs changed
    economy_total.at[0,'Total']= economic_impact_df['JobsChanged_1'].sum()
    economy_total.at[1,'Total']= economic_impact_df['JobsChanged_2'].sum()
    economy_total.at[2,'Total']= economic_impact_df['JobsChanged_3'].sum()
    economy_total.at[3,'Total']= economic_impact_df['JobsChanged_4'].sum()
    economy_total.at[4,'Total']= economic_impact_df['JobsChanged_5'].sum()
    economy_total.at[5,'Total']= economic_impact_df['JobsChanged_6'].sum()
    economy_total.at[6,'Total']= economic_impact_df['JobsChanged_7'].sum()
    economy_total.at[7,'Total']= economic_impact_df['JobsChanged_8'].sum()
    economy_total.at[8,'Total']= economic_impact_df['JobsChanged_9'].sum()
    economy_total.at[9,'Total']= economic_impact_df['JobsChanged_10'].sum()
    economy_total.at[10,'Total']= economic_impact_df['JobsChanged_11'].sum()
    economy_total.at[11,'Total']= economic_impact_df['JobsChanged_12'].sum()
    economy_total.at[12,'Total']= economic_impact_df['JobsChanged_13'].sum()
    economy_total.at[13,'Total']= economic_impact_df['JobsChanged_14'].sum()


    economy_jobs = economy_total['Total'].to_numpy()
    q = np.arange(0,14)
    return q, economy_jobs


#GDP changed
def analyzeGdpRisk():
    SQL_Query = pd.read_sql_query(
        '''select * from gdp''', eng())

    gdp_df = pd.DataFrame(SQL_Query)
    gdp_impact_df = pd.DataFrame()
    column_name = ['Total']
    gdp_total = pd.DataFrame(index=np.arange(14) , columns = column_name)

    gdp_impact_df['id'] = gdp_df['id']
    gdp_impact_df['Sector'] = gdp_df['Sector']

    gdp_impact_df['GDPImpact1'] = gdp_df['April_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact2'] = gdp_df['May_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact3'] = gdp_df['June_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact4'] = gdp_df['July_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact5'] = gdp_df['August_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact6'] = gdp_df['September_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact7'] = gdp_df['October_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact8'] = gdp_df['November_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact9'] = gdp_df['December_20'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact10'] = gdp_df['January_21'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact11'] = gdp_df['February_21'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact12'] = gdp_df['March_21'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact13'] = gdp_df['April_21'] *(
        gdp_df['RestrictionsIntensity'])
    gdp_impact_df['GDPImpact14'] = gdp_df['May_21'] *(
        gdp_df['RestrictionsIntensity'])

    gdp_total.at[0,'Total']= gdp_impact_df['GDPImpact1'].mean()
    gdp_total.at[1,'Total']= gdp_impact_df['GDPImpact2'].mean()
    gdp_total.at[2,'Total']= gdp_impact_df['GDPImpact3'].mean()
    gdp_total.at[3,'Total']= gdp_impact_df['GDPImpact4'].mean()
    gdp_total.at[4,'Total']= gdp_impact_df['GDPImpact5'].mean()
    gdp_total.at[5,'Total']= gdp_impact_df['GDPImpact6'].mean()
    gdp_total.at[6,'Total']= gdp_impact_df['GDPImpact7'].mean()
    gdp_total.at[7,'Total']= gdp_impact_df['GDPImpact8'].mean()
    gdp_total.at[8,'Total']= gdp_impact_df['GDPImpact9'].mean()
    gdp_total.at[9,'Total']= gdp_impact_df['GDPImpact10'].mean()
    gdp_total.at[10,'Total']= gdp_impact_df['GDPImpact11'].mean()
    gdp_total.at[11,'Total']= gdp_impact_df['GDPImpact12'].mean()
    gdp_total.at[12,'Total']= gdp_impact_df['GDPImpact13'].mean()
    gdp_total.at[13,'Total']= gdp_impact_df['GDPImpact14'].mean()

    gdp = gdp_total['Total'].to_numpy()
    s = np.arange(0,14)
    return s, gdp

#Business closed
def analyzeBusinessRisk():
    SQL_Query = pd.read_sql_query(
        '''select * from final''', eng())

    business_df = pd.DataFrame(SQL_Query)
    business_impact_df = pd.DataFrame()
    column_name = ['Total']
    business_total = pd.DataFrame(index=np.arange(14) , columns = column_name)

    business_impact_df['id'] = business_df['id']
    business_impact_df['Sector'] = business_df['Sector']

    business_impact_df['BusinessesClosed_1'] = (business_df['NumBusinesses']) * (
        business_df['April_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_2'] = (business_df['NumBusinesses']) * (
        business_df['May_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_3'] = (business_df['NumBusinesses']) * (
        business_df['June_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_4'] = (business_df['NumBusinesses']) * (
        business_df['July_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_5'] = (business_df['NumBusinesses']) * (
        business_df['August_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_6'] = (business_df['NumBusinesses']) * (
        business_df['September_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_7'] = (business_df['NumBusinesses']) * (
        business_df['October_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_8'] = (business_df['NumBusinesses']) * (
        business_df['November_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_9'] = (business_df['NumBusinesses']) * (
        business_df['December_20_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_10'] = (business_df['NumBusinesses']) * (
        business_df['January_21_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_11'] = (business_df['NumBusinesses']) * (
        business_df['February_21_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_12'] = (business_df['NumBusinesses']) * (
        business_df['March_21_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_13'] = (business_df['NumBusinesses']) * (
        business_df['April_21_bus']) * business_df['RestrictionsIntensity']
    business_impact_df['BusinessesClosed_14'] = (business_df['NumBusinesses']) * (
        business_df['May_21_bus']) * business_df['RestrictionsIntensity']

    business_total.at[0,'Total']= business_impact_df['BusinessesClosed_1'].sum()
    business_total.at[1,'Total']= business_impact_df['BusinessesClosed_2'].sum()
    business_total.at[2,'Total']= business_impact_df['BusinessesClosed_3'].sum()
    business_total.at[3,'Total']= business_impact_df['BusinessesClosed_4'].sum()
    business_total.at[4,'Total']= business_impact_df['BusinessesClosed_5'].sum()
    business_total.at[5,'Total']= business_impact_df['BusinessesClosed_6'].sum()
    business_total.at[6,'Total']= business_impact_df['BusinessesClosed_7'].sum()
    business_total.at[7,'Total']= business_impact_df['BusinessesClosed_8'].sum()
    business_total.at[8,'Total']= business_impact_df['BusinessesClosed_9'].sum()
    business_total.at[9,'Total']= business_impact_df['BusinessesClosed_10'].sum()
    business_total.at[10,'Total']= business_impact_df['BusinessesClosed_11'].sum()
    business_total.at[11,'Total']= business_impact_df['BusinessesClosed_12'].sum()
    business_total.at[12,'Total']= business_impact_df['BusinessesClosed_13'].sum()
    business_total.at[13,'Total']= business_impact_df['BusinessesClosed_14'].sum()

    business = business_total['Total'].to_numpy()
    t = np.arange(0,14)
    return t, business

app = Flask(__name__)
CORS(app)


@ app.route("/cases", methods=['POST'])
def cases():
    if request.method == 'POST':
        client_data = request.get_json()
        cases_df = ConnectSql()
        x, y_total, y_new, y_active = analyzeRisk(
            client_data["rValue"], client_data["positivityRate"], cases_df, client_data["numDays"], client_data["population"])
        return {'x': x.tolist(), 'y_total': y_total.tolist(), 'y_new': y_new.tolist(), 'y_active': y_active.tolist()}


@ app.route("/metrics", methods=['GET', 'POST'])
def metrics():
    if request.method == 'GET':
        cases_df = ConnectSql()
        return cases_df.to_json(orient="records")


subsection_to_industry_map = {
    'Sports and Rec': 13, 'Self Care': 12, 'School': 11, 'Social Gathering': 13, 'Religious Gathering': 15, 'Shopping': 6, 'Restaurants': 14, 'Entertainment': 13, 'University/College': 11,
    'Health Care': 12, 'Self Care': 15, 'Economic': 8, 'Personal Services': 15, 'Nature': 13, 'Community Services': 15, 'Attractions and Heritage': 13, 'Animal Services': 15}


@ app.route("/setEconomyMetrics", methods=['POST'])
def set_economy_metrics():
    if request.method == 'POST':
        new_economic_metric = request.get_json()
        engine = eng()
        SQL_Query4 = pd.read_sql_query(
            '''select * from final''', engine)

        economy_df = pd.DataFrame(SQL_Query4)

        economy_df.loc[[new_economic_metric["id"] - 1], [new_economic_metric["field"]]
                       ] = float(new_economic_metric["newVal"])

        economy_df = economy_df.set_index('id')
         # Convert dataframe to sql table
        economy_df.to_sql('oo', engine, if_exists = 'replace', index = True)
        dbConnection4 = engine.connect()
        # Convert dataframe to sql table
        trans4 = dbConnection4.begin()
        engine.execute('delete from final where id in (select id from oo)')
        trans4.commit()
        economy_df.to_sql('final', engine, if_exists = 'append', index = True)
        engine.execute('drop table oo')

        return "economic metric updated"


@ app.route("/setCasesMetrics", methods=['POST'])
def set_cases_metrics():
    if request.method == 'POST':
        new_cases_metric = request.get_json()
        cases_df = ConnectSql()

        cases_df.loc[[new_cases_metric["id"] - 1], [new_cases_metric["field"]]
                     ] = float(new_cases_metric["newVal"])

        updateCasesTable(cases_df)

        return "cases metric updated"


@ app.route("/opCapacity", methods=['POST'])
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


        engine = eng()
        SQL_Query1 = pd.read_sql_query(
            '''select * from final''', engine)
        economic_df = pd.DataFrame(SQL_Query1)
        economic_df.loc[[subsection_to_industry_map[subsection] - 1], ["RestrictionsIntensity"]
                        ] = float(1 - op_capacity_mean)
        economic_df = economic_df.set_index('id')

         # Convert dataframe to sql table
        economic_df.to_sql('eco', engine, if_exists = 'replace', index = True)
        dbConnection9 = engine.connect()
        trans = dbConnection9.begin()
        engine.execute('delete from final where id in (select id from eco)')
        trans.commit()
        economic_df.to_sql('final', engine, if_exists = 'append', index = True)
        engine.execute('drop table eco')


        #GDP
        SQL_Query = pd.read_sql_query(
            '''select * from gdp''', engine)

        gdp_df = pd.DataFrame(SQL_Query)

        gdp_df.loc[[subsection_to_industry_map[subsection] - 1], ["RestrictionsIntensity"]
                        ] = float(1 - op_capacity_mean)
        gdp_df = gdp_df.set_index('id')
        # Convert dataframe to sql table
        #engine1 = eng()
        gdp_df.to_sql('my', engine, if_exists = 'replace', index = True)
        dbConnection = engine.connect()
        trans = dbConnection.begin()
        engine.execute('delete from gdp where id in (select id from my)')
        trans.commit()
        gdp_df.to_sql('gdp', engine, if_exists = 'append', index = True)
        engine.execute('drop table my')


        return "operational capacity and restriction intensity updated"


@ app.route("/economy/data", methods=['POST'])
def economicImpact():
    if request.method == 'POST':
        q , jobs_changed = analyzeEconomicRisk()
        return {'q': q.tolist(), 'jobs_changed': jobs_changed.tolist()}

#GDP #piyush
@ app.route("/economy/data/Gdp", methods=['POST'])
def gdpImpact():
    if request.method == 'POST':
        s , gdp_changed = analyzeGdpRisk()
        return {'s': s.tolist(), 'gdp_changed': gdp_changed.tolist()}

#Businesses closed #piyush
@ app.route("/economy/data/Business", methods=['POST'])
def businessImpact():
    if request.method == 'POST':
        t , business_closed = analyzeBusinessRisk()
        return {'t': t.tolist(), 'business_closed': business_closed.tolist()}


@ app.route("/economy/metrics", methods=['GET'])
def economicMetrics():
    if request.method == 'GET':
        SQL_Query7 = pd.read_sql_query(
            '''select * from final''', eng())
        economic_metrics_df = pd.DataFrame(SQL_Query7)
        return economic_metrics_df.to_json(orient="records")
