#%% Load libs
import geopandas
from pathlib import Path
import pandas as pd
import datetime

#%% Setup paths
INPUT_PATH = Path.cwd() / "input"

ce_legacy_path = INPUT_PATH / "CookEastStrips" / "Field_Plan_Final.shp"
ce_2016_c01_path = INPUT_PATH / "FromIanLeslie_CafGeospatial" / "CE_CW_WGS1984" / "CE_WGS1984_2016_OperationalFieldBoundaries" / "C01" / "C0117001.shp"
ce_2016_c02_path = INPUT_PATH / "FromIanLeslie_CafGeospatial" / "CE_CW_WGS1984" / "CE_WGS1984_2016_OperationalFieldBoundaries" / "C02" / "C0217001.shp"
ce_current_path = INPUT_PATH / "20170206_CafRoughBoundaries" / "CafCookEastArea.shp"

cw_current_path = INPUT_PATH / "FromIanLeslie_CafGeospatial" / "CE_CW_WGS1984" / "CookWestBoundariesWGS1984" / "CookWestBoundariesWGS1984.shp"


#%% Load data

# Cook East Legacy (1999 - 2015)
ce_legacy = geopandas.read_file(ce_legacy_path)
filter_ind_field = ce_legacy["Ind_Field"].isin(range(0,21,1))
ce_legacy = ce_legacy[filter_ind_field]
ce_legacy = ce_legacy.to_crs({"init": "epsg:4326"})
ce_legacy.plot()

# Cook East 2016
ce_2016_c01 = geopandas.read_file(ce_2016_c01_path)
ce_2016_c02 = geopandas.read_file(ce_2016_c02_path)
ce_2016_c01 = ce_2016_c01.assign(
    Exp_Unit_ID = "C01"
)
ce_2016_c02 = ce_2016_c02.assign(
    Exp_Unit_ID = "C02"
)
ce_2016 = pd.concat([ce_2016_c01, ce_2016_c02], ignore_index=True)
ce_2016.plot()

# Cook East Current
ce_current = geopandas.read_file(ce_current_path)
ce_current = ce_current.to_crs({"init": "epsg:4326"})
ce_current.plot()

# Cook West Current
cw_current = geopandas.read_file(cw_current_path)
cw_current.plot()

#%% Add standardized fields

# Cook East Legacy
ce_legacy = ce_legacy.assign(
    Exp_Unit_ID = ce_legacy["Field"].astype(str) + ce_legacy["Strip"].astype(str),
    Status = "Past",
    Start_Date = "01/01/1999",
    End_Date = "12/31/2015",
    Treatment_ID = "ASP"
)

# Cook East 2016
ce_2016 = ce_2016.assign(
    Status = "Past",
    Start_Date = "01/01/2016",
    End_Date = "12/31/2016",
    Treatment_ID = "ASP"
)

# Cook East Current
ce_current = ce_current.assign(
    Exp_Unit_ID = "CE",
    Status = "Current",
    Start_Date = "01/01/2017",
    End_Date = None,
    Treatment_ID = "ASP"
)

# Cook West Current
cw_current = cw_current.assign(
    Exp_Unit_ID = "CW",
    Status = "Current",
    Start_Date = "01/01/2017",
    End_Date = None,
    Treatment_ID = "BAU"
)

#%%  Clean fields

ce_legacy = ce_legacy.drop(
    ["Strip", "Field", "Crop", "Area", "Perimeter", "Area_ac", "Ind_Field"], 
    axis = 1)
ce_2016 = ce_2016.drop(
    ["Description"], 
    axis = 1)
ce_current = ce_current.drop(
    ["Id", "Area", "Perimeter", "Acres", "Hectares"], 
    axis = 1)
cw_current = cw_current.drop(
    ["Id", "POLY_AREA", "AREA_GEO", "PERIMETER", "PERIM_GEO"], 
    axis = 1)

#%% Merge and add final fields

exp_boundaries = pd.concat(
    [ce_legacy,
    ce_2016,
    ce_current,
    cw_current], ignore_index=True)

exp_boundaries = exp_boundaries.assign(
    Site_ID = "CAF",
    SiteID_Description = "R.J. Cook Agronomy Farm",
    LTAR_FieldID = None,
    Shape_Leng = None,
    Shape_Area = None
)

exp_boundaries.head()


#%% Output
curr_date = datetime.datetime.now().strftime("%Y%m%d")
out_path = Path.cwd() / "output" / ("ltar_experiments_bndy_a_caf_" + curr_date)
out_path.mkdir(parents=True, exist_ok=True)
out_file = "ltar_experiments_bndy_a.shp"
exp_boundaries.to_file(Path(out_path / out_file))
