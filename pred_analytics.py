import getdata
import userinput as ui
import datetime as dt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn import metrics
import matplotlib.pyplot as plt


def get_pred_days(model_data):
    '''Let user input a prediction date,
       get date range from the end of training date to user input predition date'''
    while True:
        training_end_date = model_data.index[-1]  # timestamp
        pred_date = ui.get_date("PREDICTION")  # datetime
        # prediction date cannot after the training end date
        if pred_date > training_end_date:
            pred_days = pd.date_range(
                training_end_date, pred_date, freq='D')[1:]
            return pred_days
            break
        else:
            ui.errorprint("PREDICTION DATE SHOULD AFTER TRAINING END DATE")


def dataset_split(model_data):
    '''split traning data'''
    date = np.array(model_data.index.map(dt.datetime.toordinal)).reshape(-1, 1)
    price = np.array(model_data["Close"])
    date_train, date_test, price_train, price_test = train_test_split(
        date, price, test_size=0.20)
    return date_train, date_test, price_train, price_test


def RMSE_score(price_test, price_test_pred):
    '''Calcualte RMSE score'''
    MSE = metrics.mean_squared_error(price_test, price_test_pred)
    RMSE = np.sqrt(MSE)
    return RMSE


def lr_model(model_data, pred_days):
    '''Linear Regression model
       Get r2, RMSE, and the prediction prices list from LR model'''
    date_train, date_test, price_train, price_test = dataset_split(model_data)
    lr = LinearRegression()
    lr.fit(date_train, price_train)
    # get r2 score
    r2 = lr.score(date_test, price_test)
    # get RMSE score
    price_test_pred = lr.predict(date_test)
    RMSE = RMSE_score(price_test, price_test_pred)
    # get prediction price from training_end_date to user's prediction date
    pred_days = np.array(pred_days.map(dt.datetime.toordinal)).reshape(-1, 1)
    pred_prices = lr.predict(pred_days)
    return r2, RMSE, pred_prices


def svr_model(model_data, pred_days):
    '''Support Vector Regression model
       Get r2, RMSE, and the prediction prices list from SVR model'''
    date_train, date_test, price_train, price_test = dataset_split(model_data)
    svr = SVR(kernel="rbf", C=1000, gamma=0.1)
    svr.fit(date_train, price_train)
    # get r2 score
    r2 = svr.score(date_test, price_test)
    # get RMSE score
    price_test_pred = svr.predict(date_test)
    RMSE = RMSE_score(price_test, price_test_pred)
    # get prediction price from training_end_date to user's prediction date
    pred_days = np.array(pred_days.map(dt.datetime.toordinal)).reshape(-1, 1)
    pred_prices = svr.predict(pred_days)
    return r2, RMSE, pred_prices


def get_pred_result(model_data, pred_days, symbol):
    '''A table that shows the r2, RMSE, and prediction date stock price
       for both LR and SVR prediction model'''
    # get LR prediction date stock price
    lr_pred_price = lr_model(model_data, pred_days)[-1][-1]
    # get LR r2, RMSE score
    lr_result = list(lr_model(model_data, pred_days)[0:2])
    # add the prediction price to the score list
    lr_result.append(lr_pred_price)
    # get SVR prediction date stock price
    svr_pred_price = svr_model(model_data, pred_days)[-1][-1]
    # get SVR r2, RMSE score
    svr_result = list(svr_model(model_data, pred_days)[0:2])
    # add the prediction price to the score list
    svr_result.append(svr_pred_price)
    pred_date = pred_days[-1]
    col = ["r2 Score", "RMSE Score",
           "{} Prediction Price $ ({})".format(symbol.upper(), pred_date.strftime('%Y-%m-%d'))]
    idx = ["Linear Regression", "Support Vector Regression"]
    pred_result = pd.DataFrame([lr_result, svr_result],
                               columns=col, index=idx)
    ui.print_table(pred_result, "PREDICTION RESULT")


def get_pred_graph(model_data, symbol, pred_days):
    '''show prediction model data prediction, SVR, LR prediciton in one graph'''
    graph_data = model_data.reset_index()
    pred_days = pred_days.to_frame(index=False, name="Date")
    graph_data = graph_data.append(pred_days, ignore_index=True)
    graph_data = graph_data.set_index("Date")
    all_pred_days = graph_data.index
    graph_data["LR_Prediction"] = lr_model(model_data, all_pred_days)[-1]
    graph_data["SVR_Prediction"] = svr_model(model_data, all_pred_days)[-1]
    graph_data.plot()
    plt.title("{} Stock Prediction".format(symbol).upper())
    plt.ylabel("Price ($)")
    plt.show()


def main():
    model_data, symbol = getdata.get_hist_data(
        "symbol", "TRAINING START", "TRAINING END")
    model_data = model_data.loc[:, ["Close"]]
    pred_days = get_pred_days(model_data)
    get_pred_result(model_data, pred_days, symbol)
    get_pred_graph(model_data, symbol, pred_days)


if __name__ == '__main__':
    main()
