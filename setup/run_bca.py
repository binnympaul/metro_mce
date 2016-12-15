# bca4abm
# Copyright (C) 2016 RSG Inc
# See full license in LICENSE.txt.

import orca
import pandas as pd
import numpy as np
import os

from bca4abm import tracing

#startup
# there is something a little bit too opaque about this:
# the following import has the side-effect of registering injectables
from bca4abm import bca4abm as bca

parent_dir = os.path.dirname(__file__)
if not os.path.exists(os.path.join(parent_dir, 'output')):
    os.makedirs(os.path.join(parent_dir, 'output'))
orca.add_injectable('configs_dir', os.path.join(parent_dir, 'configs'))
orca.add_injectable('data_dir', os.path.join(parent_dir, 'data'))
orca.add_injectable('output_dir', os.path.join(parent_dir, 'output'))
tracing.config_logger()

orca.add_injectable('input_source', 'read_from_csv')
orca.run(['initialize_stores'])

#each row in the data table to solve is an origin zone and this processor
#calculates communities of concern (COC) / market segments based on mf.cval.csv
orca.run(['aggregate_demographics_processor'])

# each row in the data table to solve is an origin zone and this
# processor calculates zonal auto ownership differences as well as the
# differences in the destination choice logsums - ma.<purpose|income>dcls.csv
orca.run(['aggregate_zone_processor'])

# each row in the data table to solve is an OD pair and this processor
# calculates trip travel time savings, etc.  It requires the access to input zone tables,
# the COC coding, trip matrices and skim matrices.  The assign_mfs.omx, inputs and 
#results of the zone aggregate processor, and skims_mfs.omx are input.
orca.run(['aggregate_od_processor'])

# daily will be linkMD1 * scalingFactorMD1 + linkPM2 * scalingFactorPM2
orca.run(['link_daily_processor'])

#write results
orca.run(['write_four_step_results'])
orca.run(['print_results'])
