import math
from scipy.interpolate import interp1d


def svFiberAngle(v, coef, *args, **kwargs):
    v = trans(v)
    phi = svFiberAngleR(v, coef)
    return phi









def svFiberAngleR(v, coef, *args, **kwargs):
    """
    v : cylindrical coordinates [theta, r, z]
    theta : circumferential coordinate (radians)
    theta range : [0, pi]
    phi : fiber angle (degrees)
    maxk : maximum curvature (1/in)
    """

    try:
        tol = kwargs['tol']
    except KeyError:
        tol = 1e-6

    theta = v[0]
    # print('theta =', theta)

    intp_theta = coef['theta'] + [210, 240, 270, 300, 330, 360]
    intp_theta = [math.radians(float(_theta)) for _theta in intp_theta]
    intp_phi = coef['phi'] + coef['phi'][::-1][1:]

    # Calculate fiber angle
    for i, th in enumerate(intp_theta):
        if (abs(theta - th) <= tol):
            return intp_phi[i]

    f_phi = interp1d(intp_theta, intp_phi)
    phi = f_phi(theta)
    try:
        m = coef['m']
    except KeyError:
        m = 1.0
    phi = m * phi

    return phi









# --------------------------------------------------------------------

def postProcess(data, sname, *args, **kwargs):
    calcMaxCurvature(data, **kwargs)
    return









def calcMaxCurvature(data, **kwargs):
    """
    theta : circumferential coordinate (radians)
    theta range : [0, pi]
    phi : fiber angle (degrees)
    maxk : maximum curvature (1/in)
    """
    dd = data['main']

    theta = [math.radians(t) for t in kwargs['theta']]
    phi = [
        [dd['_phi10'], dd['_phi11'], dd['_phi12'], dd['_phi13'], dd['_phi14']],
        [dd['_phi30'], dd['_phi31'], dd['_phi32'], dd['_phi33'], dd['_phi34']],
        [dd['_phi50'], dd['_phi51'], dd['_phi52'], dd['_phi53'], dd['_phi54']]
    ]
    for i in range(len(phi)):
        for j in range(len(phi[i])):
            phi[i][j] = math.radians(phi[i][j])
    # intp_cos_phi = [math.cos(math.radians(phi)) for phi in intp_phi]

    # Calculate curvature
    R = data['structure']['parameters']['R']
    ks = []
    for i in range(len(phi)):
        for j in range(len(theta) - 1):
            ks.append(
                math.fabs((math.cos(phi[i][j])-math.cos(phi[i][j+1])) / (R*(theta[j+1]-theta[j])))
            )

    maxk = max(ks)

    data['main']['curv_max'] = maxk

    return {'curv_max': maxk}









def calcSafetyMargin(data, logger, *args, **kwargs):
    srs = data['dakota']['srs']  # Strength ratios
    sr_min = min(srs)
    applied_load = kwargs['applied_load']
    mf = sr_min * applied_load

    # mf = data['dakota']['mf']
    mcr = data['dakota']['mcr']
    sfm = mf - mcr

    return {'safe_m': sfm}









def trans(vin, *args, **kwargs):
    """Convert coordinates from Cartesion to cylindrical

    vin : input Cartesian coordinates [X, Y, Z]
    vout : output cylindrical coordinates [theta, r, z]
    theta : circumferential coordinates (radians)
    """
    theta = math.atan2(vin[1], vin[0])  # radians, (-pi, pi)
    theta = -theta + math.pi / 2
    if theta < 0:
        theta += 2 * math.pi
    r = 12.0
    z = vin[2]

    vout = [theta, r, z]

    return vout

