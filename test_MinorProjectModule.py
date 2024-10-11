import MinorProjectModule as mpm
from math import pi, sqrt, isclose

def test_material_fy ():
    mat01= "ASTM A36"
    mat02= "ASTM A572_Gr50"
    mat03= "ASTM A500_GrB_46"
    assert mpm.material_fy(mat01) == 36
    assert mpm.material_fy(mat02) == 50
    assert mpm.material_fy(mat03) == 46


def test_calc_wall_element_slenderness():
    b1=4
    d1=10
    t1=0.50
    t2=0.125
    E=29000
    fy=36

    assert mpm.calc_wall_element_slenderness(b1,d1,t1,E,fy) == "Section without slender walls. Compression capacity available with this app"
    assert mpm.calc_wall_element_slenderness(b1,d1,t2,E,fy) == "Section with slender walls. Compression capacity NOT available with this app"
    

def test_calc_area_section_bub():
    b1=4
    d1=10
    t1=0.50

    isclose(mpm.calc_area_section_bub(b1,d1,t1), 13.0)


def test_calc_r_x():
    b1=4
    d1=10
    t1=0.50
    a=13

    isclose(mpm.calc_r_x(b1,d1,t1,a),3.4090753690399502)


def test_calc_r_y():
    b1=4
    d1=10
    t1=0.50
    a=13

    isclose(mpm.calc_r_y(b1,d1,t1,a),1.5952654308521184)


def test_calc_lcr_x():
    k1=1
    L=3
    rx=3.4091

    isclose(mpm.calc_lcr_x(k1,L,rx), 34.64582722139527)


def test_calc_lcr_y():
    k1=1
    L=3
    ry=1.5953

    isclose(mpm.calc_lcr_x(k1,L,ry), 74.03798385913956)


def test_calc_fe_x():
    lcr_x=34.6458
    E=29000

    isclose(mpm.calc_fe_x(lcr_x,E),238.44920171293725)


def test_calc_fe_y():
    lcr_y=74.0380
    E=29000

    isclose(mpm.calc_fe_x(lcr_y,E),52.214193645910676)


def test_nominal_fn_x():
    lcr_x=34.6458
    E=29000
    fy=36
    fe_x=238.4492

    isclose(mpm.calc_nominal_fn_x(lcr_x,E,fy,fe_x), 33.795513886206905)


def test_nominal_fn_y():
    lcr_y=74.0380
    E=29000
    fy=36
    fe_y=52.2142

    isclose(mpm.calc_nominal_fn_y(lcr_y,E,fy,fe_y), 26.97584923443642)


def test_calc_cx_capacity():
    fn_x=33.7955
    a=13
    phi=0.90

    isclose(mpm.calc_cx_capacity(fn_x,a,phi), 395.4075124686208)


def test_calc_cy_capacity():
    fn_y=26.9758
    a=13
    phi=0.90

    isclose(mpm.calc_cy_capacity(fn_y,a,phi), 315.61743604290615)


def test_calc_compression_resistance_x_axis():
    b=4
    d=10
    t=0.50
    L=3
    kx=1
    ky=1
    material= "ASTM A36"
    E= 29000
    phi=0.90

    isclose(mpm.calc_compression_resistance_x_axis(b,d,t,L,kx,ky,material,E,phi), 395.4075124686208)


def test_calc_compression_resistance_x_axis():
    b=4
    d=10
    t=0.50
    L=3
    kx=1
    ky=1
    material= "ASTM A36"
    E= 29000
    phi=0.90

    isclose(mpm.calc_compression_resistance_x_axis(b,d,t,L,kx,ky,material,E,phi),395.4075124686208)


def test_calc_compression_resistance_y_axis():
    b=4
    d=10
    t=0.50
    L=3
    kx=1
    ky=1
    material= "ASTM A36"
    E= 29000
    phi=0.90

    isclose(mpm.calc_compression_resistance_y_axis(b,d,t,L,kx,ky,material,E,phi),315.61743604290615)