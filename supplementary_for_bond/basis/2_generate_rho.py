#!/usr/bin/env python3

import argparse
import numpy as np
from pyscf import gto,scf,dft
import qstack

def weighting(r, r1, r2):
    # a cosine weighting function
    v1 = r-r1
    dr = r2-r1
    dist = np.linalg.norm(dr)
    z = v1@dr/dist - dist*0.5
    if abs(z) >= dist*0.5:
        return 0.0
    return np.cos(z / dist * np.pi)

parser = argparse.ArgumentParser(description='Generate the density to be fitted')
parser.add_argument('molecule',     metavar='molecule', type=str, help='xyz file')
parser.add_argument('dm',           metavar='dm',       type=str, help='dm file')
parser.add_argument('basis',        metavar='basis',    type=str, help='ao basis')
parser.add_argument('output',       metavar='output',   type=str, help='output file')
parser.add_argument('a1',           metavar='a1',       type=int, help='atom 1')
parser.add_argument('a2',           metavar='a2',       type=int, help='atom 2')
parser.add_argument('-g', '--grid', metavar='grid',     type=int, help='grid level', default=3)
parser.add_argument('--w',          dest='use_w',    action='store_true', help='weighting', default=False)
args = parser.parse_args()

mol = qstack.compound.xyz_to_mol(args.molecule, args.basis, ignore=True)

grid = dft.gen_grid.Grids(mol)
grid.level = args.grid
grid.build()

dm = np.load(args.dm)
ao = dft.numint.eval_ao(mol, grid.coords)
rho = np.einsum('pq,ip,iq->i', dm, ao, ao)

r1 = mol.atom_coord(args.a1-1, unit='ANG')
r2 = mol.atom_coord(args.a2-1, unit='ANG')
rm = (r1+r2)*0.5
atom = "No  % f % f % f" % (rm[0], rm[1], rm[2])

weights = grid.weights
coords  = grid.coords

if args.use_w:
    R1 = mol.atom_coord(args.a1-1)
    R2 = mol.atom_coord(args.a2-1)
    w2 = np.array(list(map(lambda x: weighting(x, R1, R2), coords)))
    weights *= w2
    # remove extra grid points
    idx     = np.nonzero(weights)
    weights = weights[idx]
    rho     = rho[idx]
    coords  = coords[idx]

np.savez(args.output, atom=atom, rho=rho, coords=coords, weights=weights)
