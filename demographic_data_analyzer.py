import pandas as pd

data_url = 'https://raw.githubusercontent.com/LaurentLabine/fcc_data_analysis_python/main/demographic.csv'

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(data_url)

    df.info()

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df.loc[df['sex'] == "Male","age"].mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(len(df.loc[df['education'] == "Bachelors"].value_counts())/len(df.index)*100,1)

    # What percentage of people with  advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    education_list = ["Bachelors","Masters","Doctorate"]

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df.loc[(df['education'].isin(education_list))]
    
    lower_education = lower_education = df.loc[~(df['education'].isin(education_list))]

    # percentage with salary >50K
    higher_education_rich = round((len(higher_education.loc[higher_education["salary"] == ">50K"])/len(higher_education))*100,1)

     # What percentage of people without advanced education make more than 50K?
    lower_education_rich =  round(len(lower_education.loc[lower_education["salary"] == ">50K"])/len(lower_education)*100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_hours = df.loc[df["hours-per-week"] == df["hours-per-week"].min()]
    rich_percentage = round(len(min_hours.loc[min_hours["salary"] == ">50K"])/len(min_hours)*100,1)

    # What country has the highest percentage of people that earn >50K?
    dfsal = df[["salary", "native-country"]]
    dfsal.loc[dfsal["salary"] == ">50K"].value_counts(normalize=True).max()
    dfref = dfsal["native-country"].value_counts().reset_index()
    dfref.columns = ["native-country","nb"]
    
    total_data_per_countries = dfref.set_index('native-country').T.to_dict("records")[0]
    df_over_50k = dfsal.loc[dfsal["salary"] == ">50K"].value_counts().reset_index()
    del df_over_50k['salary']
    df_over_50k.columns = ["native-country","nb"]
    over_50k = df_over_50k.set_index('native-country').T.to_dict("records")[0]

    res = {}

    for country in total_data_per_countries:
      if(country in over_50k):
        res[country] = over_50k[country]/total_data_per_countries[country]

    new = pd.DataFrame.from_dict(res, orient ='index').reset_index()
    new.columns=["country","wealth-%"]

    highest_earning_country_percentage = round(new.loc[new['wealth-%'].idxmax()].to_dict()["wealth-%"]*100,1)

    highest_earning_country = new.loc[new['wealth-%'].idxmax()].to_dict()["country"]

    # Identify the most popular occupation for those who earn >50K in India.

    india_oc = df.loc[df['native-country'] == "India"]
    india_over_50k = india_oc.loc[india_oc["salary"] == ">50K"]
    india_over_50k_values = india_over_50k["occupation"].value_counts().reset_index()

    top_IN_occupation = india_over_50k_values.loc[india_over_50k_values['occupation'].idxmax(),["index"]].to_dict()["index"]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }