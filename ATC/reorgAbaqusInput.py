import numpy as np
import os


def reorgAbaqusInput(
    nsg, macro_model,
    nodes, elements2d, elements3d, elsets,
    sections, distributions, orientations,
    materials, densities, elastics, w
):

    material_type = {
        'ISOTROPIC': 0,
        'ENGINEERINGCONSTANTS': 1,
        'ORTHOTROPIC': 2,
        'ANISOTROPIC': 2
    }

    # ----- Nodal coordinates ----------------------------------------
    print '  Nodes.'
    # nid = nodes[:, 0]
    # if nsg == 1:
    #     n_coord = nodes[:, [3,]]
    # elif nsg == 2:
    #     n_coord = nodes[:, [2, 3]]
    # elif nsg == 3:
    #     n_coord = nodes[:, [1, 2, 3]]
    n_coord = nodes
    # print n_coord[0]

    if nsg == 0:
        nmax = np.amax(n_coord, axis=0)
        nmin = np.amin(n_coord, axis=0)
        # print nmax[1:4]
        # print nmin[1:4]
        dy = nmax - nmin
        dy1 = dy[1]
        dy2 = dy[2]
        dy3 = dy[3]
        # print dy1, dy2, dy3
        if dy1 * dy2 * dy3 != 0.0:
            nsg = 3
            if w == 0.0 and macro_model == 3:
                w = dy1 * dy2 * dy3
        elif (dy1 * dy2 != 0.0) or (dy2 * dy3 != 0.0) or (dy3 * dy1 != 0.0):
            nsg = 2
            if w == 0.0 and macro_model == 3:
                w = dy1 * dy2 + dy2 * dy3 + dy3 * dy1
            elif macro_model == 1:
                w = 1.0
        elif (dy1 != 0.0) or (dy2 != 0.0) or (dy3 != 0.0):
            nsg = 1
            if w == 0.0 and macro_model == 3:
                w = dy1 + dy2 + dy3
            elif macro_model == 2:
                w = 1.0

    # print nsg
    # print w

    # ----- Materials ------------------------------------------------
    print '  Materials.'
    mtr_id = 0
    mtr = {}
    mtr_name2id = {}
    nmate = len(materials)
    # print densities
    for i in range(nmate):
        mtr_name = materials[i].parameter['name']
        mtr_id += 1
        mtr_name2id[mtr_name] = mtr_id
        # print elastics[i].parameter.keys()
        mtr_type = 'ISOTROPIC'
        if 'type' in elastics[i].parameter.keys():
            mtr_type = elastics[i].parameter['type']
        # try:
        #     mtr_type = elastics[i].parameter['type']
        # except KeyError:
        #     mtr_type = 'ISOTROPIC'
        mtr_type = material_type[mtr_type]
        mtr[mtr_id] = {'isotropy': mtr_type, 'ntemp': 1, 'elastic': []}
        rho = 0.0
        if densities[i]:
            rho = densities[i].data[0][0]
        # print densities[i]
        # els = np.array(elastics[i].data).ravel()
        els = []
        for j in elastics[i].data:
            for k in j:
                if k is not None:
                    els.append(k)
        # print els
        if mtr_type == 0:
            elastic = els
        elif mtr_type == 1:
            elastic = [
                els[0], els[1], els[2],
                els[6], els[7], els[8],
                els[3], els[4], els[5]
            ]
        elif mtr_type == 2:
            if len(els) == 9:
                elastic = [
                    els[0], els[1], els[3],    0.0,    0.0,    0.0,
                    els[2], els[4],    0.0,    0.0,    0.0,
                    els[5],    0.0,    0.0,    0.0,
                    els[8],    0.0,    0.0,
                    els[7],    0.0,
                    els[6]
                ]
            elif len(els) == 21:
                elastic = [
                    els[0], els[1], els[3], els[15], els[10], els[6],
                    els[2], els[4], els[16], els[11], els[7],
                    els[5], els[17], els[12], els[8],
                    els[20], els[19], els[18],
                    els[14], els[13],
                    els[9]
                ]
        elastic = np.hstack(([20.0, rho], elastic))
        # print elastic
        mtr[mtr_id]['elastic'].append(elastic)

    # ----- Layer types ----------------------------------------------
    print '  Layer types.'
    lid = 0
    lyt = []
    lyt_name2id = {}
    used_lyt = []
    used_elset = []
    # print sections
    for s in sections:
        lname = s.parameter['elset']
        # used_elset.append(lname)
        mname = s.parameter['material']
        mid = mtr_name2id[mname]
        mname_angle = lname.split('/')[0]
        if nsg == 3:
            mname_angle = mname_angle + '_0'
        if mname_angle not in used_lyt:
            lid += 1
            lyt_name2id[mname_angle] = lid
            i = mname_angle.rfind('_')
            angle = mname_angle[i + 1:]
            if 'p' in angle:
                angle = angle[1:]
            elif 'n' in angle:
                angle = angle.replace('n', '-')
            angle = float(angle.replace('D', '.'))
            lyt.append([lid, mid, angle])
        used_lyt.append(mname_angle)
        used_elset.append([lname, lyt_name2id[mname_angle]])

    # ----- Element connectivities -----------------------------------
    print '  Elements.'
    eid_lid = {}
    for elset_lid in used_elset:
        es = elsets[elset_lid[0]]
        lid = elset_lid[1]
        for e in es:
            eid_lid[e] = lid

    e_connt_2d3 = elements2d[3]
    e_connt_2d4 = elements2d[4]
    e_connt_2d6 = elements2d[6]
    e_connt_2d8 = elements2d[8]

    e_connt_3d4 = elements3d[4]
    e_connt_3d8 = elements3d[8]
    e_connt_3d10 = elements3d[10]
    e_connt_3d20 = elements3d[20]

    e2d = []
    if len(e_connt_2d3) > 1:
        e_connt_2d3 = e_connt_2d3[1:]
        z = np.zeros((len(e_connt_2d3), 6))
        e_connt_2d3 = np.hstack([e_connt_2d3, z])
        e2d.append(e_connt_2d3)
    if len(e_connt_2d4) > 1:
        e_connt_2d4 = e_connt_2d4[1:]
        z = np.zeros((len(e_connt_2d4), 5))
        e_connt_2d4 = np.hstack([e_connt_2d4, z])
        e2d.append(e_connt_2d4)
    if len(e_connt_2d6) > 1:
        e_connt_2d6 = e_connt_2d6[1:]
        z = np.zeros((len(e_connt_2d6), 2))
        e_connt_2d6 = np.hstack([e_connt_2d6, z])
        e_connt_2d6 = np.insert(e_connt_2d6, 4, 0, axis=1)
        e2d.append(e_connt_2d6)
    if len(e_connt_2d8) > 1:
        e_connt_2d8 = e_connt_2d8[1:]
        z = np.zeros((len(e_connt_2d8), 1))
        e_connt_2d8 = np.hstack([e_connt_2d8, z])
        e2d.append(e_connt_2d8)
    if len(e2d) > 0:
        elements2d = np.vstack(e2d)
        elements2d = elements2d.astype(int)
    else:
        elements2d = []

    e3d = []
    if len(e_connt_3d4) > 1:
        e_connt_3d4 = e_connt_3d4[1:]
        z = np.zeros((len(e_connt_3d4), 16))
        e_connt_3d4 = np.hstack([e_connt_3d4, z])
        e3d.append(e_connt_3d4)
    if len(e_connt_3d8) > 1:
        e_connt_3d8 = e_connt_3d8[1:]
        z = np.zeros((len(e_connt_3d8), 12))
        e_connt_3d8 = np.hstack([e_connt_3d8, z])
        e3d.append(e_connt_3d8)
    if len(e_connt_3d10) > 1:
        e_connt_3d10 = e_connt_3d10[1:]
        z = np.zeros((len(e_connt_3d10), 9))
        e_connt_3d10 = np.hstack([e_connt_3d10, z])
        e_connt_3d10 = np.insert(e_connt_3d10, 5, 0, axis=1)
        e3d.append(e_connt_3d10)
    if len(e_connt_3d20) > 1:
        e3d.append(e_connt_3d20)
    if len(e3d) > 0:
        elements3d = np.vstack(e3d)
        elements3d = elements3d.astype(int)
    else:
        elements3d = []
    nelem = len(elements2d) + len(elements3d)
    # print nelem

    # ----- Local coordinates ----------------------------------------
    print '  Local coordinates.'
    eid_all = np.arange(1, nelem + 1).tolist()
    distr_all = []
    if len(distributions) > 0:
        # Join all distributions
        distr_all = np.zeros((1, 7))
        for distr in distributions:
            distr_all = np.vstack([distr_all, distr.data[1:]])
        distr_all = distr_all[1:]
        # print distr_all
        # Extract element ids
        eids = distr_all[:, 0]
        # print eids
        # Find indices of unique ids
        eids_uni, eids_uni_i = np.unique(eids, return_index=True)
        distr_uni = distr_all[eids_uni_i, :]
        if nsg == 2:
            distr_uni = distr_uni[:, :4]
            distr_uni = np.insert(distr_uni, 1, 1, axis=1)
            distr_uni = np.insert(distr_uni, 2, 0, axis=1)
            distr_uni = np.insert(distr_uni, 3, 0, axis=1)
        c_zeros = np.zeros((len(distr_uni), 3))
        distr_all = np.hstack([distr_uni, c_zeros])

    print '  Finished.'

    return {
        # 'node ids': nid,
        'nsg': nsg,
        'nodes': n_coord,
        'all elements ids': eid_all,
        'element to layer type': eid_lid,
        'elements 2d': elements2d,
        'elements 3d': elements3d,
        'distributions': distr_all,
        'layer types': lyt,
        'materials': mtr,
        'w': w
    }
