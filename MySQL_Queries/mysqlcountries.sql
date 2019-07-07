-- Written by Todd Enders, 2017
-- 1. What query would you run to get all the countries that speak Slovene?
-- Your query should return the name of the country, language and language percentage.
-- Your query should arrange the result by language percentage in descending order.
SELECT countries.name, languages.language, languages.percentage
FROM countries
	JOIN languages ON countries.id = languages.country_id
WHERE languages.language = 'Slovene'
ORDER BY languages.percentage DESC;

-- 2. What query would you run to display the total number of cities for each country?
-- Your query should return the name of the country and the total number of cities.
-- Your query should arrange the result by the number of cities in descending order.
SELECT countries.name, COUNT(cities.id) as num_cities
FROM countries
	JOIN cities ON countries.id = cities.country_id
GROUP BY countries.id
ORDER BY num_cities DESC;

-- 3. What query would you run to get all the cities in Mexico with a population
-- of greater than 500,000? Your query should arrange the result by population
-- in descending order.
SELECT cities.name, cities.population
FROM countries
	JOIN cities ON countries.id = cities.country_id
WHERE countries.name = 'Mexico' AND cities.population > 500000
ORDER BY cities.population DESC;

-- 4. What query would you run to get all languages in each country with a percentage
-- greater than 89%? Your query should arrange the result by percentage in descending order.
SELECT countries.name, languages.language, languages.percentage
FROM countries
    JOIN languages ON countries.id = languages.country_id
WHERE languages.percentage > 89
ORDER BY languages.percentage DESC;

-- 5. What query would you run to get all the countries with Surface Area below 501 and
-- Population greater than 100,000? (2)
SELECT countries.name, countries.surface_area, countries.population
FROM countries
WHERE countries.surface_area < 501 AND countries.population > 100000;

-- 6. What query would you run to get countries with only Constitutional Monarchy with a
-- capital greater than 200 and a life expectancy greater than 75 years? (1)
SELECT countries.name, countries.government_form, countries.capital
FROM countries
WHERE countries.government_form = 'Constitutional Monarchy'
	AND countries.life_expectancy > 75
	AND countries.capital > 200;

-- 7. What query would you run to get all the cities of Argentina inside the Buenos Aires
-- district and have the population greater than 500, 000? The query should return the
-- Country Name, City Name, District and Population. (2)
SELECT countries.name, cities.name, cities.district, cities.population
FROM countries
	JOIN cities ON countries.id = cities.country_id
WHERE countries.name = 'Argentina'
	AND cities.district = 'Buenos Aires'
	AND cities.population > 500000;

-- 8. What query would you run to summarize the number of countries in each region?
-- The query should display the name of the region and the number of countries.
-- Also, the query should arrange the result by the number of countries in descending order.
SELECT countries.region, COUNT(countries.id) AS num_countries
FROM countries
GROUP BY countries.region
ORDER BY num_countries DESC;