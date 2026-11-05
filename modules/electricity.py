

import streamlit as st

def electricity_calculator():
    st.title("⚡ Electricity Bill Calculator")
    st.write("Calculate your estimated electricity bill.")

    st.markdown("---")

    units = st.number_input(
        "Electricity consumed (Units)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    rate = st.number_input(
        "Electricity rate (₹ per unit)",
        min_value=0.0,
        value=6.0,
        step=0.5
    )

    if st.button("Calculate Bill", type="primary"):
        total = units * rate

        st.success("Electricity Bill Calculated!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Units", f"{units:g} kWh")

        with col2:
            st.metric("Rate per Unit", f"₹{rate:.2f}")

        st.markdown("### Estimated Electricity Bill")
        st.metric("Total Amount", f"₹{total:,.2f}")

        st.caption(
            "Note: This is an estimated bill. "
            "Actual bills may include fixed charges and taxes."
        )

# Call this function from your Electricity module:
electricity_calculator()
