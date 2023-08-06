from collections import OrderedDict
from typing import List, Sequence

import sympy as smp
from centrex_tlf import couplings
from centrex_tlf.lindblad import generate_density_matrix_symbolic

from .ode_parameters import odeParameters

__all__ = ["system_of_equations_to_lines", "generate_preamble"]


def generate_preamble(
    odepars: odeParameters, transitions: Sequence[couplings.TransitionSelector]
) -> str:
    # check if the symbols in transitions are defined by odepars
    odepars.check_transition_symbols(transitions)
    preamble = """function Lindblad_rhs!(du, ρ, p, t)
    \t@inbounds begin
    """
    for idp, par in enumerate(odepars._parameters):
        preamble += f"\t\t{par} = p[{idp+1}]\n"
    for par in odepars._compound_vars:
        preamble += f"\t\t{par} = {getattr(odepars, par)}\n"

    for transition in transitions:
        preamble += f"\t\t{transition.Ω}ᶜ = conj({transition.Ω})\n"

    # remove duplicate lines (if multiple transitions have the same Rabi rate symbol or
    # detuning
    preamble = "\n".join(list(OrderedDict.fromkeys(preamble.split("\n"))))

    # for a list of lists type inference doesn't work, setting types explicitly
    if "Array" in odepars._parameter_types:
        for transition in transitions:
            preamble = preamble.replace(
                f"{transition.Ω} ", f"{transition.Ω}::ComplexF64 "
            )
        for par_type, par in zip(odepars._parameter_types, odepars._parameters):
            if par_type == "Array":
                par_type = f"Array{{{odepars._array_types.get(par)},1}}"
            preamble = preamble.replace(f"{par} ", f"{par}::{par_type} ")
    return preamble


def system_of_equations_to_lines(
    system: smp.matrices.dense.MutableDenseMatrix,
) -> List[str]:
    n_states = system.shape[0]
    ρ = generate_density_matrix_symbolic(n_states)

    code_lines = []
    # only calculating the upper triangle and diagonal
    for idx in range(n_states):
        for idy in range(idx, n_states):
            if system[idx, idy] != 0:
                cline = str(system[idx, idy])
                cline = f"du[{idx+1},{idy+1}] = " + cline
                cline = cline.replace("(t)", "")
                cline = cline.replace("(t)", "")
                cline = cline.replace("I", "1im")
                cline += "\n"
                for i in range(system.shape[0]):
                    for j in range(system.shape[1]):
                        _ = str(ρ[i, j])
                        cline = cline.replace(_ + "*", f"ρ[{i+1},{j+1}]*")
                        cline = cline.replace(_ + " ", f"ρ[{i+1},{j+1}] ")
                        cline = cline.replace(_ + "\n", f"ρ[{i+1},{j+1}]")
                        cline = cline.replace(_ + ")", f"ρ[{i+1},{j+1}])")
                cline = cline.strip()
                # replace ρ[i,j] with conj(ρ[j,i])
                for i in range(n_states):
                    for j in range(0, i):
                        cline = cline.replace(
                            f"ρ[{i+1},{j+1}]", f"conj(ρ[{j+1},{i+1}])"
                        )

                code_lines.append(cline)
    return code_lines
