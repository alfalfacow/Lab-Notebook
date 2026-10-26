#!/usr/bin/env python3
"""
Export a HEST-1K AnnData (.h5ad) sample into a Seurat/Visium-style folder.

Configured for:
  Input:  /Users/alfred/Downloads/HTAN_Vanderbilt/MISC73.h5ad
  Output: /Users/alfred/Downloads/HTAN_Vanderbilt/MISC73/

This version uses adata.X as the expression matrix because the inspected
HEST object has no layers and adata.X contains nonnegative integer-valued data.
Integer values are consistent with raw counts but are not, by themselves, proof
of provenance; confirm the HEST file documentation if raw-count provenance is
critical.

The script preserves the existing array and pixel coordinate columns in adata.obs.
Validate the exported spot/image overlay in Seurat before downstream spatial
analysis. This is a Seurat-compatible export, not original Space Ranger output.
"""

from pathlib import Path
import gzip
import json
import sys

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.io import mmwrite
from PIL import Image

# ============================================================
# CONFIGURATION
# ============================================================

INPUT_H5AD = Path(
    "/Users/alfred/Downloads/HTAN_Vanderbilt/MISC73.h5ad"
)

OUTPUT_DIR = Path(
    "/Users/alfred/Downloads/HTAN_Vanderbilt/MISC73"
)

SPATIAL_LIBRARY_ID = "ST"

# ============================================================
# LOAD AND VALIDATE INPUT
# ============================================================

if not INPUT_H5AD.is_file():
    sys.exit(f"ERROR: Input .h5ad file not found: {INPUT_H5AD}")

print(f"Reading: {INPUT_H5AD}")
adata = ad.read_h5ad(INPUT_H5AD)

print(f"AnnData: {adata.n_obs:,} spots x {adata.n_vars:,} genes")
print("Available layers:", list(adata.layers.keys()))
print("Using adata.X as the expression matrix.")

if adata.X is None:
    sys.exit("ERROR: adata.X is empty.")

if "spatial" not in adata.uns or SPATIAL_LIBRARY_ID not in adata.uns["spatial"]:
    sys.exit(
        f"ERROR: Expected adata.uns['spatial']['{SPATIAL_LIBRARY_ID}'] "
        "was not found."
    )

spatial = adata.uns["spatial"][SPATIAL_LIBRARY_ID]
if "images" not in spatial or "downscaled_fullres" not in spatial["images"]:
    sys.exit(
        "ERROR: Expected image at "
        "adata.uns['spatial']['ST']['images']['downscaled_fullres'] "
        "was not found."
    )
if "scalefactors" not in spatial:
    sys.exit("ERROR: Spatial scale factors are missing.")

required_obs_cols = [
    "in_tissue",
    "array_row",
    "array_col",
    "pxl_row_in_fullres",
    "pxl_col_in_fullres",
]
missing_obs_cols = [c for c in required_obs_cols if c not in adata.obs.columns]
if missing_obs_cols:
    sys.exit(
        "ERROR: Required coordinate columns are missing from adata.obs: "
        + ", ".join(missing_obs_cols)
    )

# Validate expression matrix values before exporting as counts.
X_input = adata.X
if sparse.issparse(X_input):
    values = X_input.data
else:
    values = np.asarray(X_input).ravel()

if values.size and (
    not np.all(np.isfinite(values))
    or np.any(values < 0)
    or not np.allclose(values, np.round(values))
):
    sys.exit(
        "ERROR: adata.X contains non-integer, negative, or non-finite values. "
        "It may be normalized/transformed data, so it was not exported as counts."
    )

# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

matrix_dir = OUTPUT_DIR / "filtered_feature_bc_matrix"
spatial_dir = OUTPUT_DIR / "spatial"
matrix_dir.mkdir(parents=True, exist_ok=True)
spatial_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# STEP 1: EXPORT EXPRESSION MATRIX
# ============================================================

print("Preparing expression matrix...")
# AnnData matrix is spots x genes. Seurat Matrix Market input is genes x spots.
X = sparse.csr_matrix(X_input).T.tocoo()

matrix_path = matrix_dir / "matrix.mtx"
print(f"Writing matrix: {X.shape[0]:,} genes x {X.shape[1]:,} spots")
mmwrite(matrix_path, X)

with matrix_path.open("rb") as f_in, gzip.open(
    matrix_dir / "matrix.mtx.gz", "wb"
) as f_out:
    while True:
        chunk = f_in.read(8 * 1024 * 1024)
        if not chunk:
            break
        f_out.write(chunk)

matrix_path.unlink()

# Matrix columns follow this barcode order.
pd.Series(adata.obs_names.astype(str)).to_csv(
    matrix_dir / "barcodes.tsv.gz",
    sep="\t",
    index=False,
    header=False,
    compression="gzip",
)

# Use gene IDs from adata.var when available, and var_names as feature names.
if "gene_ids" in adata.var.columns:
    feature_ids = (
    adata.var["gene_ids"]
    .fillna(pd.Series(adata.var_names, index=adata.var.index))
    .astype(str)
    .to_numpy())
else:
    feature_ids = adata.var_names.astype(str).to_numpy()

if "feature_types" in adata.var.columns:
    feature_types = adata.var["feature_types"].fillna("Gene Expression").astype(str).to_numpy()
else:
    feature_types = np.repeat("Gene Expression", adata.n_vars)

features = pd.DataFrame({
    0: feature_ids,
    1: adata.var_names.astype(str),
    2: feature_types,
})
features.to_csv(
    matrix_dir / "features.tsv.gz",
    sep="\t",
    index=False,
    header=False,
    compression="gzip",
)

print("Expression matrix and feature/barcode files exported.")

# ============================================================
# STEP 2: EXPORT DOWNSCALED H&E IMAGE
# ============================================================

print("Exporting downscaled H&E image...")
img = np.asarray(spatial["images"]["downscaled_fullres"])

if img.ndim not in (2, 3):
    sys.exit(f"ERROR: Unsupported image shape: {img.shape}")

if img.dtype != np.uint8:
    if img.size and np.nanmax(img) <= 1:
        img = img * 255
    img = np.clip(np.nan_to_num(img), 0, 255).astype(np.uint8)

Image.fromarray(img).save(spatial_dir / "tissue_lowres_image.png")
print(f"Image dimensions: {img.shape}")

# ============================================================
# STEP 3: EXPORT SPATIAL POSITIONS AND SCALE FACTORS
# ============================================================

print("Exporting spatial positions...")
# Use actual coordinates and array indices already provided in adata.obs.
positions = pd.DataFrame({
    "barcode": adata.obs_names.astype(str),
    "in_tissue": pd.to_numeric(adata.obs["in_tissue"]).astype(int).to_numpy(),
    "array_row": pd.to_numeric(adata.obs["array_row"]).astype(int).to_numpy(),
    "array_col": pd.to_numeric(adata.obs["array_col"]).astype(int).to_numpy(),
    "pxl_row_in_fullres": pd.to_numeric(
        adata.obs["pxl_row_in_fullres"]
    ).to_numpy(),
    "pxl_col_in_fullres": pd.to_numeric(
        adata.obs["pxl_col_in_fullres"]
    ).to_numpy(),
})

positions.to_csv(
    spatial_dir / "tissue_positions_list.csv",
    index=False,
    header=False,
)

sf = spatial["scalefactors"]
required_sf = [
    "spot_diameter_fullres",
    "tissue_downscaled_fullres_scalef",
]
missing_sf = [k for k in required_sf if k not in sf]
if missing_sf:
    sys.exit("ERROR: Missing scale factors: " + ", ".join(missing_sf))

scale_factors = {
    "spot_diameter_fullres": float(sf["spot_diameter_fullres"]),
    "tissue_lowres_scalef": float(sf["tissue_downscaled_fullres_scalef"]),
}
with (spatial_dir / "scalefactors_json.json").open("w") as f:
    json.dump(scale_factors, f, indent=2)

# ============================================================
# SUMMARY
# ============================================================

print("\nExport complete.")
print(f"Output directory: {OUTPUT_DIR.resolve()}")
print(f"Counts matrix: {X.shape[0]:,} genes x {X.shape[1]:,} spots")
print(f"Image: {spatial_dir / 'tissue_lowres_image.png'}")
print(f"Positions: {spatial_dir / 'tissue_positions_list.csv'}")
print(f"Scale factors: {spatial_dir / 'scalefactors_json.json'}")
print(
    "\nIMPORTANT: The integer-valued expression matrix is consistent with raw "
    "counts, but confirm its provenance if required. Validate the spot/image "
    "overlay in Seurat before relying on spatial plots."
)
