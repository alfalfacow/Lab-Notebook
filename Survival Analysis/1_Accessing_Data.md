# Accessing Survival Data

## Quick intro to survival analysis
[Survival analysis](https://numiqo.com/tutorial/survival-analysis) is very important in biomedical research because it allows us to evaluate whether a treatment or condition is associated with better or worse outcomes. In cancer research, it is commonly done to see whether a drug treatment results in better patient survival compared with a control group. It can also be done to see whether patients with a certain gene signature or condition exhibit better survival and outcome.

Typically you will see survival analysis results displayed in a [Kaplan Meier Curve](https://numiqo.com/tutorial/kaplan-meier-curve) (image attached below). The x-axis represents time, while the y-axis represents the estimated probability of surviving beyond a given time point. The lower the curve, the lower the percent of surviving patients and thus the worse the outcome. The y-axis value of "estimated survival probability" involves more detailed statistics and math that is not discussed here.

In more "technical" terms, survival analysis is interested in "survival time", defined as the time until an event occurs. In biomedicine, the "event" is most commonly death (often called "Overall Survival"). However, you will encounter some studies that are interested in time until recurrence/relapse of a disease ("Recurrence/Relapse-free survival"), progression of a disease to a more severe state ("Progression-Free Survival"), and more.

Sometimes, information on "time to outcome" are not available for certain patients. This often occurs because of study limitations (clincal trials do not last forever, and the study may end before patients experience the "event" of interest) or patient circumstances (patient drops out due to private circumstances). This is referred to as ["censorship" or "censured data"](https://www.youtube.com/watch?v=XNV3vuDWo-U). For TCGA survival data, many patients are alive at their last follow-up time. Their exact survival time is unknown, but we know they survived at least until their last follow-up date. The R package for survival analysis will take into consideration censuring!

## Accessing Survival Data from TCGA

## Accessing HPV Status

## Accessing mRNA Expression data
