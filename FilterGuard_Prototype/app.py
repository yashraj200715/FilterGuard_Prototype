import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="FilterGuard | Prototype", page_icon="💧", layout="wide")

# FilterGuard is a concept prototype. Values are simulated or manually entered,
# not a validated diagnosis of water quality or filter life.

NAVY = "#18304D"
TEAL = "#159A91"
RED = "#E53955"
AMBER = "#D98E16"

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.metric-card {background:#F3F6FA;border:1px solid #DFE6EE;border-radius:14px;padding:14px 16px;}
.small-note {color:#64748B;font-size:0.88rem;}
</style>
""", unsafe_allow_html=True)

st.title("💧 FilterGuard")
st.subheader("Predictive filter-health monitoring for domestic water purifiers")
st.caption("Concept prototype • Rule-based demonstration • Not a water-safety test")

with st.sidebar:
    st.header("Demo controls")
    st.write("Change the readings to see how the alert logic responds.")
    mode = st.radio("Data source", ["Manual inputs", "Simulated trend"], index=0)
    st.divider()
    st.subheader("Current sensor readings")
    flow = st.slider("Flow rate (L/min)", 0.2, 3.0, 1.4, 0.1)
    pressure_drop = st.slider("Pressure drop (relative units)", 0.1, 3.0, 1.8, 0.1)
    usage_liters = st.slider("Estimated cumulative usage (L)", 0, 15000, 6500, 250)
    days_since_change = st.slider("Days since filter replacement", 0, 730, 120, 5)
    tds_in = st.slider("Inlet TDS (ppm) — optional context", 0, 1500, 450, 10)
    tds_out = st.slider("Outlet TDS (ppm) — optional context", 0, 1500, 120, 10)
    st.caption("TDS values are contextual only; they cannot establish overall drinking-water safety.")

# Illustrative reference values for demo logic only. Must be calibrated for a real purifier.
baseline_flow = 2.0
baseline_pressure = 1.0
flow_ratio = flow / baseline_flow
pressure_ratio = pressure_drop / baseline_pressure

# Transparent rule-based indicator; not a validated remaining-life prediction.
risk_points = 0
reasons = []
if flow_ratio < 0.65:
    risk_points += 35
    reasons.append("Flow is substantially below the illustrative clean-filter baseline.")
elif flow_ratio < 0.80:
    risk_points += 20
    reasons.append("Flow is moderately below the illustrative clean-filter baseline.")

if pressure_ratio > 2.0:
    risk_points += 35
    reasons.append("Pressure drop is high relative to the illustrative baseline.")
elif pressure_ratio > 1.5:
    risk_points += 20
    reasons.append("Pressure drop is elevated relative to the illustrative baseline.")

if usage_liters > 10000:
    risk_points += 15
    reasons.append("Cumulative usage is high in this demonstration scenario.")
elif usage_liters > 7000:
    risk_points += 8
    reasons.append("Cumulative usage is approaching the demo's configured threshold.")

if days_since_change > 365:
    risk_points += 15
    reasons.append("Time since replacement is long; check the manufacturer's maintenance guidance.")
elif days_since_change > 180:
    risk_points += 8
    reasons.append("Time since replacement is increasing; check the manufacturer's maintenance guidance.")

health_indicator = max(0, 100 - risk_points)
if risk_points >= 55:
    status = "Inspection recommended"
    status_color = RED
elif risk_points >= 25:
    status = "Monitor closely"
    status_color = AMBER
else:
    status = "No rule-based warning"
    status_color = TEAL

if mode == "Simulated trend":
    rng = np.random.default_rng(12)
    days = np.arange(0, 31)
    trend_flow = np.linspace(2.0, flow, len(days)) + rng.normal(0, 0.055, len(days))
    trend_pressure = np.linspace(1.0, pressure_drop, len(days)) + rng.normal(0, 0.045, len(days))
    trend = pd.DataFrame({
        "Day": days,
        "Flow rate (L/min)": np.clip(trend_flow, 0.2, None),
        "Pressure drop (relative units)": np.clip(trend_pressure, 0.1, None)
    })
else:
    days = np.arange(0, 15)
    rng = np.random.default_rng(7)
    trend = pd.DataFrame({
        "Day": days,
        "Flow rate (L/min)": np.clip(flow + rng.normal(0, 0.03, len(days)), 0.2, None),
        "Pressure drop (relative units)": np.clip(pressure_drop + rng.normal(0, 0.03, len(days)), 0.1, None)
    })

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rule-based indicator", f"{health_indicator}/100")
c2.metric("Flow rate", f"{flow:.1f} L/min", f"{(flow_ratio-1)*100:+.0f}% vs demo baseline")
c3.metric("Pressure drop", f"{pressure_drop:.1f}× baseline")
c4.metric("Current status", status)

st.progress(health_indicator / 100, text="Illustrative condition indicator (not a certified filter-life score)")

left, right = st.columns([1.55, 1])
with left:
    st.markdown("### Sensor trend")
    st.line_chart(trend.set_index("Day")[["Flow rate (L/min)", "Pressure drop (relative units)"]])
    st.caption("Trend values are simulated for demonstration. Real trend analysis requires timestamped sensor measurements.")
with right:
    st.markdown("### Why did it flag this?")
    if reasons:
        for reason in reasons:
            st.warning(reason)
    else:
        st.success("No configured rule was triggered by the current readings.")
        st.write("Continue monitoring and follow the purifier manufacturer's maintenance instructions.")
    st.markdown("### Recommended next action")
    if risk_points >= 55:
        st.write("Inspect the system and compare readings with the manufacturer's specifications. Do not assume the filter is unsafe or failed from these readings alone.")
    elif risk_points >= 25:
        st.write("Record readings over time and check for persistent changes before deciding on maintenance.")
    else:
        st.write("Continue routine monitoring and follow the manufacturer's replacement schedule.")

st.markdown("---")
st.markdown("### Prototype scope and limitations")
st.info(
    "This demo uses transparent, illustrative rules and example thresholds. It does not use a trained machine-learning model, "
    "does not predict a verified remaining filter life, and cannot certify water safety. TDS alone cannot detect all contaminants. "
    "Before real deployment, thresholds must be calibrated for the specific purifier and validated against measured filter-performance data."
)

with st.expander("Show current demo data"):
    st.dataframe(pd.DataFrame([{
        "Flow rate (L/min)": flow,
        "Pressure drop (relative units)": pressure_drop,
        "Cumulative usage (L)": usage_liters,
        "Days since replacement": days_since_change,
        "Inlet TDS (ppm)": tds_in,
        "Outlet TDS (ppm)": tds_out,
        "Rule-based indicator": health_indicator,
        "Status": status
    }]), use_container_width=True)

st.caption("FilterGuard • Student hackathon concept • Replace illustrative thresholds with validated measurements before any real-world use.")
