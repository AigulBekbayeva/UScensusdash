
This is the app for US census data from 1990
Original data were taken from https://archive.ics.uci.edu/dataset/116/us+census+data+1990, created by Meek Meek, Thiesson Thiesson, Heckerman Heckerman

The following attributes were chosen from the dataset:
Age, Sex, Occupation, Marital status, Fertility, Industry, earning, and income
All data types of attributes are categorical. (Income and earnings were taken as continuous variables as having more values)

The app is https://dash-us-census-xoay2fh4ha-em.a.run.app/ 

This app was created in Python (jupyter notebook), with Pycharm to build a virtual environment, and also pip manager to download libraries listed in requirements.txt

In order to use the app locally: 
1) install python, pip
2) run pip install -r requirements.txt
3) change in app.py the last line: from "app.run(debug=False,host='0.0.0.0', port=8080)" to "app.run(debug=True)"
4) run app.py 

#To use the app on the Google Cloud run:
1) create your own project on Google Cloud console
2) change project ID
3) run the following with your own project ID
gcloud builds submit --tag gcr.io/uscensus1990/dash-us-census --project=uscensus1990

gcloud run deploy --image gcr.io/uscensus1990/dash-us-census --platform managed  --project=uscensus1990 --allow-unauthenticated
