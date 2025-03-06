CREATE DATABASE Heatmiser;

USE Heatmiser;

-- Drop tables if they exist
DROP TABLE IF EXISTS TempData;
DROP TABLE IF EXISTS ApiKeys;

-- Create the temperature data table:
-- Stores the minimum temperatue data and Date
CREATE TABLE TempData (
    id INT UNIQUE NOT NULL AUTO_INCREMENT,
    mintemp DOUBLE NOT NULL,
    date_added DATE,
    PRIMARY KEY (id)
);

ALTER TABLE Data AUTO_INCREMENT = 100;

-- Create the API keys table
-- Stores the API key and name data
CREATE TABLE ApiKeys (
    kid INT UNIQUE NOT NULL AUTO_INCREMENT,
    api_key VARCHAR(36) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (kid)
);

ALTER TABLE ApiKeys AUTO_INCREMENT = 100;

-- Test api key, check key data is stored correctly
INSERT INTO ApiKeys (api_key, name)
VALUES ('0f0dg280-7741-7d89-b25b-48ae3c93c29r', 'Testkey');

-- Test temp data, check doubles are handled correctly
INSERT INTO TempData (mintemp)
VALUES(2.5);

DELETE FROM ApiKeys;
DELETE FROM TempData;