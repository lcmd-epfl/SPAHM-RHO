#!/usr/bin/env python3

from qstack import compound
from qstack.spahm.rho import atom, bond

charge = +1
spin = 1
xyz = 'mol/C2H5OH.xyz'
guess = 'LB'

mol = compound.xyz_to_mol(xyz, 'minao', charge=charge, spin=spin)

spahm_a = atom.get_repr(mol, ['H', 'C', 'N', 'O', 'S'], charge, spin,
                        open_mod=['alpha', 'beta'],
                        guess=guess, model='lowdin-long-x', auxbasis='ccpvdzjkfit')
print(spahm_a)

spahm_b = bond.get_repr([mol], [xyz], guess, spin=spin, omods=['alpha', 'beta'], printlevel=2)
print(spahm_b)
