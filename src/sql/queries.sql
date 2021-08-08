-- See what categories of crime were committed by Asian-Americans
-- disproportionate to percentage of population
SELECT offenses, percent_asian_pop, percent_asian_crimes, year
FROM race_data
WHERE percent_asian_crimes > percent_asian_pop;

-- Get series of years from least to most occurrences of violent crime
SELECT year
FROM age_data
WHERE offenses = "Violent Crime Index"
ORDER BY all_ages;

-- Get average commission of burglary by age group
SELECT offenses, avg(0_to_17), avg(18_and_older), avg(10_to_17), avg(0_to_14),
avg(15_to_17), avg(18_to_20), avg(21_to_24), avg(25_and_older)
FROM age_data
WHERE offenses = "Burglary";
