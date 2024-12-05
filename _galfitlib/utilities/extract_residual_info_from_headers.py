import numpy as np
import pandas as pd
import sys
from galfitlib.classes.fits_handlers import *
from galfitlib.functions.helper_functions import *

def main(*args):
    basename         = args[0]
    pkl_end_str      = args[1]
    out_dir          = args[2] #os.path.dirname(basename)
    galaxy_names     = args[3].split(",")
    output_df        = pd.DataFrame()
    
    #out_nmr = parallel_wrapper(galfit_tmp_path, galfit_mask_path, out_png_dir, all_gname_tmp_out)
    all_df = pd.DataFrame()
    DNE_dict = {"gname" : []}
    for gname in galaxy_names:
        output_file = pj(out_dir, gname, f"{gname}_galfit_out.fits")

        if exists(output_file):
            output_fits = OutputFits(output_file)
            output_df   = output_fits.feedme.to_pandas()
            output_df["gname"]   = gname
            output_df["NMR"]     = output_fits.model.header.get("NMR", None) 
            output_df["KS_P"]    = output_fits.model.header.get("KS_P", None)
            #output_df["KS_STAT"] = output_fits.model.header.get("KS_STAT", None)
            
            all_df = pd.concat([all_df, output_df])
            # with fits.open(output_file) as hdul: 
            #     output_dict[gname] = (hdul[2].header.get("NMR", None), 
            #                           hdul[2].header.get("ks_p", None),
            #                           hdul[2].header.get("ks_stat", None)
            #                          )
            
        else:
            DNE_dict["gname"].append(gname)
            #output_dict[gname] = (None, None, None)

    # TODO: Will this mess up the analysis framework?
    DNE_dict2 = {
        col : ["N/A"]*len(DNE_dict["gname"])
        for col in output_df.columns if col != "gname"
    }
    DNE_dict2["gname"] = DNE_dict["gname"]
    all_df = pd.concat(
            [all_df, pd.DataFrame(DNE_dict2, dtype = "object")],
            ignore_index = True
    ).replace("N/A", pd.NA)

    all_df.set_index("gname", inplace = True)
    
    if basename:
        pickle_filename = f'{basename}_{pkl_end_str}.pkl'
        all_df.to_pickle(pickle_filename)
    #pickle.dump(output_dict, open(pickle_filename, 'wb'))
    
    return all_df

if __name__ == "__main__":
    basename         = sys.argv[1]
    pkl_end_str      = sys.argv[2]
    out_dir          = sys.argv[3] #os.path.dirname(basename)
    galaxy_names     = sys.argv[4] #.split(",")
    
    main(basename, pkl_end_str, out_dir, galaxy_names)

