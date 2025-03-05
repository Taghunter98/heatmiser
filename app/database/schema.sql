CREATE DATABASE Heatmiser;

USE heatmiser;

CREATE TABLE Data (
    id INT UNIQUE NOT NULL AUTO_INCREMENT=100,
    mintemp INT NOT NULL,
    date_added DATE,
    PRIMARY KEY (id)
)