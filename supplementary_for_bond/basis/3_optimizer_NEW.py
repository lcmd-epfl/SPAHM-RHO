#!/usr/bin/env python3

import os
from qstack import basis_opt

#initial = "CF.bas"
#data = ["../xyz2/CF4.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

#initial = "CCl.bas"
#data = ["../xyz2/CCl4.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

#initial = "ClN.bas"
#data = ["../xyz2/NCl3.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

#initial = "ClO.bas"
#data = ["../xyz2/ClO-.xyz.rho_bond.npz", "../xyz2/ClO2-.xyz.rho_bond.npz", "../xyz2/ClO3-.xyz.rho_bond.npz", "../xyz2/ClO4-.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

#initial = "ClH.bas"
#data = ["../xyz2/HCl.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

#initial = "FH.bas"
#data = ["../xyz2/HF.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

#initial = "FO.bas"
#data = ["../xyz2/FOOF.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

#initial = "FN.bas"
#data = ["../xyz2/NF3.xyz.rho_bond.npz"]
#optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")

initial = "../basis_opt/FN.bas"
data = ["ttt/NF3.xyz.rho_bond.npz"]
optimized_basis = basis_opt.opt.optimize_basis(["No"], [initial], data, gtol_in = 1e-7, method_in = "CG")
