USE mRNA_BioPharma_DB;

-- 1. Total Contracted Revenue per Country
SELECT country_name, SUM(total_doses * price_per_dose) AS total_revenue
FROM Contracts
JOIN countries_real USING (country_id)
GROUP BY country_name;

-- 2. Dose Delivery Completion Rate per Contract
SELECT contract_id, 
       country_name,
       total_doses,
       SUM(doses_shipped) AS shipped,
       ROUND(SUM(doses_shipped)/total_doses * 100, 2) AS delivery_rate_percent
FROM Contracts
JOIN countries_real USING (country_id)
JOIN Shipments USING (contract_id)
GROUP BY contract_id, country_name, total_doses;

-- 3. Country-Level Vaccination Uptake
SELECT c.country_name,
       SUM(v.doses_given) AS total_doses_administered,
       c.population,
       ROUND(SUM(v.doses_given)/c.population * 100, 2) AS coverage_percent
FROM Vaccinations v
JOIN countries_real c USING (country_id)
GROUP BY c.country_name, c.population;

-- 4. Severe Adverse Events per Million Doses
SELECT 
  c.country_name,
  COUNT(CASE WHEN severity = 'Severe' THEN 1 END) AS severe_events,
  SUM(v.doses_given) AS total_doses,
  ROUND(COUNT(CASE WHEN severity = 'Severe' THEN 1 END)/SUM(v.doses_given) * 1000000, 2) AS events_per_million
FROM Adverse_Events a
JOIN Vaccinations v USING (vaccination_id)
JOIN countries_real c ON v.country_id = c.country_id
GROUP BY c.country_name;

-- 5. Top 5 Countries by Revenue
SELECT c.country_name, SUM(total_doses * price_per_dose) AS revenue
FROM Contracts
JOIN countries_real c USING (country_id)
GROUP BY c.country_name
ORDER BY revenue DESC
LIMIT 5;

-- 6. Average Efficacy Rate by Trial Phase
SELECT phase, ROUND(AVG(efficacy_rate), 2) AS avg_efficacy
FROM Clinical_Trials
GROUP BY phase;

-- 7. Trial Participants by Income Level
SELECT income_level, SUM(participants) AS total_participants
FROM Clinical_Trials
JOIN countries_real USING (country_id)
GROUP BY income_level;

-- 8. Top 5 Busiest Vaccination Days
SELECT date_administered, SUM(doses_given) AS total_given
FROM Vaccinations
GROUP BY date_administered
ORDER BY total_given DESC
LIMIT 5;

-- 9. Country with Highest Dose Wastage
SELECT country_name,
       SUM(doses_shipped) AS delivered,
       SUM(doses_given) AS administered,
       SUM(doses_shipped) - SUM(doses_given) AS wasted,
       ROUND((SUM(doses_shipped) - SUM(doses_given))/SUM(doses_shipped) * 100, 2) AS wastage_rate
FROM countries_real
JOIN Contracts USING (country_id)
JOIN Shipments USING (contract_id)
JOIN Vaccinations USING (country_id)
GROUP BY country_name
ORDER BY wastage_rate DESC
LIMIT 1;

-- 10. Contracts by Delivery Window
SELECT contract_id, country_name,
       DATEDIFF(delivery_end, delivery_start) AS delivery_days
FROM Contracts
JOIN countries_real USING (country_id)
ORDER BY delivery_days DESC;

-- 11. Age Group Distribution of Doses
SELECT age_group, SUM(doses_given) AS total_given
FROM Vaccinations
GROUP BY age_group
ORDER BY total_given DESC;

-- 12. Adverse Events Resolved Rate
SELECT country_name,
       COUNT(*) AS total_events,
       SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END) AS resolved_events,
       ROUND(SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END)/COUNT(*) * 100, 2) AS resolved_percent
FROM Adverse_Events
JOIN Vaccinations USING (vaccination_id)
JOIN countries_real ON Vaccinations.country_id = countries_real.country_id
GROUP BY country_name;

-- 13. Contracts Exceeding $50M
SELECT contract_id, country_name, total_doses * price_per_dose AS contract_value
FROM Contracts
JOIN countries_real USING (country_id)
WHERE total_doses * price_per_dose > 50000000;

-- 14. Monthly Vaccine Shipments
SELECT DATE_FORMAT(shipment_date, '%Y-%m') AS shipment_month, SUM(doses_shipped) AS total_shipped
FROM Shipments
GROUP BY shipment_month
ORDER BY shipment_month;

-- 15. Highest Efficacy Trial by Country
SELECT country_name, trial_id, efficacy_rate
FROM Clinical_Trials
JOIN countries_real USING (country_id)
ORDER BY efficacy_rate DESC
LIMIT 1;

-- 16. Adverse Event Rate by Vaccine Dose Number
SELECT dose_number,
       COUNT(a.event_id) AS event_count,
       SUM(v.doses_given) AS total_doses,
       ROUND(COUNT(a.event_id)/SUM(v.doses_given) * 1000000, 2) AS events_per_million
FROM Adverse_Events a
JOIN Vaccinations v USING (vaccination_id)
GROUP BY dose_number;

-- 17. Median Contract Price per Dose by Income Level
SELECT income_level, MEDIAN(price_per_dose) AS median_price
FROM Contracts
JOIN countries_real USING (country_id)
GROUP BY income_level;

-- 18. Severe Events per Clinical Trial Phase
SELECT phase, SUM(severe_events) AS total_severe_events
FROM Clinical_Trials
GROUP BY phase;

-- 19. Contracts Signed per Year
SELECT YEAR(contract_date) AS year, COUNT(*) AS contracts_signed
FROM Contracts
GROUP BY year
ORDER BY year;

-- 20. Top 3 Countries by Public Health Coverage
SELECT country_name,
       SUM(doses_given) AS total_doses,
       population,
       ROUND(SUM(doses_given)/population * 100, 2) AS coverage
FROM countries_real
JOIN Vaccinations USING (country_id)
GROUP BY country_name, population
ORDER BY coverage DESC
LIMIT 3;

/******************
21–40: Stored Views, Procedures, and Functions
******************/

-- 21. VIEW: Vaccination counts per country
CREATE VIEW CountryVaccinationStats AS
SELECT c.country_name, COUNT(*) AS total_vaccinations
FROM Vaccinations vx
JOIN countries_real c ON vx.country_id = c.country_id
GROUP BY c.country_name;

-- 22. VIEW: Adverse events summary by severity
CREATE VIEW AdverseEventSeveritySummary AS
SELECT severity, COUNT(*) AS event_count
FROM Adverse_Events
GROUP BY severity;

-- 23. VIEW: Population coverage percent by country
CREATE VIEW CountryCoveragePercent AS
SELECT c.country_name, ROUND(COUNT(vx.vaccination_id) / p.population_total * 100, 2) AS coverage_percent
FROM Vaccinations vx
JOIN populations p ON vx.country_id = p.country_id
JOIN countries_real c ON vx.country_id = c.country_id
GROUP BY c.country_name;

-- 24. PROCEDURE: Get vaccine sales revenue by country
DELIMITER $$
CREATE PROCEDURE CountryRevenueReport(IN InputCountry VARCHAR(100))
BEGIN
  SELECT c.country_name, SUM(v.price_usd) AS revenue
  FROM Vaccinations vx
  JOIN countries_real c ON vx.country_id = c.country_id
  JOIN vaccines v USING(vaccination_id)
  WHERE c.country_name = InputCountry
  GROUP BY c.country_name;
END $$
DELIMITER ;

-- 25. PROCEDURE: List recent adverse events for a vaccine
DELIMITER $$
CREATE PROCEDURE RecentAdverseEvents(IN VaccineID INT)
BEGIN
  SELECT ae.event_id, ae.event_type, ae.severity, ae.event_date
  FROM Adverse_Events ae
  JOIN Vaccinations vx USING(vaccination_id)
  WHERE vx.vaccination_id = VaccineID
  ORDER BY ae.event_date DESC
  LIMIT 10;
END $$
DELIMITER ;

-- 26. PROCEDURE: AgeGroupReport
DELIMITER $$
CREATE PROCEDURE AgeGroupReport(IN ageGrp VARCHAR(20))
BEGIN
    SELECT v.date_administered, v.doses_given, c.country_name
    FROM Vaccinations v
    JOIN countries_real c ON v.country_id = c.country_id
    WHERE v.age_group = ageGrp;
END $$
DELIMITER ;

-- 27. FUNCTION: Calculate adverse event rate per 100k doses
DELIMITER $$
CREATE FUNCTION AdverseEventRatePer100k(VaxID INT)
RETURNS DECIMAL(10,2)
READS SQL DATA
BEGIN
  DECLARE event_count INT;
  DECLARE dose_count INT;
  SELECT COUNT(*) INTO event_count
  FROM Adverse_Events ae
  JOIN Vaccinations vx USING(vaccination_id)
  WHERE vx.vaccination_id = VaxID;

  SELECT COUNT(*) INTO dose_count
  FROM Vaccinations
  WHERE vaccination_id = VaxID;

  RETURN ROUND(event_count / dose_count * 100000, 2);
END $$
DELIMITER ;

-- 28. FUNCTION: Get country vaccination rate
DELIMITER $$
CREATE FUNCTION CountryVaccinationRate(CID INT)
RETURNS DECIMAL(5,2)
READS SQL DATA
BEGIN
  DECLARE total_pop INT;
  DECLARE vax_count INT;

  SELECT population_total INTO total_pop FROM populations WHERE country_id = CID;
  SELECT COUNT(*) INTO vax_count FROM Vaccinations WHERE country_id = CID;

  RETURN ROUND(vax_count / total_pop * 100, 2);
END $$
DELIMITER ;

-- 29. FUNCTION: GetVaccinationCountByCountry
DELIMITER $$
CREATE FUNCTION GetVaccinationCountByCountry(country INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE count_vx INT;
    SELECT COUNT(*) INTO count_vx FROM Vaccinations WHERE country_id = country;
    RETURN count_vx;
END $$
DELIMITER ;

-- 1️⃣ Create the new table
CREATE TABLE countries_real (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    population BIGINT,
    income_level VARCHAR(50),
    region VARCHAR(50)
);

-- 2️⃣ Insert your real-world data
INSERT INTO countries_real (country_id, country_name, population, income_level, region)
VALUES
    (1, 'United States', 331002651, 'High income', 'North America'),
    (2, 'Germany', 83783942, 'High income', 'Europe'),
    (3, 'India', 1380004385, 'Lower middle income', 'Asia'),
    (4, 'Brazil', 212559417, 'Upper middle income', 'South America'),
    (5, 'South Africa', 59308690, 'Upper middle income', 'Africa');

-- 3️⃣ Drop foreign key constraints in dependent tables
ALTER TABLE Contracts DROP FOREIGN KEY contracts_ibfk_1;
ALTER TABLE Vaccinations DROP FOREIGN KEY vaccinations_ibfk_1;
ALTER TABLE Clinical_Trials DROP FOREIGN KEY clinical_trials_ibfk_1;
ALTER TABLE Shipments DROP FOREIGN KEY shipments_ibfk_1;
ALTER TABLE Adverse_Events DROP FOREIGN KEY adverse_events_ibfk_1;

-- 4️⃣ Recreate foreign keys to point to countries_real
ALTER TABLE Contracts
ADD CONSTRAINT contracts_ibfk_1
FOREIGN KEY (country_id) REFERENCES countries_real(country_id);

ALTER TABLE Vaccinations
ADD CONSTRAINT vaccinations_ibfk_1
FOREIGN KEY (country_id) REFERENCES countries_real(country_id);

ALTER TABLE Clinical_Trials
ADD CONSTRAINT clinical_trials_ibfk_1
FOREIGN KEY (country_id) REFERENCES countries_real(country_id);

ALTER TABLE Shipments
ADD CONSTRAINT shipments_ibfk_1
FOREIGN KEY (country_id) REFERENCES countries_real(country_id);

ALTER TABLE Adverse_Events
ADD CONSTRAINT adverse_events_ibfk_1
FOREIGN KEY (country_id) REFERENCES countries_real(country_id);
