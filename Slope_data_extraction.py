import numpy as np
import rasterio
from rasterio.transform import Affine

# ============================
# INPUT / OUTPUT FILES
# ============================
dem_file = "Karnataka_dem.tif"
slope_file = "Karnataka_slope.tif"

# ============================
# READ DEM
# ============================
with rasterio.open(dem_file) as src:
    dem = src.read(1).astype(np.float32)
    profile = src.profile.copy()
    transform = src.transform
    nodata = src.nodata

# Replace NoData with NaN
if nodata is not None:
    dem[dem == nodata] = np.nan

# Pixel size
pixel_width = transform.a
pixel_height = abs(transform.e)

# ============================
# COMPUTE GRADIENTS
# ============================
dz_dy, dz_dx = np.gradient(dem, pixel_height, pixel_width)

# Slope in radians
slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))

# Convert to degrees
slope_deg = np.degrees(slope_rad)

# Replace NaN with 0
slope_deg = np.nan_to_num(slope_deg)

# ============================
# SAVE SLOPE RASTER
# ============================
profile.update(dtype=rasterio.float32, count=1)

with rasterio.open(slope_file, "w", **profile) as dst:
    dst.write(slope_deg.astype(rasterio.float32), 1)

print("Slope raster saved as:", slope_file)
