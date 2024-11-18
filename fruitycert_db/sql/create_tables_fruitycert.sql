-- Crea la base de datos y las tablas necesarias para fruitycert
CREATE TABLE Inspection (
    inspection_id SERIAL PRIMARY KEY,
    inspection_date DATE NOT NULL,
    port VARCHAR(255),
    inspector_name VARCHAR(255)
);

CREATE TABLE Pallet (
    pallet_id SERIAL PRIMARY KEY,
    inspection_id INT NOT NULL REFERENCES Inspection(inspection_id),
    farm VARCHAR(255),
    variety VARCHAR(255),
    size VARCHAR(50),
    packing_date DATE,
    grower VARCHAR(255)
);

CREATE TABLE Sample (
    sample_id SERIAL PRIMARY KEY,
    pallet_id INT NOT NULL REFERENCES Pallet(pallet_id),
    quality_score FLOAT,
    condition_score FLOAT
);

CREATE TABLE Parameter (
    parameter_id SERIAL PRIMARY KEY,
    parameter_name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE CustomerAttributes (
    attribute_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    analysis1 VARCHAR(255),
    analysis2 VARCHAR(255),
    analysis3 VARCHAR(255),
    analysis4 VARCHAR(255),
    analysis5 VARCHAR(255)
);

CREATE TABLE Lot (
    lot_id SERIAL PRIMARY KEY,
    lot_name VARCHAR(255)
);

CREATE TABLE LotPallet (
    lot_id INT NOT NULL REFERENCES Lot(lot_id),
    pallet_id INT NOT NULL REFERENCES Pallet(pallet_id),
    PRIMARY KEY (lot_id, pallet_id)
);
