import streamlit as st
import plotly.graph_objects as go
import MinorProjectModule as mpm

st.header("Built-Up Box Section Compression Capacity")

st.sidebar.subheader("Section Geometry")

base_o= st.sidebar.number_input("Base of box section (in)", min_value=0.0, format="%.3f", value=6.00)
depth_o= st.sidebar.number_input("Depth of box section (in)", min_value=0.0, format="%.3f", value=6.00)
t_wall= st.sidebar.number_input("Wall thickness (in)", min_value=0.0, format="%.3f", value=0.500)
L= st.sidebar.number_input("Clear height (m)", min_value=0.0, format="%.3f", value=3.00)
k_x=st.sidebar.number_input("Effective lenght factor about x-axis", min_value=0.0, value= 1.00)
k_y=st.sidebar.number_input("Effective lenght factor about y-axis", min_value=0.0, value= 1.00)
material= st.sidebar.selectbox("Material", ("ASTM A36", "ASTM A572_Gr50", "ASTM A500_GrB_46"))
E= st.sidebar.number_input("Elastic Modulus (ksi)", min_value= 1.00, value= 29000.00)
phi=st.sidebar.number_input("Reduction resistance factor for compression", min_value=0.00, value= 0.90)

fy= mpm.material_fy(material)
a_bub=mpm.calc_area_section_bub(base_o, depth_o, t_wall)
rx_bub=mpm.calc_r_x(base_o, depth_o, t_wall,a_bub)
ry_bub=mpm.calc_r_y(base_o, depth_o, t_wall,a_bub)
lcr_x=mpm.calc_lcr_x(k_x, L, rx_bub)
lcr_y=mpm.calc_lcr_y(k_y, L, ry_bub)
fe_x=mpm.calc_fe_x(lcr_x,E)
fe_y=mpm.calc_fe_y(lcr_y,E)
fn_x=mpm.calc_nominal_fn_x(lcr_x, E, fy, fe_x)
fn_y=mpm.calc_nominal_fn_y(lcr_y, E, fy, fe_y)
pn_x=mpm.calc_cx_capacity(fn_x, a_bub, phi)
pn_y=mpm.calc_cy_capacity(fn_y, a_bub, phi)

outer_x = [0, base_o, base_o, 0, 0]
outer_y = [0, 0, depth_o, depth_o, 0]
inner_x = [t_wall, base_o - t_wall, base_o - t_wall, t_wall, t_wall]
inner_y = [t_wall, t_wall, depth_o - t_wall, depth_o - t_wall, t_wall]
    
fig = go.Figure()

fig.add_trace(go.Scatter(x=outer_x, y=outer_y, fill='toself', fillcolor='lightgray', mode='lines', line=dict(color='black', width=2), name='Exterior'))
fig.add_trace(go.Scatter(x=inner_x, y=inner_y, fill='toself', fillcolor='white', mode='lines', line=dict(color='black', width=2), name='Interior'))

fig.update_layout(
    title="Built Up Box Section Geometry",
    xaxis_title="Base (x-axis)",
    yaxis_title="Depth (y-axis)",
    showlegend=False,
    width=600,
    height=600,
    xaxis=dict(scaleanchor="y", scaleratio=1), 
)

st.plotly_chart(fig)

slender_section = mpm.calc_wall_element_slenderness(base_o,depth_o,t_wall,E,fy)


pn_resistance_x = mpm.calc_compression_resistance_x_axis(base_o, depth_o, t_wall, L, k_x, k_y, material, E, phi)
pn_resistance_y = mpm.calc_compression_resistance_y_axis(base_o, depth_o, t_wall, L, k_x, k_y, material, E, phi)

if slender_section == "Section without slender walls. Compression capacity available with this app":
    st.write(slender_section)
    container1 = st.container(border=True)
    container1.write("Governing compression resistance")
    container1.write( f"{min(pn_resistance_x, pn_resistance_y):.2f} kips")

    container2 = st.container(border=True)
    container2.write("Compression resistance, buckling about x-axis")
    container2.write( f"{(pn_resistance_x):.2f} kips")

    container3 = st.container(border=True)
    container3.write("Compression resistance, buckling about y-axis")
    container3.write( f"{(pn_resistance_y):.2f} kips")

    st.subheader("Step by step calculations")

    with st.expander("Section Area"):
        area_latex, area = mpm.calc_l_area_section_bub(base_o, depth_o, t_wall )
        st.latex(area_latex)

    with st.expander("Radius of gyration about x-axis"):
        rx_latex, rx = mpm.calc_l_r_x(base_o, depth_o, t_wall, a_bub)
        st.latex(rx_latex)

    with st.expander("Radius of gyration about y-axis"):
        ry_latex, ry = mpm.calc_l_r_y(base_o, depth_o, t_wall, a_bub)
        st.latex(ry_latex)

    with st.expander("Effective length about x-axis"):
        lcrx_latex, lcrx = mpm.calc_l_lcr_x(k_x, L, rx_bub)
        st.latex(lcrx_latex)

    with st.expander("Effective length about y-axis"):
        lcry_latex, lcry = mpm.calc_l_lcr_y(k_y, L, ry_bub)
        st.latex(lcry_latex)

    with st.expander("Elastic buckling stress about x-axis"):
        fex_latex, fex = mpm.calc_l_fe_x(lcr_x,E)
        st.latex(fex_latex)

    with st.expander("Elastic buckling stress about y-axis"):
        fey_latex, fey = mpm.calc_l_fe_y(lcr_y,E)
        st.latex(fey_latex)

    with st.expander("Nominal stress about x-axis"):
        fnx_latex, fnx = mpm.calc_l_nominal_fn_x(lcr_x, E, fy, fe_x)
        st.latex(fnx_latex)

    with st.expander("Nominal stress about y-axis"):
        fny_latex, fny = mpm.calc_l_nominal_fn_y(lcr_y, E, fy, fe_y)
        st.latex(fny_latex)

    with st.expander("Compression capacity about x-axis"):
        pnx_latex, pnx = mpm.calc_l_cx_capacity(fn_x, a_bub, phi)
        st.latex(pnx_latex)

    with st.expander("Compression capacity about y-axis"):
        pny_latex, pny = mpm.calc_l_cy_capacity(fn_y, a_bub, phi)
        st.latex(pny_latex)

else:
    st.write(slender_section)













