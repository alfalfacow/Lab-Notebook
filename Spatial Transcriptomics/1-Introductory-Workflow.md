# Spatial Transcriptomics
Spatial transcriptomics (ST) is a technique that maps gene expression at (near) single cell resolution onto an intact tissue sample. This is powerful because it preserves spatial information between individual cells, allowing for analysis of cell-cell communication, signaling pathways, and more.

The two main types of ST are imaging based (quantifies gene expression for select genes of interest through the microscope) and sequencing based (quantifies gene expression for many genes through a microarray). Here is a [paper](https://link.springer.com/article/10.1186/s13073-022-01075-1) that explains the exact science behind ST in more detail.

These instructions are a compilation of the common workflow for dealing with sequencing based ST (of the Visium 10x plaform) through the Seurat package in R.

## Table of Contents

1: Data Entry
* 1.1: filtered_feature_bc_matrix.h5 file
* 1.2: .mtx file
* 1.3: .rds file

2: Data Quality Control and Preprocessing
* 2.1: Quality Control
* 2.2: Normalization of Data

3: Optional Visualizations
* 3.1 Gene Expression Visualization
* 3.2: Constructing and Visualizing Gene Scores

4: Cell Clustering and Manual Cell Type Annotation
* 4.1: Dimension Reduction and Clustering
* 4.2: Finding gene markers for each cluster
* 4.3: Manually annotating cell type

## Step 1: Data Entry
First, you will have to install and initialize the Seurat package on an R studio window.
```
install.packages("Seurat")
library(Seurat)
```

Next, you will need to obtain a spatial transcriptomics dataset, either from a publically accessible dataset or one you generated yourself. An example is the [GSE281978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE281978) series from the Gene Expression Omnibus (GEO) for Head and Neck Cancer (HNSC). The dataset can be downloaded as a tar file at the bottom of the page.

NOTE: This page will mostly focus on 10x Genomics Visium spatial transcriptomics datasets.

There are many different data formats for spatial transcriptomics that may be present on GEO or other datasets. We will focus on three different ways that gene expression data is stored

### 1.1: filtered_feature_bc_matrix.h5 file
The most common (in my experience) main output file from a Visium dataset is the filtered_feature_bc_matrix.h5, which contains the gene expression data. However, there are other files that make up the dataset that fully distinguish it as a spatial transcriptomics dataset, including the image file of the tissue sample (a .png file) the coordinates of each Visium "cell spot" (tissue_positions_list.csv), and a "scale factor" file that helps to scale the cell spots and map the coordinates onto the image (scalefactors_json.json).

To read the dataset into Seurat as a Seurat object, the files for EACH specific sample need to be organized in a very specific structure. This specific structure is recognized with Seurat's Load10X_Spatial command.

* (Folder) Sample name
* -> (File) (SampleName)_filtered_feature_bc_matrix.h5
* -> (Folder) (SampleName)
* ->-> (File) tissue_lowres_image.png
* ->-> (File) scalefactors_json.json
* ->-> (File) tissue_positions_list.csv

You may need to manually change the contents and names of the files in order to achieve this structure. Now we are ready to read our data on R studio!

```
#Load in Necessary Packages
library(Seurat)
library(ggplot2)
library(patchwork)
library(tidyverse)
set.seed(123) #Some steps (like UMAP) depend on random number generators, so we should set a seed in order to make our work reproducible! 123 is an arbitrary number and can be anything

data.dir <- "Path/To/The/SampleName/Folder/Containing/Your/Dataset" #ex: /Users/alfred/Desktop/GSM8633891
NameOfSeuratObject <- Load10X_Spatial(data.dir, filename="(SampleName)_filtered_feature_bc_matrix.h5") #filename should be whatever name is in the folder for the feature matrix file
glimpse(HNSCC) #Allows you to look at the type of data included in a Seurat Object

```
### 1.2: .mtx file
Another format for the gene expression matrix is the .mtx format (usually named (sample name)_matrix.mtx; [see this example](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9322957). This requires a slightly different workflow for loading in the data into Seurat: since the Load10X_Spatial command recognizes .h5 files, we have to convert the .mtx file into an .h5 file.

To do this, we will need 3 components from the dataset to make up the .h5 file: "matrix.mtx" (gene expression matrix), "features.tsv" (gene names), and "barcodes.tsv" (name of each spot, labeled with a genetic barcode). We will use the [write10x](https://rdrr.io/bioc/DropletUtils/man/write10xCounts.html) function from the DropletUtils package.

Begin by installing and loading the DropletUtils package from Biocondutor!
```
BiocManager::install("DropletUtils") #install package from Bioconductor
library(DropletUtils) #load package into current R session
```
Then, we need to prepare the necessary files. Move the aforementioned 3 components (matrix.mtx, features.tsv, and barcodes.tsv) into the same folder on your computer. You will need to note the path to this folder (example: this format /home/user/desktop, or something similar. You can find this on a mac by right clicking the folder in your file explorer and holding the option button, then clicking "copy (filename) as pathname".)

Format:
* (Folder) arbitrary_folder_name
* -> (File) matrix.mtx
* -> (File) features.tsv
* -> (File) barcodes.tsv

Next, we can load these files as a "sparse matrix" object without any of the spatial data involved YET, using the Read10X command from Seurat
```
filter_matrix <- Read10X("path/to/arbitrary_folder_name")
```

Then, we use the write10xCounts command to convert this matrix object into a .h5 file format:
```
write10xCounts(
  path = "/path/to/desired/location/filtered_feature_bc_matrix.h5", #this line specifies the path to the folder/location where the .h5 file                                                                         will be made, as well as the name of the .h5 file
  x = filter_matrix, #this is the matrix object we created earlier
  genome = "GRCh38", #current human reference genome used for gene alignment
  type = "HDF5", #this is the type of file we want to make (HDF5 is same as .h5 file format)
  version = "3", #current version of CellRanger
  gene.id = rownames(filter_matrix),
  gene.symbol = rownames(filter_matrix) 
)
```
Now you can use this file to load the data into Seurat using the steps from section 1.1!

You might be wondering: why are there different formats if there are technically able to be interconverted? According to the [CellRanger website](https://www.10xgenomics.com/support/jp/software/cell-ranger/latest/analysis/outputs/cr-outputs-mex-matrices) (a tool from 10X genomics that converts the raw expression data from single cell and spatial transcriptomics pipelines into gene expression matrices), earlier versions of CellRanger (v3 and before) output .mtx, while later versions output the filtered_feature_bc_matrix.h5 file).

### 1.3 .rds file
For GEO datasets this pretty much never appears, but for other public repositories, researchers may choose to save their own Seurat objects as a .rds file. A .rds file stands for "R Data Serialization", with [serialization](https://www.geeksforgeeks.org/r-language/data-serialization-rds-using-r/) defined as "the process of converting complex data structures into an understandable format, suitable for storage and transmission".

To load a .rds file into the environment, simply use the [readRDS()](https://rdrr.io/r/base/readRDS.html) command!
```
readRDS("file_name.rds") #use this if is already within the R studio working directory
readRDS("/path/to/file_name.rds") #use this if the rds file is not within the R studio working directory
```
There is also a .rda format, which can store multiple objects. Load this using the [load() function](https://www.r-bloggers.com/2017/04/load-save-and-rda-files/) (very simple!)
```
load("file.rda")
load("/path/to/file.rda")
```
Again, this format is pretty rare for spatial transcriptomics/visium datasets, but now you will be prepared for it! 

## Step 2: Data Quality Control and Preprocessing
To make sure that our data is high quality, the next steps are to quality control and normalize the data. We want to filter out low quality spots (quality control), including spots with with too little or too many genes detected, or spots with a high proportion of unwanted mitochondrial and ribosomal DNA. We also want to normalize the data to account for "variance in molecular counts" among different spots of the tissue (due to technology imperfections and biological differences). 

### 2.1: Quality Control
The four main metrics commonly controlled are:
1. nFeature_Spatial (number of unique genes detected at each spot, part of Seurat object)
2. nCount_Spatial (number of DNA molecules detected at each spot, part of Seurat object)
3. percent.mt (percent of DNA that is from mitochondria, must be manually calculated)
4. percent.ribo (percent of DNA that is from ribosomes, must be manually calculated

The first two have been stored as part of the meta.data of the Seurat object and do not need to be calculated. However, Seurat does not calculate the last two metrics, so we must do that ourselves:

```
#SeuratObject[[meta.data.column]] accesses or creates a new column in the meta.data section of the Seurat object
#PercentageFeatureSet calculates the percent of all counts that include a certain pattern
#The following code calculates the percent of all counts that belong to mitochondrial DNA (named "MT-XX" or "RPS"/"RPL", apparently Regex notation) and puts it into newly defined meta.data columns

SeuratObject[["percent.mt"]] <- PercentageFeatureSet(object = SeuratObject, pattern = "^MT-")
SeuratObject[["percent.ribo"]] <- PercentageFeatureSet(SeuratObject, pattern = "^RP[SL]")

#Visualize the current distribution of each of these metrics with a violin plot
VlnPlot(
  SeuratObject, features = c("nFeature_Spatial", "nCount_Spatial", "percent.mt", "percent.ribo"), 
  pt.size = 0.1, ncol = 3) & 
  theme(axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank())

#Visualize each metric on the tissue image using the SpatialFeaturePlot() function
SpatialFeaturePlot(
  SeuratObject, features = c("nFeature_Spatial", "nCount_Spatial", "percent.mt", "percent-ribo")) &
  theme(legend.position = "bottom")

```
The violin plots should show that each of these metrics are rather widely distributed, with some points close to 0 and others ranging from 10 thousand for nFeature_Spatial to 40 thousand for nCount_Spatial! Our next step is to filter out low quality points of each of these metrics.

Common thresholds for quality control have been taken from this [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11655296/):
1. nFeature_Spatial less than 200 or greater than 7,500
2. nCount_Spatial less than 250 or greater than 50,000
3. percent.mt > 15%
4. percent.ribo > 40%

```
#Creates a NEW Seurat object as a subset of the original using the subset() function, keeping the features that are NOT part of the exclusion criteria defined above

SeuratObject_Subset <- subset(
  SeuratObject, subset = nFeature_Spatial < 7500 & nFeature_Spatial > 200 &
  nCount_Spatial < 50000 & nCount_Spatial > 250 & percent.mt < 15 & percent.ribo < 40)

#You may plot new violin plots to verify filtering
VlnPlot(
  SeuratObject_subset, features = c("nFeature_Spatial", "nCount_Spatial", "percent.mt", "percent.ribo"), 
  pt.size = 0.1, ncol = 3) & 
  theme(axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank())

```

### Step 2.2: Normalization of Data
As mentioned above, we must account for variance and heterogeneity in our tissue sample. The SCTransform function from Seurat will help us normalize our nCount and nFeature data.

```
SeuratObject_subset <- SCTransform(SeuratObject_subset, assay = "Spatial")

```
Seurat is also used for single cell RNA sequencing analyses, which is why we must specify that our assay is a Spatial (Transcriptomics) assay. The SCTransform function automatically creates a new assay column called SCT. 

After normalization, we can plot our violin plots and spatial feature plots again to verify the process:

```
VlnPlot(HNSCC_subset, features = c("nFeature_SCT", "nCount_SCT"), pt.size = 0.1)
SpatialFeaturePlot(HNSCC_subset, features=c("nFeature_SCT", "nCount_SCT")) + theme(legend.position = "right")

#Tip: If you ever need to check the documentation of each function (I highly recommend it for learning purposes),
#use the function ?(functionName)

```
Yay! Now that normalization is complete, we can now move on to downstream analyses of our spatial transcriptomics dataset.

## Step 3: Some fun visualizations (Optional)
Now that we have filtered and normalized our data, there are some fun visualizations that we can do!

## 3.1: Gene expression visualization
Using the SpatialFeaturePlot function again, we can visualize gene expression on the tissue image itself! It shows up as dots across the surface of the tissue, each representing a spot that was sequenced. The color of each dot represents the expression level of specific genes of interest that you will define, and there will be a "legend" telling you what colors correspond to what expression level.

What does each parameter of the SpatialFeaturePlot do?
features: gene(s) of interest that you define
pt.size.factor: size of the dots on the figure
alpha: opacity of the dot (0 to 1)

You can play around with the parameters and find a good visual balance

```
#Remember we are working with SeuratObject_subset now

#Single gene
SpatialFeaturePlot(SeuratObject_subset, features="geneOfInterest", pt.size.factor = 3, alpha = 1)

#Multiple Genes, creates several side by side plots
SpatialFeaturePlot(SeuratObject_subset, features=c("gene1", "gene2", "gene3"), pt.size.factor = 3, alpha = 1)
```

## 3.2: Constructing gene scores and visualizing it in the tissue
Seurat also has a function called AddModuleScore that allows us to define a set of genes, calculating the average expression of each to "spit" out an overall gene signature score, which is added into the meta.data of your Seurat object. This is especially useful when there is a certain cancer pathway, environment/state, or phenotype that you want to define (such as metastasis or perineural invasion, as for our project).

```
#define list of genes for your gene signature
gene_list <- c("gene1", "gene2","gene3", "gene4", "gene5")

#add gene signature score as meta.data
SeuratObject_subset <- AddModuleScore(SeuratObject_subset, features = list(gene_list), name = "name_of_gene_score") 

#visualize your gene signature score as a feature using SpatialFeaturePlot
SpatialFeaturePlot(SeuratObject_subset, features="name_of_gene_score", pt.size.factor = 3, alpha = 1)

```

## Step 4: Cell clustering and manual cell type annotations 
Gene expression visualization is cool and all, but we want more information! We may know the tissue type (head and neck, lung, breast, etc) of our dataset/sample, but one major goal of spatial transcriptomics analyses is to quantify cell-cell communication. We want to know whether each spot is an immune cell (T cells, B cells, macrophages, etc), stromal cell (fibroblast), or epithelial cancer cell! To do this, we perform dimension reduction and clustering of our data.

### 4.1: Dimension Reduction and Clustering
The following code is from the typical Seurat workflow for ST analyses. I will try and add an explanation for the math behind it later, but for now this code will be functional for our purposes. If you are curious I recommend googling some resources to learn more about PCA/UMAP techniques! 

The end result/goal of cell clustering is a UMAP plot, which clusters similar cells onto 2 axes based on gene expression.

```
#Playing around with the dimensions of PCA/UMAP can result in different clustering algorithms.
SeuratObject_subset <- RunPCA(SeuratObject_subset, assay = "SCT", verbose = FALSE)
SeuratObject_subset <- FindNeighbors(SeuratObject_subset, reduction = "pca", dims = 1:30)
SeuratObject_subset <- FindClusters(SeuratObject_subset, resolution = 0.5, verbose = FALSE) #changing the resolution changes how broadly or specifically the algorithm clusters the cell populations. A low resolution (close to 0) results in very broad clustering (fewer clusters), while high resolution results in very specific clustering (more clusters)
SeuratObject_subset <- RunUMAP(SeuratObject_subset, reduction = "pca", dims = 1:30)

#UMAP plot, using DimPLot()
DimPlot(SeuratObject_subset, reduction = "umap", label = TRUE) 

#Plotting newly clustered cells onto the tissue image based on cluster number, using SpatialDimPlot()
SpatialDimPlot(SeuratObject_subset, label = TRUE, pt.size.factor = 2.5, label.size = 3)

#Table representing the number of cells in each cluster number
table(SeuratObject_subset@active.ident)

```

The UMAP is a rather colorful graph showing populations of clustered cells on a two axis graph (UMAP_1 and UMAP_2). Each cell population that has been clustered together by the algorithm will be a different color and is assigned a different number identity. Each cluster is taken to be a different cell type; this interpretation stems from the fact that cell populations are clustered near each other if they have similar gene expression (similar cell types), and far from others if they have different gene expression profiles (different cell types).

The second figure from the SpatialDimPlot allows us to see how neigboring cells are clustered together on the tissue image.

Now we are ready to assign cell type to each cluster!

### 4.2: Finding gene markers for each population
Seurat has a built in function called "FindMarkers", which allows us to quantify the genes that are most upregulated or downregulated in a specific cluster number, compared to all other clusters. FindMarkers creates a dataframe with information on the genes that are markers, logFC values (quantifying how upregulated/downregulated that marker is compared to other clusters), and p-values.

```
#Replace N with the cluster number. min.pct defines the percent of cells that must express a gene in the cluster before it is taken into account as a marker. YOU WILL HAVE TO RUN THIS LINE ONCE FOR EACH MARKER

clusterN_markers <- FindMarkers(SeuratObject_subset, ident.1 = N, min.pct = 0.25)
head(clusterN_markers, n = 5) #view the first 5 rows of the dataframe

#Visualize expression of a gene in each cluster to verify up/downregulation. After clustering, this plot will automatically split the violin plot, with one plot for each cluster, all shown side by side

VlnPlot(SeuratObject_subset, features = c("gene1", "gene2", "gene3"))

```

### 4.3: Manually annotating cell type
We clustered our cells into similar populations (yay!), but now we have to decide the specific cell type that each cluster represents. One way to do this is to individually look at the strongest markers that were identified, using these markers to guide our manual labeling of each cell type. For example, CD3, CD4 and CD8 are well-established T cell markers, according to this [resource](https://www.antibodies.com/primary-antibodies/cell-markers/immune-cell-markers). There are also automatic computational methods to assign cell types based on a reference dataset, but results are highly variable.

The manual annotation is very subjective and prone to error, but it allows for more control and is informed by known markers. No single technique for annotation is perfect, and unfortunately cell type annotation is one of the more "unstable" aspects of ST analyses.

Once you have looked through the markers dataframe for each cluster, compared the TOP few upregulated markers (high positive Log Fold Change/LogFC value) to known markers, the following code allows you to assign the cell type to each cluster:
```
SeuratObject_subset <- RenameIdents(SeuratObject_subset,
                             "0" = "type0",
                             "1" = "type1",
                             "2" = "type2",
                             "3" = "type3", 
                             "4" = "type4",
                             "5" = "type5",
                             "6" = "type6",
                             "7" = "type7",
                             "8" = "type8")

#Visualize clusters on tissue image again, but this time with cell types annotated
SeuratObject_subset[["cell_types"]] <- Idents(SeuratObject_subset) #creates new meta.data column for cell types
DimPlot(SeuratObject_subset, group.by = "cell_types", raster=FALSE, label=FALSE, cols=my_colors)
```
## Conclusion
Congratulations! With the cell types labeled, there are many other computational tools and packages that will allow for downstream analyses.

After following this workflow, you have successfully:
* Input and preprocessed your spatial transcriptomics dataset as a Seurat object
* Visualized gene expression and gene signatures on the tissue
* Clustered and manually defined cell type populations on the tissue

Feel free to reach out of any of the code does not work as intended! I have also linked some references I used below :)

## References
* [Seurat ST Vignette](https://satijalab.org/seurat/articles/spatial_vignette)
* [Seurat Command List](https://satijalab.org/seurat/articles/essential_commands.html#seurat-standard-worflow)
* [Preprocessing/QC and Normalization](https://yu-tong-wang.github.io/talk/sc_st_data_analysis_R.html#quality-contro)
* [Reading in .mtx files](https://github.com/satijalab/seurat/issues/7157)
* [scRNA seq tutorial](https://bioinformatics.ccr.cancer.gov/docs/singlecell-spatial-2026/IntroSeurat2026/IntroSeurat2026.html)

## Food For Thought
* [Biologists, stop putting UMAP plots in your papers](https://simplystatistics.org/posts/2024-12-23-biologists-stop-including-umap-plots-in-your-papers/)
* [Basic explanation of PCA, t-SNE, UMAP](https://bioconductor.org/books/3.15/OSCA.basic/dimensionality-reduction.html)
* [More on dimensional reduction](https://biostatsquid.com/pca-umap-tsne-comparison/#:~:text=Final%20notes,the%20data%20are%20primarily%20linear.)
* [More on dimensional reduction 2](https://carnotresearch.medium.com/understanding-dimensionality-reduction-pca-vs-t-sne-vs-umap-vs-fit-sne-vs-largevis-vs-laplacian-13d0be9ef7f4)






















