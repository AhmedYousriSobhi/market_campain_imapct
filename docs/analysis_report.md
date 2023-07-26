# Fixed Solutions
# Analysis Report: Sports Group Campaign Analysis

## Introduction
The aim of this analysis report is to provide insights into the process of estimating offering time for properties in the context of Fixed Solution's business model. As a company specializing in managing properties for customers, accurately determining the appropriate offering time for properties is crucial for ensuring fair transactions and maintaining competitive advantage in the market.

Estimating the offering time of a properties involves considering various factors, such as the number of bedrooms, the developer of each property, the area in squared meters for the property, The type of property either it is appartment, Villa, or others, the area where the property is located, and the delivery time of each property. By analyzing these factors and the market dynamics, we can develop a robust offering time strategy that aligns with customer expectations and market trends.

In this analysis, we will leverage a comprehensive dataset that includes information about the properties features. It is important to note that there are still missing extra features that would be very informative for our target estimati.

Through this analysis, we aim to gain insights into the key factors influencing property's offering time, identify patterns or trends in the market, and develop a data-driven approach for estimating offering time that aligns with customer expectations and the competitive landscape. By leveraging the power of data science and statistical techniques, we can enhance our decision-making process and optimize our pricing strategy for buying used cars from customers.

The following sections of this report will go into the details of the analysis, including data preprocessing, descriptive statistics, correlation analysis, feature importance, competitor price analysis, provide recommendations based on the findings for the company.

## Data Overview
The analysis is based on given dataset that contains information relevant to estimating the offering time of a property.

The dataset includes the following columns:
| Column | Description|
|--------|------------|
| detailed_property_id | Unique id representing the unit|
| number_of_bedrooms | number of bedrooms per property|
|  finishing_status | The status of each property whether it is (Finished, semi finished, unfinished, furnied).|
| developer_name | Name of the developer.|
| compound_name | Name of the compound.|
| english_area_name | Name of the geographical area.|
| english_prop_type_name | property type |
|down_payment| down payment percentage from the total property. |
|time_to_delivery|delivery date of the property ( in days)|
|offering_time|the time for the property to be sold since offered time ( days)|

## Data Preprocessing
Before conducting the analysis, several preprocessing steps were performed on the dataset. 

These steps included:
- Handling duplicated unique id for property, the dropping of duplicated id, should not be in random, as there are extra dependant features we should take care of them, like making sure we don't drop propety where time to delivery feature is postive, and leave the duplicated one where the feature is negative.
That's why dropping duplicated were handled using filtering according certain values in depondant features.
- Hanlding negative values in time_to_delivery.
- Handling missing values in both numerical and categorical features. 
- Filtering outliers based on relevant features.

## Analysis Insights
#### Analysis: Individual Features Analayis of raw data

![numerical_distplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/60952028-586a-4d69-994b-10bc32dd3c6d)

By analysing the distribution of each of these features [number of bedrooms, unit area, down payment, time to delivery, offering time] by each car, It was identified the following
- There are skewness in {offering_time, time_to_delivery} features.
- Huge outliers in both [unit_area, time_to_delivery].

#### Analysis: Boxplot for each numeric features
Before Cleaning
![numerical_boxplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/1b71f756-cdb4-4c29-abc7-beeda2e9ddea)

After Cleaning
![data_after_remove_outliers_boxplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/883fd4dd-27dc-45db-844d-ba6b2f52ccf5)

#### Analysis: The most common used for property
![finishing_status_countplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/f0f295b3-570e-45b8-b35f-a54dd3cc44a8)

![compound_name_countplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/b6963f71-b803-4372-b737-c1bef4293146)

![developer_name_countplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/037efb4c-ea5f-4bc6-833a-6d912b45ec74)

![english_area_name_countplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/44b36d5e-01ed-49a2-85d5-7de17adc1122)

![english_prop_type_name_countplot](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/b0cd17eb-7b82-4d65-9b7c-c58d750156cc)

There are some important insights we should take care of:
- The customers like to have the property either [unfinshed - finshied] most.
- Top developer names should invest more with are [PHD, MM, D, TMD, RM, OD].
- The most popular compound are [S, B, ZE, J, TC].
- Top 4 Area to target by the Marketing team should be [New Cairo - New Capital City - 6th October City - North Coast].
- The most used property_type are Apartment, so it is recommended for the acquisition team to hunt for more Apartment property.

#### Analysis: Identify the most common property types and their distribution across different areas.
![Most Common property types over area](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/4fe08456-1be3-4896-aa4d-fddbee325266)

Some insights for the businees team:
- Areas like [North Coast, Ain Sokhna], where are used mainly for summer vactions, are full of [Chalet, Twinhouse]
- Main cities like [6th of October City, New Cairo, New Capital City, Mokstakbal City] are mainly occupied by Appartement.
- In New Cairo, where there are set of industrial companies, so most of employees choose to rent Studios, That's the reason for having large percentage of property type "Studio".

So the aquasation team should be more focused on hunting these types of properties depending on each Area.

#### Analysis: The distribution of finishing statuses (finished, semi-finished, unfinished) across different property types.Analyze the distribution of finishing statuses (finished, semi-finished, unfinished) across different property types.
![Finishing status distribution across property](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/412b6e2e-ddd5-4e3f-b5a5-50032fd81f96)

Marketing team should target properties like [Chalet, Office, Clinic] in 'finished' status, in the opposite side, properties like [Apartment, Villa, Retail, Townhouse, Duplex] should be in 'Not finished' status.

#### Analysis: Investigate the relationship between property area (unit_area) and the number of bedrooms to understand the typical size of properties in different categories.
![Relationship between Property Area and Number of Bedrooms](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/e83b7848-d9db-4aab-8206-188764bfa50c)

![Distribution of Property Area for Each Number of Bedrooms](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/d19e34c2-69f0-4093-a8d5-cdffd76406cd)
#### Insights:
- There are postive correlation seen in the relation between property Area & number of bedrooms, as the larger the area, the higher the number of bedroom it has.
- Most of [Offices, Duplex, Retails] have small area, so correspondingly have no bedrooms. Compared to Apartments, which have middle Area size, with around 2 to 4 bedrooms.

To understand Violin plot, there are some aspects to consider:
| Aspect | Description|
|--------|------------|
|Distribution of Data| The width of the violin plot represents the density of data points at different price level. <br/>A wider section indicates a higher concentration of data points, which a narrower section indicates a lower concentration.|
|Median| The white dot within the violin plot represents the median value of the data distribution. <br/>It provides an estimate of the central tendency of the data.|
|Interquartile Range (IQR)| The box inside the violin plot represents the interquartile range, which spans from the 25th precentile (lower quartile) to the 75th precentile (upper quartile) of the data. <br/>It provides information about the spread and variability of the data.|
|Whiskers| The thin lines extending from the box (IQR) represents the data range within a certain threshould of the IQR. <br/>They typically cover a certain percentage of the data, such as 1.5 times the IQR. <br/>Any data points outside the whiskers are considered outliers.|
|Symmetry| The shape of the violin plot can provide insights into the symmetry or skewness of the data distribution. <br/>A symmetric distribution will have similar shapes on both sides of the median, while a skewed distribution will have a longer tail on one side.|

Insights: Using Violin plot tell us the following:
- From distribution of price over car model:
    - The width of each violin indicates the density of area sizes for a particular bedrooms number. A narrorw section in the violin plot like in [4, 5] bedrooms, indicates a more dispersed pricing pattern. A wider section in the violin plot like in [0, 1, 2, 3] indicate a high concentration of properties within a specific area range.
    - The whitedot in the violin plots indicates the median area value (in square Meters) for each car model, which give idea of typical price range. So all models  have similar range of prices, except for "Juke Platinium" has a significantly higher price.
- From distribution of area size over number of bedrooms:
    - The whitedot indicates that, the median area value per each bedrooms numbers is following a rising trend over each increasing bedrooms numbers.
  
From All these insights, they can guide our pricing strategies, We can determine which car models command higher prices due to their perceived value, understand the range of prices that customers are willing to pay for different models, and identify any outliers in the prices.

#### Anlaysis: Evalulate the performance of different developers
![developer Market Acquisition](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/262995c1-1751-4dfe-96fd-052d13570845)


#### Analysis: Features Correlation
![correlation](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/71f1c530-0b4a-49db-8fd5-3a9da6373f63)

## Feature Engineering
Creating additional informative feature will have huge impact in model training process. So the recommened features to engineered are:
| Feature | Description|
|--------|------------|
|number of bedrooms per area| the ratio between number of bedrooms per unit area in square meter. <br/>This give insigts about the luxary in property size.|
| down payment per delivery time|The ratio between number of bedrooms per unit area in square meter.|
|Average delivery time based on Developer|Calculate the average of 'time_to_delivery' based on each property per each Developer.|
|Developer market share over property| Indicate how many percentage in total property does each Developer contributes|
|Developer Performance| Calculate how much percentage each Developer has of property types|
|Average delivery time based on Area|Calculate the average of 'time_to_delivery' based on each property per each Area.|
|Area market share over property| Indicate how many percentage in total property does each area contributes|
|Area Performance| Calculate how much percentage each area has of property types|

## Model Insights
Estimating property offering time is a regression problem, So one of the most powerfull model is XGBOOST Regressor, which was used here in this project.

The overall RMSE were [Training set: 35.07, Validation set: 48.05]

For model tuning and imporvement, A baseline model will be used to be a baseline for each new developed model, and compare the performance.

Notes to be considered for more improvement:
- There are negative values in the prediction model, should be first treated to be at least be zeros.
- During the feature engineering, during calculation the average time_to_delivery per property, there were missing values, which should be imputed.
  - For the current time, it was imputed with -1, which is not accurate, but also can't be filled with zeros.
  - The correct way is to fit linear regressor model, to calculate the appropriate values for the missing values.

Note: 
- As we are dealing with Regression problem, we don't have such Accuracy metric, So Depending on Bussiness, An accuracy metric could be defined as measurable & understandable method.
- A suggested accuracy metric, is depending on relative features, we could calculate the [mean, standard deviation] as a margin for each offering time. So this problem would be converted into classification of whether the prediction are within the margin of true values or not.
  
## Feature Importance
According to the used features after all preprocessing steps inlcuding [feature engineering to create new features, imputing for missing values, scalling for numerical values, one-hot encoding for categorical values], More important features were created.

To get more details regarding the first top 20 features detected by current model.
![feature_importance_v0](https://github.com/AhmedYousriSobhi/aCupOfTea/assets/66730765/d299e48b-f969-4ede-9751-60c31f1eb8c6)

## Recommendations
Based on the analysis conducted, the following recommendations are suggested:
- Regularly monitor and update offering time estimation strategies based on the market trends and developers' performance and delivery time.
- Consider the impact of specific features on property's offering time estimation decisions.
- Continuously collect and analysis data on developers performance and market share, and also each area contribution in each property to maintain a competitive edge.
  
## Conclution
In conclusion, the analysis of the properties dataset has provided valuable insights into property type, number of bedrooms, developer performance and their market share, and areas contribution in each property. These insights can assist the company in making informed decisions regarding estimation of property offering time, inventory management, and understanding customer preferences. It is crucial for the company to leverage these findings to refine its strategies, maximize profitability, and establish a strong foothold in the competitive real state market.