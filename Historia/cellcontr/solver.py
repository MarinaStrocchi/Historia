import json

import numpy as np
from scipy.integrate import solve_ivp

from Historia.cellcontr.model import Land2012
from Historia.shared.constants import RESOURCES_PARAMETERS_DIR, posix_path


class CONTRSolution:
    """
    This class implements the solution of the Land et al. (2012) cellular contraction model*.
    *https://physoc.onlinelibrary.wiley.com/doi/full/10.1113/jphysiol.2012.231928
    """

    def __init__(self, rat, Cai, paramsdir=RESOURCES_PARAMETERS_DIR):
        constantspath = posix_path(paramsdir, "cellcontr/parameters.json")
        with open(constantspath, "r") as f:
            dct_p = json.load(f)

        initstatespath = posix_path(paramsdir, "cellcontr/init_states.json")
        with open(initstatespath, "r") as f:
            dct_is = json.load(f)

        self.Cai = Cai
        self.constant = dct_p[rat]
        self.init_state = dct_is

    def solver_sol(self, p_dict=None, i_dict=None):
        if p_dict is not None:
            for key in p_dict.keys():
                self.constant[key] = p_dict[key]

        if i_dict is not None:
            for key in i_dict.keys():
                self.init_state[key] = i_dict[key]

        self.t = np.arange(len(self.Cai))
        tspan = [0, self.t[-1]]

        sizeStates = len(self.init_state.keys())
        Y0 = np.zeros((sizeStates,), dtype=float)
        for i, item in enumerate(self.init_state.items()):
            Y0[i] = item[1]

        Y = solve_ivp(
            lambda t, y: Land2012.computeRates(t, y, self.Cai, self.constant),
            t_span=tspan,
            y0=Y0,
            method="BDF",
            t_eval=self.t,
            max_step=1.0,
        )
        self.Y = Y.y

        constant = Land2012.initConsts(self.constant)
        self.T = np.array(
            [
                Land2012.computeAlgebraics(ti, Yi, self.Cai, constant)[-1]
                for ti, Yi in zip(self.t, self.Y.T)
            ]
        )

    def steadystate_sol(self, p_dict=None):
        if p_dict is not None:
            for key in p_dict.keys():
                self.constant[key] = p_dict[key]

        (
            TRPN_ss,
            trpn_EC50,
            XB_ss,
            xb_EC50,
            F_ss,
            pCa50,
            nH,
            hl,
        ) = Land2012.computeSteadystate(self.Cai, self.constant)
        self.TRPN = {"TRPN": TRPN_ss, "EC50": trpn_EC50}
        self.XB = {"XB": XB_ss, "EC50": xb_EC50}
        self.F = {"F": F_ss, "pCa50": pCa50, "h": nH, "hl": hl}
