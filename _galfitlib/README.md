<h1> galfitlib </h1>

An object-oriented python library to handle [GALFIT](https://users.obs.carnegiescience.edu/peng/work/galfit/galfit.html) I/O and other tasks.

<h1> README (work in progress) </h1>

The scripts in this folder are written to automatically generate GALFIT input files from SpArcFiRe output.

Please note, this library is still a work-in-progress and relies on some assumptions having to do with SpArcFiRe's conventions.
These will be fixed in a future update.

<h2> INTRODUCTION </h2>

The previous version of the GALFIT processing was simply a few scripts, `s2g.py` and others, 
written to automatically generate the disk and bulge parameters for GALFIT. `s2g.py` was 
intended to include the generation of spiral arc parameters but was halted before it could be completed.

The current version of the code has been written as a Python library in order to use an OOP framework.
In the galfitlib, OOP constitutes the underlying framework and much of the pre and post-processing relies on it. 
The creation of the library in this framework is twofold:
1) OOP allows us to utilize distributed computing with multi-step fitting (necessary for certain GALFIT practices) and
2) The OOP framework can be used by others to streamline their usage of GALFIT with Python.
Note, the galfitlib in its current state _requires_ **Python3.7 or greater**. This choice has been made to utilize
the CaptureOutput feature of the Subprocess Python library, which is crucial during multi-step fitting.

There are three main scripts which are run to perform the fitting, 
`s2g_feedme_gen.py`, which generates the galfit input file from the results from SpArcFiRe,
`go_go_galfit.py`, which more or less runs GALFIT and is the script that is sent to the compute nodes in distributed computing, and
`control_script.py`, which prepares everything for `go_go_galfit.py` and processes the output.

`s2g_feedme_gen.py` is written such that it can be run on its own from the command line to generate the GALFIT input
files without actually running them. These files are placed in the individual galaxy directories. We recommend doing this on
a first installation to verify that everything is working correctly before running `control_script.py`.

The `control_script.py` operates on the assumption that there are three directories, input, temporary, and output to coincide
with SpArcFiRe's convention of the same. The script is currently restricted to directories which end in _"-in", "-tmp", "-out"_
for convention reasons and some assumptions used in the library when processing. Again, this will likely disappear in a production version.
`control_script.py` defaults to using on-node parallelization via **parallel** which can be found in the ParallelDrivers directory,
an executable written by Wayne Hayes at UCI. It can be run in serial and has several options which can be accessed by running
`control_script.py --help` on the command line.
See the 'Current Directory Structure' section below for an example of what files are put where when `control_script.py` is run.

![Flow chart for `control_script.py`](control_script_flowchart.png)

`go_go_galfit.py` need not be touched. In fact, it may be a little confusing since it uses many functionalities from the OOP framework
to do most of the leg work, so it may be more of a rabbit hole than anything else. It is currently only somewhat documented but feel
free to contact Matthew if something is unclear.

![Flow chart for 3(+1) component version of `go_go_galfit.py`](go_go_galfit_flowchart_3+1.png)

Most OOP implementation things can be found in the `classes` directory in the library. We recommend taking a look at the 
Jupyter Notebook version of these codes which can be found in the `notebooks` dirs located inside each class folder in order
to familiarize yourself (until tutorials come along). 

Several utility scripts can be found in the (aptly named) `utilities` folder some of which are currently used by 
`control_script.py` and `go_go_galfit.py`. There is also a Notebook which details an analysis procedure for the results
output from our pipeline entitled `results_analysis.ipynb`. We recommend starting there to get an idea of how the results may
be used or processed.

There is also a regression test which can be run from the `tests` directory as `python3 reg_test.py`.

---

<h2> Output Directory Structure </h2> 

```
*[IN-DIRECTORY]  --    input FITS files

                       *galfit_masks -- SExtractor Star Masks
*[TMP-DIRECTORY] -- <- *galfits      -- Output FITS models (and empty files to indicate failure)
                       *galfit_png   -- PNG files generated from output FITS

                                        Output 'combined' PNG (observation, model, residual)
*[OUT-DIRECTORY] -- <- *galaxy_dirs  <- Output FITS model
                                        File(s) used for input to GALFIT
                                        (PSFs go here as galaxyname_psf.fits)

                                        *galfit_png -- All FITS models converted to PNG
                       *runname_dir  <- Output tar.gz file containing all FITS models
                                        Output pkl file containing a pandas dataframe of the parameterization for all models

```

---

<h2> TO RUN: </h2>

Note: _SpArcFiRe_'s setup.bash _must_ be run first so that the *SPARCFIRE_HOME* environment variable is set. From there,
the library can figure everything else out pathing-wise.

`python3 control_script.py [OPTION] [[RUN-DIRECTORY] IN-DIRECTORY TMP-DIRECTORY OUT-DIRECTORY]`

Ex:

`python3 control_script.py -p 0 -NS 1 -v`

<h3> Arguments: </h3>

(these can also be seen by running `python3 control_script.py --help`)

<h3> -p | --parallel [0, 1, 2] (default 1) </h3>

Run algorithm with/without intensive parallelization. Defaults to on machine parallel.

Options are:
- 0: in serial,
- 1: on machine parallel,
- 2: cluster computing via SLURM
                                    
<h3> -drs | --dont-remove-slurm (default False, i.e. removal) </h3>

Choose NOT to remove all old slurm files (they may contain basic info about each fit but there will be a bunch!)

<h3> -t  | --tmp (default False) </h3>

Indicates to the program a run from a directory in /tmp/ local to each cluster machine.
WARNING: either output to a different location or copy from tmp to said location
under the assumption that tmp will be wiped at some point in the near future.

<h3> -ac | --aggressive-clean (default False) </h3>

Aggressively clean-up directories, removing -in, temp output, psf, and mask files after galfit runs

<h3> -NS | --num-steps [1, 2, 3] (default 2) </h3>

Run GALFIT using step-by-step component selection (up to 3), i.e.
- 1: Bulge + Disk + Arms,
- 2: Disk -> Bulge + Disk + Arms,
- 3: Disk -> Bulge + Disk -> Bulge + Disk + Arms
                                    
<h3> -r | --restart (default False) </h3>

Restart control script on the premise that some have already run (likely in parallel).

<h3> -nsf | --no-simultaneous-fitting (default True, also not currently implemented) </h3>

Turn off simultaneous fitting.

<h3> -v | --verbose </h3>

Verbose output. Includes standard out.

<h3> -n | --basename [name] (default "GALFIT") </h3>

Basename of the output results pkl file (\[name\]_output_results.pkl).

<h3> RUN-DIRECTORY (default current working directory) </h3>

The directory from which the script should be run 

<h3> IN-DIRECTORY (default cwd/sparcfire-in) </h3>

Images used by SpArcFiRe, _must_ be FITS files, GALFIT does not take PNG as input.

<h3> TMP-DIRECTORY (default cwd/sparcfire-tmp) </h3>

Extra output including star masks, PNG conversions, and galfit output

<h3> OUT-DIRECTORY (default cwd/sparcfire-out) </h3>

Galaxy folders from SpArcFiRe which will also hold the output from this script 
including `.in` files, final galfit output, and final output 'combined' pngs.

***Since the library is still a WIP, please name these folders [name]-in, [name]-tmp, [name]-out or
the script(s) won't work. `control_script.py` defaults to "sparcfire-in", "sparcfire-tmp", and "sparcfire-out".
Feel free to use those if you'd like!***

---

<h2> JUST THE FEEDME PARAMETERS </h2>

`python3 s2g_feedme_gen.py`

(it must be run in Python >3.6 to work with f-string implementation)

We recommend running this alone upon first installation to ensure it works correctly.

---
<h2> OUTPUT </h2>

Several items are output as a result of this script which are detailed in the **Directory Structure**
section above. Importantly, the results of the fits, i.e. the final GALFIT parameters used to generate
the model for each galaxy, are tabulated into a Pandas DataFrame saved as a pickle file, `[basename]_output_results[num].pkl`
\[num\] is iterative and merely prevents an overwrite of the results of a previous run with the same basename.
Note: for [security reasons](https://docs.python.org/3/library/pickle.html), this may be updated to a csv 
or more secure storage format in the future. 

The format of the DataFrame arises from the OOP framework
and uses dynamically named column headers that follow the convention: `[parameter name]_[component type]_[component_number]`
e.g. `magnitude_sersic_1` or `position_x_sersic_2`. 

The DataFrame is the *easiest* way to extract parameters from the fitting process but parameter 
extraction can also be achieved by using classes and methods from the galfitlib to read the 
output FITS files themselves.

We also recommend taking a look at the _combined_ pngs in the `OUT-DIRECTORY/galfit_png` folder or
in the `OUT-DIRECTORY/[galaxy name]` folder itself. The conversion for FITS to PNG is not straightforward
but these images can serve as a litmus test for the goodness of fit, especially when viewing the residual.

---

It is possible to perform the feedme generation with just the input FITS and feedme but there are other optional
inputs which we recommend and which are also generated by the pipeline---to avoid their inclusion, we recommend providing a
string with GALFIT's comment convention (# string) on the corresponding lines in `s2g_feedme_gen.py`:

* Star Masks: Requires the use of `SExtractor`. Parameters and python script found in `star_removal`. `control_script.sh`
automatically generates a folder to hold the masks and checks if they've already been generated. Placed in a folder in
TMP-DIRECTORY. 

* PSF Generation (SDSS only): Requires the use of the `Read_PSF` program from SDSS's website. `s2g_feedme_gen.py`
takes information from the csv included in star_dl according to our own naming convention - as controlled by a function in
`s2g_feedme_gen.py` to be easily modified to follow SDSS' naming convention - and
outputs the information necessary to find and download the psfield file into the generated feedme. The 
psfield should then be processed by the `Read_PSF` executable.
** NOTE, to modify the soft bias of the PSF files, once you compile the `Read_PSF` executable, you must modify the file,
`phConsts.h`, changing the value of `SOFT_BIAS` to that which is desired. If this is not done, the PSF generated will 
produce bad output due to the existence of a pedestal. 

* Output conversion to PNG: Requires the use of the `fitspng` utility from http://integral.physics.muni.cz/fitspng/. 
fitspng provides an easy and efficient way to convert the output from GALFIT to pngs for ease of viewing. This is also
already included in the control script. If the pngs seem to be blown out, it's possible the conversion utility is having
trouble with some flags in control_script.sh. If this is the case, try removing the flag -fr "1,150" and then run. This has
only occurred on one machine for reasons I'm not familiar with. control_script.sh then uses the *ImageMagick* utility to 
automatically panel the PNG converted output with some of SpArcFiRe's to reduce bloat and make comparison easy. The converted
PNGs are then deleted and all that is left is the combined/paneled image in a separate folder within sparcfire-out.


------------------------------------------------------------------------------------
<h2>Disclaimer</h2>

This software is an independent creation and is intended to be used as a supplemental tool. It is not affiliated with, endorsed by, or in any way officially connected to [GALFIT](https://users.obs.carnegiescience.edu/peng/work/galfit/galfit.html) 
or its developers. All product names, trademarks, and registered trademarks are the property of their respective owners. The use of these names, trademarks, and brands does not imply endorsement or affiliation.

------------------------------------------------------------------------------------
<h2>Acknowledgements</h2>

This work was supported by the Computational Science Research Center at San Diego State University, the University of California Irvine School of Information and Computer Sciences, and National Science Foundation (NSF) grant DUE-1259951. 

We would also like to thank the LSST-DA Data Science Fellowship Program, which is funded by LSST-DA, the Brinson Foundation, and the Moore Foundation; the primary author's participation in the program has benefited this software.

This software has benefited greatly from communication with Chien Peng. His help greatly improved our understanding of GALFIT. We would additionally like to thank him for his prompt and courteous replies.

Additional thanks to:

Darren Davis who wrote SpArcFiRe.

Wayne for his guidance, patience, and support.

Azra Zahin, whose work aided the development of the pitch angle analysis and bulge masking routine.

------------------------------------------------------------------------------------
galfitlib is developed and maintained by Dr. Matthew Portman, (formerly) under the tutelage of Dr. Wayne Hayes, UCI.

Email: <portmanm@uci.edu>
