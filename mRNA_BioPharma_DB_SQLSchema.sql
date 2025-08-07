-- Create the database
CREATE DATABASE IF NOT EXISTS mRNA_BioPharma_DB;
USE mRNA_BioPharma_DB;

CREATE TABLE Countries (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(100),
    income_level ENUM('Low', 'Middle', 'High'),
    population INT
);

CREATE TABLE Contracts (
    contract_id INT PRIMARY KEY,
    country_id INT,
    contract_date DATE,
    total_doses INT,
    price_per_dose DECIMAL(8,2),
    delivery_start DATE,
    delivery_end DATE,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);

CREATE TABLE Shipments (
    shipment_id INT PRIMARY KEY,
    contract_id INT,
    shipment_date DATE,
    doses_shipped INT,
    batch_id VARCHAR(50),
    FOREIGN KEY (contract_id) REFERENCES Contracts(contract_id)
);

CREATE TABLE Vaccinations (
    vaccination_id INT PRIMARY KEY,
    country_id INT,
    date_administered DATE,
    age_group VARCHAR(20),
    doses_given INT,
    dose_number TINYINT,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);

CREATE TABLE Adverse_Events (
    event_id INT PRIMARY KEY,
    vaccination_id INT,
    event_date DATE,
    severity ENUM('Mild', 'Moderate', 'Severe'),
    event_type VARCHAR(100),
    resolved BOOLEAN,
    FOREIGN KEY (vaccination_id) REFERENCES Vaccinations(vaccination_id)
);

CREATE TABLE Clinical_Trials (
    trial_id INT PRIMARY KEY,
    country_id INT,
    phase ENUM('I', 'II', 'III', 'IV'),
    start_date DATE,
    end_date DATE,
    participants INT,
    efficacy_rate DECIMAL(5,2),
    severe_events INT,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);