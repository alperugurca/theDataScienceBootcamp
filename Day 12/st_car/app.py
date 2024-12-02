import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import streamlit as st

df=pd.read_excel("cars.xls")
x=df.drop("Price",axis=1)
y=df[["Price"]]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

preprocessor=ColumnTransformer(
    transformers=[
        ("num",StandardScaler(),["Mileage","Cylinder","Doors","Cruise","Sound","Leather"]),
        ("cat",OneHotEncoder(),["Make","Model", "Trim","Type"])
    ]
)

model=LinearRegression()

pipeline=Pipeline(steps=[("preprocessor",preprocessor),("regressor",model)])

pipeline.fit(x_train,y_train)
pred=pipeline.predict(x_test)

rms=mean_squared_error(pred,y_test)**0.5
r2=r2_score(pred,y_test)

def price_pred(make, model, trim, mileage, car_type, cylinder, liter, doors, cruise, sound, leather):
    input_data = pd.DataFrame({
        "Make": [make],
        "Model": [model],
        "Trim": [trim],
        "Mileage": [mileage],
        "Type": [car_type],
        "Cylinder": [cylinder],
        "Liter": [liter],
        "Doors": [doors],
        "Cruise": [cruise],
        "Sound": [sound],
        "Leather": [leather]
    })
    prediction = pipeline.predict(input_data)[0]
    return float(prediction)  # Convert to float to ensure it's a scalar

def main():
    st.title("MLOps Car Price Prediction :car:")
    st.write("Ender Car Details to Predict the Price")

    make=st.selectbox("Make",df["Make"].unique())
    model=st.selectbox("Model",df[df["Make"]==make]["Model"].unique())
    trim=st.selectbox("Trim",df[(df["Make"]==make) & (df["Model"]==model)]["Trim"].unique())
    mileage = st.number_input("Mileage", min_value=int(df["Mileage"].min()), max_value=int(df["Mileage"].max()))
    car_type = st.selectbox("Type", df["Type"].unique())
    cylinder = st.number_input("Cylinder", min_value=int(df["Cylinder"].min()), max_value=int(df["Cylinder"].max()))
    liter = st.number_input("Liter", min_value=float(df["Liter"].min()), max_value=float(df["Liter"].max()), step=0.1)
    doors = st.number_input("Doors", min_value=int(df["Doors"].min()), max_value=int(df["Doors"].max()))
    cruise = st.radio("Cruise", df["Cruise"].unique())
    sound = st.radio("Sound", df["Sound"].unique())
    leather = st.radio("Leather", df["Leather"].unique())


    if st.button("Predict"):
        predicted_price = price_pred(make, model, trim, mileage, car_type, cylinder, liter, doors, cruise, sound, leather)
        st.write(f"The predicted price is ${predicted_price:.2f}")
if __name__=="__main__":
    main()
