# -------------------------------
# This is the python noteback i will use to analyse questions such as Which locations
#have the highest number of data-related vacancies?

#What is the average advertised salary by job title?

#How does salary vary between London and other UK locations?

#Which Work Model appear most frequently in Analyst vacancies?

#All analysis will be taken from my job_vacancies.csv.
# -------------------------------


# -------------------------------
# Importing Libraries
# -------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("job_vacancies.csv")

# -------------------------------
# DATA CLEANING
# -------------------------------

df.head()
df.info()
print(df.isnull().sum())

df["Salary"]=(df["Salary"].astype(str).str.replace(",","").str.strip().astype(float))
df["Location"]=(df["Location"].astype(str).str.strip())
df["Work model"]=(df["Work model"].astype(str).str.strip())


# -------------------------------
# 1. TOP 10 LOCATIONS
# -------------------------------

location_counts = df.groupby("Location").size().sort_values(ascending=False)
print(location_counts)

plt.figure()

location_counts.head(10).plot(kind="bar")

plt.title("Top 10 Locations by Number of Data Job Vacancies")
plt.xlabel("Location")
plt.ylabel("Number of Vacancies")
plt.xticks(rotation=270)
plt.tight_layout()
plt.show()


# -------------------------------
# 2. AVERAGE SALARY BY JOB TITLE
# -------------------------------
salary_by_title = (
df.groupby("Job title")["Salary"].mean().sort_values(ascending=False))

plt.figure()

salary_by_title.head(10).plot(kind="bar")

plt.title("Average Salary by Job Title")
plt.xlabel("Job Title")
plt.ylabel("Average Salary")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# -------------------------------
# 3. LONDON VS OTHER LOCATIONS
# -------------------------------

df["location_group"] = np.where(
    df["Location"] == "London",
    "London",
    "other"
    )
plt.figure()

df.groupby("location_group")["Salary"].mean().plot(kind="bar")

plt.title("Average Salary: London vs Others")
plt.xlabel("Location")
plt.ylabel("Average Salary")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



# -------------------------------
# 4. WORK MODEL
# -------------------------------

analyst_df=df[df["Job title"].str.contains("Analyst",case=False, na=False)]
frequent_model = analyst_df["Work model"].value_counts()
print(frequent_model)


plt.figure()

frequent_model.plot(kind="bar")
plt.title("Most Frequently Appearing Model")
plt.xlabel("Work Model")
plt.ylabel("Number of Job vacancies")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# -------------------------------
# I have now ansered all the questions specified in the introduction.
#From my analysis using python all the questions have been answered with
#their visualisations.
# -------------------------------

