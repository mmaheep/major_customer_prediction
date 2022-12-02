import pickle
from flask import Flask,request,jsonify,render_template
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
model = pickle.load(open("model.pkl","rb"))
d = pickle.load(open("LabelEncodingDict.pkl","rb"))
ss = pickle.load(open("StandardScaler.pkl","rb"))
rfm = pd.read_csv('RFM_data.csv',encoding='unicode-escape')


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods = ['POST'])
def predict():
    features = [x for x in request.form.values()]
    seg_in = features[-1]
    features = features[:-1]
    inp1 = [1.0]
    inp1.append(float(features[0]))
    inp3 = [abs(int(features[-1])-int(features[-2]))]
    features = features[1:-2]
    inp2 = [["Type"],["Delivery Status"],["Customer City"],["Customer Country"],["Customer Segment"],["Customer State"],["Department Name"],["Order City"],["Order Region"],["Shipping Mode"]]
    for i in range(len(features)):
        inp2[i].append(features[i])
    inp = inp1+[d[x[0]].transform([x[1]])[0] for x in inp2]+inp3
    final_features = [np.array(inp)]
    score = model.predict(ss.transform([inp]))[0]
    dis = "a fraud"
    seg = rfm.loc[rfm['Order Customer Id'] == int(seg_in)]["Customer_Segmentation"].item()
    if score == 0:
        dis = "not a fraud"
        return render_template("index.html",disply_text = f"The customer is {dis} and their Customer Segmetation is : {seg}")
    else:
        return render_template("index.html",disply_text = f"The customer is {dis}")
if __name__ == "__main__":
    app.run(debug=False)
