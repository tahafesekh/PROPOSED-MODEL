import streamlit as st
import math

# ======= CSS Styles (white background, blue info box, green special box) =======
st.markdown("""
    <style>
        .stApp {
            background-color: white !important;
            color: black !important;
        }
        .stMarkdown, .stTitle, .stHeader, .stSubheader, .stCaption, .stTextInput > label,
        .stNumberInput > label, .stSelectbox > label, .stInfo, .stAlert, .stSuccess, .stError, .stButton > button {
            color: black !important;
        }
        [data-testid="stSidebar"] {
            background-color: white !important;
        }
        .stButton > button {
            color: black !important;
            border: 1px solid #333;
            background: #fff !important;
        }
        .stAlert, .stInfo, .stSuccess, .stError {
            background-color: #e3f2fd !important;
            color: #222 !important;
            border-left: 5px solid #2196f3 !important;
            border-radius: 6px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }
        .stInfo > div, .stAlert > div, .stSuccess > div, .stError > div {
            color: #222 !important;
            background-color: #e3f2fd !important;
        }
        .special-bold-box {
            background-color: #d2ffd2 !important;
            color: #185d18 !important;
            border-left: 5px solid #219653 !important;
            border-radius: 7px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            font-weight: bold !important;
            padding: 0.8em 0.7em !important;
            margin-bottom: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Calculation of the Maximum Deflection Using the Proposed Model")
st.markdown("by Taha A.Fesekh, Ehab M. Lotfy, Erfan Abdel-Latif, Nady M. Abdel-Fattah, and Abdel-Rahman M. Naguib")

section_type = st.selectbox("Section Type", ["T-section", "R-section"])

# =========== Default values based on section type ===========
if section_type == "T-section":
    default_Pa = 121.0
    default_X = 600.0
    default_L = 1800.0
    default_fc = 26.80
    default_Ef = 50000.0
    default_Af = 157.0
    default_rho_f = 0.35
    default_rho_fb = 0.23
    default_d = 225.0
    default_d_prime = 25.0
    default_b = 200.0
    default_y1 = 175.0
    default_B = 500.0
    default_y2 = 75.0
else:
    default_Pa = 107.0
    default_X = 600.0
    default_L = 1800.0
    default_fc = 26.80
    default_Ef = 50000.0
    default_Af = 157.0
    default_rho_f = 0.35
    default_rho_fb = 0.23
    default_d = 225.0
    default_d_prime = 25.0
    default_b = 200.0
    default_t = 250.0

st.subheader("Input Data")

col1, col2, col3, col4 = st.columns(4)
with col1:
    Pa = st.number_input("Applied Load (Pa, kN)", value=default_Pa)
with col2:
    X = st.number_input("flexural-shear span X (mm)", value=default_X)
with col3:
    L = st.number_input("Beam Length L (mm)", value=default_L)
with col4:
    fc = st.number_input("Concrete compressive strength f'c (MPa)", value=default_fc)

col5, col6, col7, col8 = st.columns(4)
with col5:
    Ef = st.number_input("Modulus of elasticity of FRP Ef (MPa)", value=default_Ef)
with col6:
    Af = st.number_input("Area of FRP reinforcement Af (mm2)", value=default_Af)
with col7:
    rho_f = st.number_input("Reinforcement ratio rho_f", value=default_rho_f)
with col8:
    rho_fb = st.number_input("Balanced reinforcement ratio rho_fb", value=default_rho_fb)

col9, col10 = st.columns(2)
with col9:
    d = st.number_input("Effective depth d (mm)", value=default_d)
with col10:
    d_prime = st.number_input("Concrete Cover d' (mm)", value=default_d_prime)

# Section geometry inputs
if section_type == "T-section":
    colT1, colT2, colT3, colT4 = st.columns(4)
    with colT1:
        b = st.number_input("Width of flange b (mm)", value=default_b)
    with colT2:
        y1 = st.number_input("Height of flange y1 (mm)", value=default_y1)
    with colT3:
        B = st.number_input("Width of web B (mm)", value=default_B)
    with colT4:
        y2 = st.number_input("Height of web y2 (mm)", value=default_y2)
    A1 = b * y1
    A2 = B * y2
else:
    colR1, colR2 = st.columns(2)
    with colR1:
        b = st.number_input("Width b (mm)", value=default_b)
    with colR2:
        t = st.number_input("Height t (mm)", value=default_t)
    A1 = b * t
    A2 = 0

# ======= Pre-calculations =======
Ec = 4700 * (fc ** 0.5)
nf = Ef / Ec
beta_d = min(0.05 * (rho_f / rho_fb), 0.50)
Xd_ratio = X / d if d != 0 else 0
if Xd_ratio <= 2.7:
    lambda_e = min(max(0.085 * Xd_ratio + 0.00813 * d_prime + 0.461, 0.75), 0.95)
else:
    lambda_e = min(max(-0.0074 * Xd_ratio + 0.0094 * d_prime + 0.32, 0.55), 0.95)

if section_type == "T-section":
    At = A1 + A2 + (nf - 1) * Af
    yt = (A1 * (y1 / 2) + A2 * (y1 + y2 / 2) + (nf - 1) * Af * d_prime) / At if At != 0 else 0
    Ig = (b * y1 ** 3) / 12 + A1 * (y1 / 2 - yt) ** 2 + (B * y2 ** 3) / 12 + A2 * ((y1 + y2 / 2) - yt) ** 2 + ((nf - 1) * Af) * (yt - d_prime) ** 2
else:
    At = b * t + (nf - 1) * Af
    yt = ((b * t ** 2) / 2 + (nf - 1) * Af * d_prime) / At if At != 0 else 0
    Ig = (b * t ** 3) / 12 + b * t * (t / 2 - yt) ** 2 + ((nf - 1) * Af) * (yt - d_prime) ** 2

Ma = (Pa * 1000) / 2 * X  # (N*mm)
fr = 0.62 * math.sqrt(fc)  # MPa
Mcr = fr * Ig / yt if yt != 0 else 0  # (N*mm)

if section_type == "T-section":
    a = B / 2
    b_quad = nf * Af
    c = - (nf * Af) * d
    delta = b_quad**2 - 4*a*c
    if delta < 0 or a == 0:
        Z = 0
    else:
        Z = (-b_quad + math.sqrt(delta)) / (2*a)
    Icr = B * Z ** 3 / 3 + (nf * Af) * (d - Z) ** 2
else:
    a = b / 2
    b_quad = nf * Af
    c = - (nf * Af) * d
    delta = b_quad**2 - 4*a*c
    if delta < 0 or a == 0:
        Z = 0
    else:
        Z = (-b_quad + math.sqrt(delta)) / (2*a)
    Icr = b * Z ** 3 / 3 + (nf * Af) * (d - Z) ** 2

# ========= معادلة Ie مع شرط Ma =========
if Ma < Mcr:
    Ie = Ig
else:
    ratio = (Mcr / Ma) ** 3 if Ma > 0 else 0
    Ie = beta_d * ratio * Ig + lambda_e * (1 - ratio) * Icr
    Ie = min(Ie, Ig)

if Ec != 0 and Ie != 0:
    delta_max = (Pa * 1000 * X) / (48 * Ec * Ie) * (3 * L ** 2 - 4 * X ** 2)
else:
    delta_max = 0

# ========= Main Results Button =========
if st.button("Calculate"):
    results = []
    if section_type == "T-section":
        results.append(f"Area of web A1 = {A1:.2f} mm²")
        results.append(f"Area of flange A2 = {A2:.2f} mm²")
    else:
        results.append(f"Area = {A1:.2f} mm²")
    results.append(f"Elastic modulus of concrete Ec = {Ec:.2f} MPa")
    results.append(f"Modular ratio nf (Ef/Ec) = {nf:.3f} (calculated)")
    results.append(f"Reduction coefficient βd = {beta_d:.3f}")
    results.append(f"Reduction factor λe = {lambda_e:.3f}")
    results.append(f"Neutral axis depth y_t = {yt:.3f} mm")
    results.append(f"Equivalent area A_t = {At:.3f} mm²")
    results.append(f"Ig (uncracked moment of inertia) = {Ig:.3f} mm⁴")
    results.append(f"Maximum moment Ma = {Ma:.2f} N·mm")
    results.append(f"Modulus of rupture fr = {fr:.3f} MPa")
    results.append(f"Cracking moment Mcr = {Mcr:.2f} N·mm")
    results.append(f"Compression zone depth Z = {Z:.3f} mm")
    results.append(f"Icr (cracked moment of inertia) = {Icr:.3f} mm⁴")
    idx_Ie = len(results)
    results.append(f"Effective moment of inertia Ie = {Ie:.3f} mm⁴")
    idx_defl = len(results)
    results.append(f"Maximum Deflection δ_max = {delta_max:.5f} mm")

    # ======== Display results horizontally (4 per row) ========
    cols_per_row = 4
    for i in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for idx, col in enumerate(cols):
            res_idx = i + idx
            if res_idx < len(results):
                result = results[res_idx]
                if res_idx == idx_Ie or res_idx == idx_defl:
                    col.markdown(
                        f'<div class="special-bold-box">{result}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    col.info(result)
    st.success("Done")

# ========= LOG BUTTON =========
if st.button("Show step-by-step calculations (Log)"):
    st.subheader("Step-by-step Calculation Log")
    st.write(f"1️⃣ Concrete elastic modulus Ec = 4700 * sqrt({fc}) = {Ec:.2f} MPa")
    st.write(f"2️⃣ Modular ratio nf = Ef / Ec = {Ef} / {Ec:.2f} = {nf:.3f}")

    if section_type == "T-section":
        st.write(f"3️⃣ Flange area A1 = {b} * {y1} = {A1:.2f} mm²")
        st.write(f"4️⃣ Web area A2 = {B} * {y2} = {A2:.2f} mm²")
        st.write(f"5️⃣ Equivalent area At = {A1:.2f} + {A2:.2f} + ({nf:.3f} - 1) * {Af} = {At:.2f} mm²")
        st.write(f"6️⃣ Neutral axis yt =  {yt:.2f} mm")
        st.write(f"7️⃣ Gross moment of inertia Ig =  {Ig:.2f} mm⁴")
    else:
        st.write(f"3️⃣ Area = {b} * {t} = {A1:.2f} mm²")
        st.write(f"4️⃣ Equivalent area At = {At:.2f} mm²")
        st.write(f"5️⃣ Neutral axis yt =  {yt:.2f} mm")
        st.write(f"6️⃣ Gross moment of inertia Ig =  {Ig:.2f} mm⁴")

    st.write(f"8️⃣ Reduction coefficient βd = min(0.05*({rho_f}/{rho_fb}), 0.50) = {beta_d:.3f}")
    st.write(f"9️⃣ Reduction factor λe = {lambda_e:.3f}")
    st.write(f"🔟 Maximum moment Ma = (Pa*1000)/2 * X = ({Pa}*1000)/2 * {X} = {Ma:.2f} N·mm")
    st.write(f"11️⃣ Modulus of rupture fr = 0.62 * sqrt({fc}) = {fr:.3f} MPa")
    st.write(f"12️⃣ Cracking moment Mcr = fr * Ig / yt = {fr:.3f} * {Ig:.2f} / {yt:.2f} = {Mcr:.2f} N·mm")
    if Ma < Mcr:
        st.write(f"❗️ Ma < Mcr ⇒ Section is uncracked. So: Ie = Ig = {Ig:.2f} mm⁴")
    else:
        st.write(f"13️⃣ Moment ratio = (Mcr/Ma)^3 = ({Mcr:.2f}/{Ma:.2f})^3 = {(Mcr/Ma)**3:.3f}")
        if section_type == "T-section":
            st.write(f"14️⃣ Compression zone Z = {Z:.3f} mm")
            st.write(f"15️⃣ Cracked moment of inertia Icr = {Icr:.2f} mm⁴")
        else:
            st.write(f"14️⃣ Compression zone Z = {Z:.3f} mm")
            st.write(f"15️⃣ Cracked moment of inertia Icr = {Icr:.2f} mm⁴")
        st.write(f"16️⃣ Effective moment of inertia Ie = {Ie:.2f} mm⁴")
    st.write(f"17️⃣ Maximum deflection δ_max = {delta_max:.5f} mm")
    st.success("All step-by-step calculations are shown.")
