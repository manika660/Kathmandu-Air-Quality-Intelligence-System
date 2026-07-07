import streamlit as st
import pandas as pd
import joblib

from users import login


# ==========================
# LOAD MODEL AND SCALER
# ==========================

model = joblib.load("air_quality_model.pkl")

scaler = joblib.load("scaler.pkl")


# ==========================
# SESSION LOGIN
# ==========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False



# ==========================
# LOGIN PAGE
# ==========================

if not st.session_state.logged_in:

    st.title("🌫 Kathmandu Air Quality Intelligence System")

    st.subheader("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        if login(username, password):

            st.session_state.logged_in = True

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid username or password")



# ==========================
# DASHBOARD
# ==========================

else:

    st.title(" Kathmandu Air Quality Dashboard")


    st.write(
        "Predict PM2.5 concentration using Random Forest Machine Learning Model"
    )


    st.subheader(" Enter Air Quality Parameters")


    col1, col2 = st.columns(2)



    # -------- COLUMN 1 --------

    with col1:


        pm10 = st.number_input(
            "PM10",
            value=80.0
        )


        carbon_monoxide = st.number_input(
            "Carbon Monoxide",
            value=2.5
        )


        nitrogen_dioxide = st.number_input(
            "Nitrogen Dioxide",
            value=40.0
        )


        sulphur_dioxide = st.number_input(
            "Sulphur Dioxide",
            value=10.0
        )


        ozone = st.number_input(
            "Ozone",
            value=30.0
        )


        temperature_2m = st.number_input(
            "Temperature (°C)",
            value=25.0
        )


        relative_humidity_2m = st.number_input(
            "Humidity (%)",
            value=60.0
        )



    # -------- COLUMN 2 --------

    with col2:


        wind_speed_10m = st.number_input(
            "Wind Speed",
            value=5.0
        )


        wind_direction_10m = st.number_input(
            "Wind Direction",
            value=180.0
        )


        surface_pressure = st.number_input(
            "Surface Pressure",
            value=1010.0
        )


        month = st.number_input(
            "Month",
            min_value=1,
            max_value=12,
            value=7
        )


        day = st.number_input(
            "Day",
            min_value=1,
            max_value=31,
            value=7
        )


        hour = st.number_input(
            "Hour",
            min_value=0,
            max_value=23,
            value=12
        )


        day_of_week = st.number_input(
            "Day of Week",
            min_value=0,
            max_value=6,
            value=1
        )



    # ==========================
    # PREDICTION BUTTON
    # ==========================


    if st.button("🌫 Predict PM2.5"):


        input_data = pd.DataFrame({

            "pm10":[pm10],

            "carbon_monoxide":[carbon_monoxide],

            "nitrogen_dioxide":[nitrogen_dioxide],

            "sulphur_dioxide":[sulphur_dioxide],

            "ozone":[ozone],

            "temperature_2m":[temperature_2m],

            "relative_humidity_2m":[relative_humidity_2m],

            "wind_speed_10m":[wind_speed_10m],

            "wind_direction_10m":[wind_direction_10m],

            "surface_pressure":[surface_pressure],

            "month":[month],

            "day":[day],

            "hour":[hour],

            "day_of_week":[day_of_week]

        })


        # Scale input

        scaled_input = scaler.transform(
            input_data
        )


        # Predict PM2.5

        prediction = model.predict(
            scaled_input
        )[0]



        st.success(
            f" Predicted PM2.5: {prediction:.2f} µg/m³"
        )



        # ==========================
        # HEALTH ADVICE
        # ==========================


        st.subheader(" Health Advice")



        if prediction <= 12:


            st.success(
                """
                  Good Air Quality

                Advice:
                - Outdoor activities are safe.
                - Air pollution level is low.
                - No special precautions required.
                """
            )


        elif prediction <= 35.4:


            st.info(
                """
                  Moderate Air Quality

                Advice:
                - Air quality is acceptable.
                - Sensitive people should reduce long outdoor exposure.
                - Monitor air quality regularly.
                """
            )


        elif prediction <= 55.4:


            st.warning(
                """
                  Unhealthy for Sensitive Groups

                Advice:
                - Children and elderly people should be careful.
                - Avoid prolonged outdoor activities.
                - Consider wearing a mask outside.
                """
            )


        elif prediction <= 150.4:


            st.warning(
                """
                  Unhealthy Air Quality

                Advice:
                - Avoid heavy outdoor exercise.
                - Wear an N95 mask outside.
                - Keep windows closed during pollution peaks.
                """
            )


        elif prediction <= 250.4:


            st.error(
                """
                  Very Unhealthy Air Quality

                Advice:
                - Stay indoors if possible.
                - Avoid outdoor activities.
                - Use air purification if available.
                """
            )


        else:


            st.error(
                """
                 Hazardous Air Quality

                Advice:
                - Avoid outdoor exposure.
                - Stay indoors.
                - Follow health safety guidelines.
                """
            )