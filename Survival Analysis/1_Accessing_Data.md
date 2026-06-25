# Accessing Survival Data

## Quick intro to survival analysis
[**Survival analysis**](https://numiqo.com/tutorial/survival-analysis) is very important in biomedical research because it allows us to evaluate whether a treatment or condition is associated with better or worse outcomes. In cancer research, it is commonly done to see whether a drug treatment results in better patient survival compared with a control group. It can also be done to see whether patients with a certain gene signature or condition exhibit better survival and outcome.

Typically you will see survival analysis results displayed in a [**Kaplan Meier Curve**](https://numiqo.com/tutorial/kaplan-meier-curve) (image attached below). The x-axis represents time, while the y-axis represents the estimated probability of surviving beyond a given time point. The lower the curve, the lower the percent of surviving patients and thus the worse the outcome. The y-axis value of "estimated survival probability" involves more detailed statistics and math that is not discussed here.


In more "technical" terms, survival analysis is interested in "survival time", defined as the time until an event occurs. In biomedicine, the "event" is most commonly death (often called **"Overall Survival"** (OS)). However, you will encounter some studies that are interested in time until recurrence/relapse of a disease ("Recurrence/Relapse-free survival" (RFS)), progression of a disease to a more severe state ("Progression-Free Survival" (PFS)), and more.

Sometimes, information on "time to outcome" are not available for certain patients. This often occurs because of study limitations (clincal trials do not last forever, and the study may end before patients experience the "event" of interest) or patient circumstances (patient drops out due to private circumstances). This is referred to as [**"censuring"** or "censured data"](https://www.youtube.com/watch?v=XNV3vuDWo-U). The tick marks in the kaplan meier curve displayed above each represent censured individuals: their location along the x-axis shows the last known time point for that patient.

For TCGA survival data, many patients are alive at their last follow-up time. Their exact survival time is unknown, but we know they survived at least until their last follow-up date. The R package for survival analysis will take into consideration censuring!

The types of data needed for survival analysis will be explored in the next section!

## 1. Accessing Survival Data from TCGA (The Cancer Genome Atlas)
Patient clinical data from TCGA can be accessed through the [Genomic Data Commons (GDC) Portal](https://portal.gdc.cancer.gov/), hosted by the National Cancer Institute (NCI).

Once you navigate to the image shown above, click on "Cohort Builder" as circled in red above. Under the "Project" window, after clicking the "+ 85 more" button to expand the selection, scroll down and you will see all the TCGA projects (with the format TCGA-"project abbreviation"). For example, TCGA-HNSC is for Head-Neck Squamous Cell Carcinoma, while TCGA-BRCA is for breast cancer. Click on the check box next to the project you are interested in.

Next, navigate to the "Repository" tab, circled in red above. On the left side you should see a tab for "filters". Scroll down to "Data Category" and click the check mark for "clinical". Then, click "Add All Files to Cart", circled in blue above. 

Finally, navigate to the "Cart" button of the website. Under "File Counts By Project", make sure the patient count is correct for your specific project (TCGA-HNSC should have something like 528 as of 2026). You can then click the dropdown arrow of the "Clinical" button and click the "TSV" option to download the data in the TSV (Tab-Separated Values) format. You have officially downloaded all the clinical information, including survival data, for your TCGA cohort of interest!

## 2. Accessing HPV Status
If you are interested in HPV status of TCGA patients, this can be found from the [cBioPortal](https://www.cbioportal.org/datasets) resource. For each TCGA cohort, HPV data is stored in the "(TCGA, PanCancer Atlas)" datasets from the link above (for example, for HNSC, click on ["Head and Neck Squamous Cell Carcinoma (TCGA, PanCancer Atlas)"](https://www.cbioportal.org/study/summary?id=hnsc_tcga_pan_can_atlas_2018)). Once clicked, go to the "Clincal Data" tab, where HPV status should be displayed under the "Subtype" column. To download this data in TSV format, click on the little cloud button to the left of the search bar.

