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

### Compute SPAHM(b) representations for selected bonds

The SPAHM(b) representation can be generated also for specific bonds.

For example, representations for the C–O bond of ethanol radical cation and C–N bond of methylamine radical anion
are computed as follows:
```
python -m qstack.spahm.rho.bond_selected --mol mol/set2.inp --dir out/ \
                                         --omod alpha beta --charge mol/set1_charge.dat --spin mol/set1_spin.dat \
                                         --guess lb
```
The input file contains paths to the xyz files as well as indices (base 1) of atoms forming the bond of interest.
<details><summary>(file content)</summary>

```
==> mol/set2.inp <==
mol/C2H5OH.xyz   2 3
mol/CH3NH2.xyz   1 2
```
</details>

### Hyperparameter search and regression
Hyperparameters cross-validated grid-search was used to find the optimal parameters of the KRR model. It can be performed using the corresponding Q-stack module.
Where the numbers of split for cross-validation and the grid values can be specified using the `--splits`, `--eta` and `--sigma`
parameters respectivley. Currently 3 kernel functions are avaiable for kernel generation: Gaussian, Laplacian and linear. The desired one can 
be selected through the `--kernel` parameter (default: Laplacian).

For example searching the `eta` and `sigma` parameters minimizing the mean absolute error (MAE) with respect to the toy-properties found in 
`./mol/y_set1.txt` using a Laplacian kernel is done by running:
```
python -m qstack.regression.hyperparameters --x out/set1_bond_alpha_beta.npy \
                                            --y mol/y_set1.txt \
                                            --akernel L
```
The output displays the list with all tested `eta` and `sigma` values with the corresponding MAE and standard-variations in invrese order 
(from highest to lowest MAE value).

<details><summary>(output content)</summary>

```
error        stdev          eta          sigma
5.178182e+00 1.393084e+00 | 1.000000e+00 1.000000e+06
5.178182e+00 1.393083e+00 | 1.000000e+00 3.162278e+05
    ...         ...             ...         ...
3.451178e+00 1.545717e+00 | 3.162278e-08 1.000000e+02
3.450524e+00 1.510564e+00 | 1.000000e-05 1.000000e+01
3.450092e+00 1.550506e+00 | 1.000000e-10 1.000000e+04
3.449305e+00 1.552126e+00 | 1.000000e-10 3.162278e+03
3.448982e+00 1.552641e+00 | 1.000000e-10 1.000000e+03
3.448697e+00 1.552728e+00 | 1.000000e-10 3.162278e+02
3.448032e+00 1.552502e+00 | 1.000000e-10 1.000000e+02
3.447143e+00 1.549218e+00 | 3.162278e-08 3.162278e+01
3.446003e+00 1.551632e+00 | 1.000000e-10 3.162278e+01
3.439973e+00 1.548043e+00 | 3.162278e-08 1.000000e+01
3.439598e+00 1.548834e+00 | 1.000000e-10 1.000000e+01
3.429671e+00 1.512283e+00 | 1.000000e-05 3.162278e+00
3.419343e+00 1.539770e+00 | 3.162278e-08 3.162278e+00
3.419226e+00 1.540019e+00 | 1.000000e-10 3.162278e+00
3.359772e+00 1.498204e+00 | 1.000000e-05 1.000000e+00
3.353693e+00 1.512606e+00 | 3.162278e-08 1.000000e+00
3.353659e+00 1.512681e+00 | 1.000000e-10 1.000000e+00

```
</details>
<details><summary><b>Full reference</b></summary>

```
usage: hyperparameters.py [-h] --x REPR --y PROP [--test TEST_SIZE] [--akernel AKERNEL] [--gkernel GKERNEL] [--gdict [GDICT ...]] [--splits SPLITS] [--print PRINTLEVEL]
                          [--eta ETA [ETA ...]] [--sigma SIGMA [SIGMA ...]] [--ll] [--ada] [--readkernel]

This program finds the optimal hyperparameters.

options:
  -h, --help            show this help message and exit
  --x REPR              path to the representations file
  --y PROP              path to the properties file
  --test TEST_SIZE      test set fraction (default=0.2)
  --akernel AKERNEL     local kernel type (G for Gaussian, L for Laplacian, myL for Laplacian for open-shell systems) (default L)
  --gkernel GKERNEL     global kernel type (avg for average kernel, rem for REMatch kernel) (default )
  --gdict [GDICT ...]   dictionary like input string to initialize global kernel parameters
  --splits SPLITS       k in k-fold cross validation (default=5)
  --print PRINTLEVEL    printlevel
  --eta ETA [ETA ...]   eta array
  --sigma SIGMA [SIGMA ...]
                        sigma array
  --ll                  if correct for the numper of threads
  --ada                 if adapt sigma
  --readkernel          if X is kernel

```
</details>
Once the output has been generated, the optimized parameters can be extract from the last line to perform the final regression using the 
approtiate Q-satck module as (using the ouput from the previous example):

```
python -m qstack.regression.regression  --x out/set1_bond_alpha_beta.npy \
                                        --y mol/y_set1.txt \
                                        --akernel L \
                                        --eta 1.000000e-10 \
                                        --sigma 1.000000e+00
```

The output is a table containing all training-set sizes averaged over 5 randomly shuffled runs (training set).
<details><summary>(output extract)</summary>
size    MAE             STD

```
1	4.109106e+00	1.125572e+00
3	4.140986e+00	1.258406e+00
6	2.546631e+00	8.568210e-01
9	1.737456e+00	4.872807e-01
12	2.436564e+00	1.763576e-12

```

</details>

<details><summary><b>Full reference</b></summary>

```
usage: regression.py [-h] --x REPR --y PROP [--test TEST_SIZE] [--eta ETA] [--sigma SIGMA] [--akernel AKERNEL] [--gkernel GKERNEL] [--gdict [GDICT ...]] [--splits SPLITS]
                     [--train TRAIN_SIZE [TRAIN_SIZE ...]] [--debug] [--ll] [--readkernel]

This program computes the learning curve.

options:
  -h, --help            show this help message and exit
  --x REPR              path to the representations file
  --y PROP              path to the properties file
  --test TEST_SIZE      test set fraction (default=0.2)
  --eta ETA             eta hyperparameter (default=1e-05)
  --sigma SIGMA         sigma hyperparameter (default=32.0)
  --akernel AKERNEL     local kernel type (G for Gaussian, L for Laplacian, myL for Laplacian for open-shell systems) (default L)
  --gkernel GKERNEL     global kernel type (avg for average kernel, rem for REMatch kernel) (default None)
  --gdict [GDICT ...]   dictionary like input string to initialize global kernel parameters
  --splits SPLITS       number of splits (default=5)
  --train TRAIN_SIZE [TRAIN_SIZE ...]
                        training set fractions
  --debug               enable debug
  --ll                  if correct for the numper of threads
  --readkernel          if X is kernel

```
</details>

### Basis set optimization
The basis functions used to fit the bond-density between two atoms to a set of single atom-centered expansion coefficients (where the single atom is fictiously placed at 
at the middle of the bond are optimized according to atom-type with the following procedure:
1. We build a set, for the desired pair of atoms, composed of several structures containing this specific bond with optimized geometries (high-level of theory). We generate the density-matrix 
associated with the selected bond, using Lowdin formalism and the molecular density-matrix evaluated at the single point PBE level of theory.
2. We project the obtained density-matrix onto a grid in real space and fix a fictious Nobelium atom at the middle of the selected bond.
3. We perform a basis-set optimization procedure, as implemented in Q-stack, on the fictious atom, starting from any basis-set file (`*.bas`). 

All the necessary scripts are located at `/supplementary_for_bond/basis`.

`1_extract_dm_bond.py` takes as input a single molecular structure file, the total charge and spin of the compound and the indices attributed to the atoms involved in the bond. 
The script saves the associated bond-density matrix to a `.npy` file.
```
1_extract_dm_bond.py $PATH_TO_XYZ $CHARGE $SPIN $INT_1 $INT_2
```
For conveniance we provide a bash-script to extract the bond-density of various structures: `1_extract_dm_bond.bash`. This script takes a list of structures with associated
charges and spins and the pair of the atom indices defining the selected bond gather in a text-file named `xyz.dat` (fixed name).
<details><summary><b>Example</b></summary>

```
# mol charge spin a1 a2
CH4.xyz        0 0       1 2
CO.xyz         0 0       1 2
H2CCH2.xyz     0 0       1 4
H2CNH.xyz      0 0       1 4
```
</details>

`2_generate_rho.py` script takes as input the bond-density matrices generated using `1_extract_dm_bond.py`, the basis-set used to project the density-matrix (i.e. minao) 
and again the pair of indices defining the bond.
```
./2_generate_rho.py $PATH_TO_XYZ $BOND_DM minao $OUTPUT_NAME $INT_1 $INT_2
```
`2_generate_rho.bash` provides a script to automatically re-use the afro-mentioned `xyz.dat` file, following the output filenames as implemented in `1_extract_dm_bond.py`.

Finally `3_optimizer.py` script is a wrapper to gather all the projected bond-densities associated with a given  bond-type and an initial basis function (*.bas) to be optimized. 
The script uses the Q-stack package for the fitting procedure.

**All optimized basis can be found at `supplementary_for_bond/basis_opt/`**

**Alternative optimized basis functions (s orbitals only) can be found at `supplementary_for_bond/basis_test_s`**
*The folder `supplementary_for_bond/numerical/` provdies tools for to numerically test the averaging around the z-axis, please refer to the `README.bash` file for procedure.
