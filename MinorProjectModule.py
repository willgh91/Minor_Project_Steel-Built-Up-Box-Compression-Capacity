from handcalcs.decorator import handcalc
from math import pi, sqrt


def material_fy (material: str) -> float: 
    if material == "ASTM A36":
        return 36
    elif material == "ASTM A572_Gr50":
        return 50
    elif material == "ASTM A500_GrB_46":
        return 46
    else :
        return "Material not defined"
    

def calc_wall_element_slenderness (b:float, d:float, t:float, E:float, fy:float) -> str:
    """
    Calculates if any of the walls of a built up box section is categorize as slendern or not. 
    b: base of the box section 
    d: depth of the box section 
    t: wall thickness of box section
    E: elastic section modulus
    fy: material nominal yield resistance
    """
    b_1= b - (2*t)
    d_1= d - (2*t)

    upper_limit= 1.49*(sqrt(E/fy))

    is_base_slender = b_1/t > upper_limit
    is_depth_slender = d_1/t > upper_limit 

    if is_base_slender or is_depth_slender:
        return "Section with slender walls. Compression capacity NOT available with this app"

    else: 
        return "Section without slender walls. Compression capacity available with this app"
    

def calc_area_section_bub (b: float, d: float, t:float) -> float:
    """
    Calculates the section area of a built-up box section. 
    b: base of the box section 
    d: depth of the box section 
    t: wall thickness of box section
    """

    b_1= b - (2*t)
    d_1= d - (2*t)

    a_bub = (b*d)-(d_1*b_1)

    return a_bub


def calc_r_x(b:float, d:float, t:float, a=float) -> float:
    """
    Calculates the radious of gyration about "X" axis. 
    b: base of the box section 
    d: depth of the box section 
    t: wall thickness of box section
    a: section area of box section
    """

    b_1= b - (2*t)
    d_1= d - (2*t)

    rx_bub = sqrt(((b*d**3)-(b_1*d_1**3))/(12*a))

    return rx_bub


def calc_r_y(b:float, d:float, t:float, a=float) -> float:
    """
    Calculates the radious of gyration about "Y" axis. 
    b: base of the box section 
    d: depth of the box section 
    t: wall thickness of box section
    a: section area of box section
    """

    b_1= b - (2*t)
    d_1= d - (2*t)

    ry_bub = sqrt(((d*b**3)-(d_1*b_1**3))/(12*a))

    return ry_bub


def calc_lcr_x(k_x:float, L: float, rx:float) -> float:
    """
    Calculates the effective length of member abour x-axis.
    k_x : effective lenght factor about x-axis
    L: clear effective height of member (m)
    rx: raius of gyration about x-axis
    """
    L_in= L/0.0254

    lcr_x= (k_x*L_in)/(rx)

    return lcr_x


def calc_lcr_y(k_y:float, L: float, ry:float) -> float:
    """
    Calculates the effective length of member abour y-axis.
    k_y : effective lenght factor about y-axis
    L: clear effective height of member (m)
    ry: raius of gyration about x-axis
    """
    L_in= L/0.0254

    lcr_y= (k_y*L_in)/(ry)

    return lcr_y


def calc_fe_x ( lcr_x:float, E: float) -> float:
    """
    Calculates the elastic buckling stress about x-axis.
    lcr_x: effective length of member about x-axis. 
    E: modulus of elasticity of steel (ksi)
    """
    fe_x = (pi**2 * E) / (lcr_x**2)

    return fe_x


def calc_fe_y ( lcr_y:float, E: float) -> float:
    """
    Calculates the elastic buckling stress about y-axis.
    lcr_y: effective length of member about y-axis. 
    E: modulus of elasticity of steel (ksi)
    """
    fe_y = (pi**2 * E) / (lcr_y**2)

    return fe_y


def calc_nominal_fn_x(lcr_x:float, E:float, fy:float, fe_x:float) -> float: 
    """
    Calculates the nominal stress about x-axis
    """
    fn_limit = 4.71 * (sqrt(E/fy))

    if lcr_x <= 25:
        fn_x = fy 
    elif lcr_x <= fn_limit: 
        fn_x = fy * (0.658 ** (fy/fe_x))
    elif lcr_x > fn_limit: 
        fn_x = 0.877 * fe_x

    return fn_x


def calc_nominal_fn_y(lcr_y:float, E:float, fy:float, fe_y:float) -> float: 
    """
    Calculates the nominal stress about y-axis
    """
    fn_limit = 4.71 * (sqrt(E/fy))

    if lcr_y <= 25:
        fn_y = fy 
    elif lcr_y <= fn_limit: 
        fn_y = fy * (0.658 ** (fy/fe_y))
    elif lcr_y > fn_limit: 
        fn_y = 0.877 * fe_y

    return fn_y


def calc_cx_capacity (fn_x:float, A: float, phi: float) -> float: 
    """
    Calculates the axial compression capacity about x-axis
    """

    pn_x = fn_x * A * phi

    return pn_x


def calc_cy_capacity (fn_y:float, A: float, phi: float) -> float: 
    """
    Calculates the axial compression capacity about y-axis
    """

    pn_y = fn_y * A * phi

    return pn_y


def calc_compression_resistance_x_axis (b:float, d: float, t:float, L: float, kx:float, ky:float, material: str, E: float, phi:float) -> float: 
    """
    Calculates the compression resistance about x_axis
    """

    fy = material_fy(material)
    a_bub= calc_area_section_bub(b, d, t)
    rx_bub = calc_r_x(b,d,t,a_bub)
    lcr_x= calc_lcr_x(kx, L, rx_bub)
    fe_x= calc_fe_x(lcr_x, E)
    fn_x = calc_nominal_fn_x (lcr_x, E, fy, fe_x) 
    pn_x = calc_cx_capacity (fn_x, a_bub, phi) 

    return pn_x


def calc_compression_resistance_y_axis (b:float, d: float, t:float, L: float, kx:float, ky:float, material: str, E: float, phi:float) -> float: 
    """
    Calculates the compression resistance about x_axis
    """

    fy = material_fy(material)
    a_bub= calc_area_section_bub(b, d, t)
    ry_bub= calc_r_y(b,d,t,a_bub)
    lcr_y= calc_lcr_y(ky, L, ry_bub)
    fe_y = calc_fe_y(lcr_y, E) 
    fn_y = calc_nominal_fn_y (lcr_y, E, fy, fe_y) 
    pn_y = calc_cy_capacity (fn_y, a_bub, phi) 

    return pn_y


hc_renderer = handcalc(override="long")
calc_l_area_section_bub = hc_renderer(calc_area_section_bub)
calc_l_r_x= hc_renderer(calc_r_x)
calc_l_r_y= hc_renderer(calc_r_y)
calc_l_lcr_x= hc_renderer(calc_lcr_x)
calc_l_lcr_y= hc_renderer(calc_lcr_y)
calc_l_fe_x= hc_renderer(calc_fe_x)
calc_l_fe_y= hc_renderer(calc_fe_y)
calc_l_nominal_fn_x= hc_renderer(calc_nominal_fn_x)
calc_l_nominal_fn_y= hc_renderer(calc_nominal_fn_y)
calc_l_cx_capacity= hc_renderer(calc_cx_capacity)
calc_l_cy_capacity= hc_renderer(calc_cy_capacity)