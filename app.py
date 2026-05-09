import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Real Estate Explorer",
    layout="wide"
)


df = pd.read_csv("cleaned_data_final.csv")

city_bhk_avg = df.groupby(
    ['City', 'BHK']
)['Price_per_SqFt'].median().reset_index()


X = df[['Size_in_SqFt', 'BHK']]
y = df['Price_in_Lakhs']

model = LinearRegression()
model.fit(X, y)

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Home",
        "Investment Analyzer",
        "Analytics Dashboard",
        "Property Comparison",
        "AI Recommendations"
    ]
)
if page == "Home":

    st.title("🏠 Smart Real Estate Explorer")

    st.write("""
    Welcome to the Smart Real Estate Investment Platform 😎

    Features:
    - Investment Analysis
    - 5 Year Future Prediction
    - Analytics Dashboard
    - Property Comparison
    - AI Recommendations
    """)

elif page == "Investment Analyzer":

    st.title("📈 Investment Analyzer")

    size_input = st.number_input(
        "Size (SqFt)",
        min_value=100,
        max_value=5000,
        value=1000
    )

    bhk_input = st.selectbox(
        "BHK",
        sorted(df['BHK'].unique())
    )

    city_input = st.selectbox(
        "City",
        df['City'].unique()
    )

    price_input = st.number_input(
        "Price (Lakhs)",
        min_value=1.0,
        max_value=1000.0,
        value=50.0
    )

    if st.button("🔍 Check Investment"):

        input_pps = (price_input * 100000) / size_input

        filtered = city_bhk_avg[
            (city_bhk_avg['City'] == city_input) &
            (city_bhk_avg['BHK'] == bhk_input)
        ]

        if filtered.empty:

            st.warning("⚠ No market data available.")

        else:

            median_pps = filtered['Price_per_SqFt'].values[0]

            difference = (
                (input_pps - median_pps)
                / median_pps
            ) * 100

            score = max(
                0,
                min(100, 100 - abs(difference))
            )

            st.subheader("📊 Investment Report")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Your Price/SqFt",
                    f"₹ {round(input_pps,2)}"
                )

            with col2:
                st.metric(
                    "Market Avg",
                    f"₹ {round(median_pps,2)}"
                )

            with col3:
                st.metric(
                    "Investment Score",
                    f"{round(score)}/100"
                )

            if difference < -20:

                st.success("✅ Excellent Investment")

            elif difference > 20:

                st.error("❌ Overpriced Property")

            else:

                st.warning("⚖ Fairly Priced")

            # Future Prediction

            growth_rate = 0.08

            future_price_5y = (
                price_input *
                ((1 + growth_rate) ** 5)
            )

            st.subheader("📈 5 Year Prediction")

            st.success(
                f"Estimated Value After 5 Years: ₹ {round(future_price_5y,2)} Lakhs"
            )

            # Top Deals

            st.subheader("🔥 Top Deals")

            top_deals = df.sort_values(
                by='Price_per_SqFt'
            ).head(10)

            st.dataframe(
                top_deals[[
                    'City',
                    'BHK',
                    'Size_in_SqFt',
                    'Price_in_Lakhs',
                    'Price_per_SqFt'
                ]]
            )

elif page == "Analytics Dashboard":

    st.title("📊 Analytics Dashboard")

    total_properties = len(df)

    avg_price = round(
        df['Price_in_Lakhs'].mean(),
        2
    )

    most_expensive_city = (
        df.groupby('City')['Price_in_Lakhs']
        .mean()
        .idxmax()
    )

    cheapest_city = (
        df.groupby('City')['Price_in_Lakhs']
        .mean()
        .idxmin()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🏠 Total Properties",
            total_properties
        )

    with col2:
        st.metric(
            "💰 Avg Price",
            f"₹ {avg_price} L"
        )

    with col3:
        st.metric(
            "📈 Expensive City",
            most_expensive_city
        )

    with col4:
        st.metric(
            "📉 Cheapest City",
            cheapest_city
        )

    # Charts

    city_avg = df.groupby(
        'City'
    )['Price_in_Lakhs'].mean().reset_index()

    fig1 = px.bar(
        city_avg,
        x='City',
        y='Price_in_Lakhs',
        color='City',
        title='Average Property Price by City'
    )

    st.plotly_chart(fig1)

    fig2 = px.scatter(
        df,
        x='Size_in_SqFt',
        y='Price_in_Lakhs',
        color='City',
        title='Property Size vs Price'
    )

    st.plotly_chart(fig2)

elif page == "Property Comparison":

    st.title("🏘 Property Comparison Tool")

    st.subheader("Property 1")

    city1 = st.selectbox(
        "City 1",
        sorted(df['City'].unique()),
        key="city1"
    )

    bhk1 = st.selectbox(
        "BHK 1",
        sorted(df['BHK'].unique()),
        key="bhk1"
    )

    size1 = st.number_input(
        "Size 1",
        value=1000,
        key="size1"
    )

    price1 = st.number_input(
        "Price 1",
        value=50.0,
        key="price1"
    )

    st.divider()

    st.subheader("Property 2")

    city2 = st.selectbox(
        "City 2",
        sorted(df['City'].unique()),
        key="city2"
    )

    bhk2 = st.selectbox(
        "BHK 2",
        sorted(df['BHK'].unique()),
        key="bhk2"
    )

    size2 = st.number_input(
        "Size 2",
        value=1200,
        key="size2"
    )

    price2 = st.number_input(
        "Price 2",
        value=70.0,
        key="price2"
    )

    if st.button("📊 Compare"):

        pps1 = (price1 * 100000) / size1
        pps2 = (price2 * 100000) / size2

        compare_df = pd.DataFrame({

            "Feature": [
                "City",
                "BHK",
                "Size",
                "Price",
                "Price/SqFt"
            ],

            "Property 1": [
                city1,
                bhk1,
                size1,
                price1,
                round(pps1,2)
            ],

            "Property 2": [
                city2,
                bhk2,
                size2,
                price2,
                round(pps2,2)
            ]
        })

        st.dataframe(compare_df)

        if pps1 < pps2:

            st.success(
                "✅ Property 1 offers better value."
            )

        elif pps2 < pps1:

            st.success(
                "✅ Property 2 offers better value."
            )

        else:

            st.warning(
                "⚖ Both properties are similar."
            )

elif page == "AI Recommendations":

    st.title("🤖 AI Recommendations")

    budget = st.number_input(
        "Budget (Lakhs)",
        value=50.0
    )

    preferred_bhk = st.selectbox(
        "Preferred BHK",
        sorted(df['BHK'].unique())
    )

    filtered_df = df[
        (df['Price_in_Lakhs'] <= budget) &
        (df['BHK'] == preferred_bhk)
    ]

    if filtered_df.empty:

        st.warning(
            "⚠ No matching properties found."
        )

    else:

        best_props = filtered_df.sort_values(
            by='Price_per_SqFt'
        ).head(5)

        st.subheader("🏆 Recommended Properties")

        st.dataframe(
            best_props[[
                'City',
                'BHK',
                'Size_in_SqFt',
                'Price_in_Lakhs',
                'Price_per_SqFt'
            ]]
        )

        best_city = (
            best_props['City']
            .value_counts()
            .idxmax()
        )

        st.success(
            f"📍 Best Investment City: {best_city}"
        )