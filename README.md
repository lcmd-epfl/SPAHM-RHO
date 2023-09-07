# SPA<sup>H</sup>M(a,b)

This code supports the paper
>  K. R. Briling, Y. Calvino Alonso, A. Fabrizio, and C. Corminboeuf,<br>
> “SPAHM(a,b): encoding the density information from guess Hamiltonian in quantum machine learning representations”<br>
> [arXiv:2309.02950 [physics.chem-ph]](https://doi.org/10.48550/arXiv.2309.02950)<br>

The SPAHM(a) and SPAHM(b) representations are integrated to
[`Q-stack`](https://github.com/lcmd-epfl/Q-stack/tree/local-spahm).

This repo is a collection of scripts which allow to reproduce the results presented in the paper.

## Requirements
* [`qstack@local-spahm`](https://github.com/lcmd-epfl/Q-stack/tree/local-spahm)
* [`QML-toolkit >= 0.4`](https://www.qmlcode.org/) (optional, for comparison with aSLATM, see [`get_aSLATM.py`](get_aSLATM.py))

## Usage
<!-- See [workflow.md](workflow.md) for scripts to reproduce the results of the paper. !-->

SPAHM(a,b) can be computed either from command line or from a python script.
Below we show how to use the CLI.
Examples how to use the module are provided in [`get_SPAHM-ab.py`](get_SPAHM-ab.py).

### Compute SPAHM(a) representations


The SPAHM(a) representation can be generated separately for each molecule.

For example, the following line computes SPAHM(a)
with the [LB guess](https://doi.org/10.1007/s00214-019-2521-3) and the best-performing *long* Löwdin-population-analysis-based model
for ethanol radical cation concatenating α and β representations and saving the output to `out/C2H5OH_atom_alpha_beta.npy`:
```
python -m qstack.spahm.rho.atom --mol mol/C2H5OH.xyz --nameout out/C2H5OH_atom \
                                --omod alpha beta --charge +1 --spin 1 \
                                --guess lb --model lowdin-long-x \
                                --species H C N O F S
```
For a correct vector padding, a list of elements presented in the dataset is required (`--species` argument).

<details><summary><b>Full reference</b></summary>

```
usage: atom.py [-h] --mol MOL [--guess GUESS] [--units UNITS] [--basis-set BASIS] [--aux-basis AUXBASIS] [--model MODEL] [--dm DM]
               [--species ELEMENTS [ELEMENTS ...]] [--charge CHARGE] [--spin SPIN] [--xc XC] [--nameout NAMEOUT]
               [--omod OMOD [OMOD ...]]

  --mol MOL                           the path to the xyz file with the molecular structure
  --species ELEMENTS [ELEMENTS ...]   the elements contained in the database
  --nameout NAMEOUT                   name of the output representations file.
  --charge CHARGE                     total charge of the system (default: 0)
  --spin SPIN                         number of unpaired electrons (default: None) (use 0 to treat a closed-shell system in a UHF manner)
  --units UNITS                       the units of the input coordinates (default: Angstrom)

  --xc XC                             DFT functional for the SAD guess (default: hf)
  --guess GUESS                       the initial guess Hamiltonian to be used (default: LB)
  --basis-set BASIS                   basis set for computing density matrix (default: minao)
  --aux-basis AUXBASIS                auxiliary basis set for density fitting (default: ccpvdzjkfit)
  --model MODEL                       the model to use when creating the representation (default: Lowdin-long-x)
  --omod OMOD [OMOD ...]              model(s) for open-shell systems (alpha, beta, sum, diff, default: ['alpha', 'beta'])
  --dm DM                             a density matrix to load instead of computing the guess
```
</details>

### Compute SPAHM(b) representations

The SPAHM(b) representation can be generated separately for each molecule as well.
For example, the SPAHM(b) counterpart of the atom-based representation above is computed with
```
python -m qstack.spahm.rho.bond --mol mol/C2H5OH.xyz --name out/C2H5OH_bond \
                                --omod alpha beta --charge +1 --spin 1 \
                                --guess lb
```

However, to pad SPAHM(b) vectors correctly a full information on dataset composition and atomic distances is required.
One way is to run the script for the whole dataset by specifing the files containing the paths to the xyz files, charges, and spins, e.g.
```
python -m qstack.spahm.rho.bond --mol mol/set1.inp --name out/set1_bond \
                                --omod alpha beta --charge mol/set1_charge.dat --spin mol/set1_spin.dat \
                                --guess lb
```

<details><summary>(files content)</summary>

```
==> mol/set1.inp <==
mol/C2H5OH.xyz
mol/CH3NH2.xyz

==> mol/set1_charge.dat <==
+1
-1

==> mol/set1_spin.dat <==
1
1
```
</details>
generates correctly-padded SPAHM(b) for a “dataset” consisting of ethanol radical cation and methylamine radical anion.

If the dataset is too big, one can first dump the atom-pair information to `out/set1_pairs.npy` with
```
python -m qstack.spahm.rho.bond --mol mol/set1.inp --name out/set1_bond --pairfile out/set1_pairs.npy --dump_and_exit
```
and then use it for each molecule separately or for dataset fractions:
```
paste mol/set1.inp mol/set1_charge.dat mol/set1_spin.dat | while read MOL CHARGE SPIN ; do
    python -m qstack.spahm.rho.bond --mol ${MOL} --name out/set1_$(basename ${MOL/.xyz/})_bond \
                                    --omod alpha beta --charge ${CHARGE} --spin ${SPIN} \
                                    --guess lb \
                                    --pairfile out/set1_pairs.npy
done
```


<details><summary><b>Full reference</b></summary>

```
usage: bond.py [-h] --mol FILENAME --name NAME_OUT [--guess GUESS] [--units UNITS] [--basis BASIS] [--charge CHARGE] [--spin SPIN]
               [--xc XC] [--dir DIR] [--cutoff CUTOFF] [--bpath BPATH] [--omod OMOD [OMOD ...]] [--print PRINT] [--zeros] [--split]
               [--merge] [--onlym0] [--savedm] [--readdm READDM] [--elements ELEMENTS [ELEMENTS ...]] [--pairfile PAIRFILE]
               [--dump_and_exit]

  --mol FILENAME                        path to an xyz file / to a list of molecular structures in xyz format
  --name NAME_OUT                       name of the output file
  --guess GUESS                         initial guess
  --units UNITS                         the units of the input coordinates (default: Angstrom)
  --basis BASIS                         AO basis set (default=MINAO)
  --charge CHARGE                       charge / path to a file with a list of thereof
  --spin SPIN                           number of unpaired electrons / path to a file with a list of thereof
  --xc XC                               DFT functional for the SAD guess (default=hf)
  --dir DIR                             directory to save the output in (default=current dir)
  --cutoff CUTOFF                       bond length cutoff in Å (default=5.0)
  --bpath BPATH                         directory with basis sets (default=<...>/qstack/spahm/rho/basis_opt)
  --omod OMOD [OMOD ...]                model for open-shell systems (alpha, beta, sum, diff, default=['alpha', 'beta'])
  --print PRINT                         printing level
  --zeros                               use a version with more padding zeros
  --split                               split into molecules
  --merge                               merge different omods
  --onlym0                              use only functions with m=0
  --savedm                              save density matrices
  --readdm READDM                       directory to read density matrices from
  --elements ELEMENTS [ELEMENTS ...]    the elements to limit the representation for
  --pairfile PAIRFILE                   path to the atom pair file
  --dump_and_exit                       write the atom pair file and exit if --pairfile is set
```
</details>

### Hyperparameter search and regression
(Under construction)

### Basis set optimization
(Under construction)
