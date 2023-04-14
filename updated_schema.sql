CREATE DATABASE test_db;
\c test_db

CREATE TABLE "User" (
    User_ID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    UserType VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE agents (
    agent_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES "User"(User_ID) ON DELETE SET NULL,
    job_title VARCHAR(255) NOT NULL,
    real_estate_agency VARCHAR(255) NOT NULL,
    contact_information VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);


CREATE TABLE renters (
    renter_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES "User"(User_ID) ON DELETE SET NULL,
    order_date DATE NOT NULL,
    delivery_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    email VARCHAR(255) NOT NULL,
    rental_preferences TEXT NOT NULL
);


CREATE TABLE address (
    address_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "User"(user_id),
    address TEXT NOT NULL,
    state VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zip_code VARCHAR(255) NOT NULL
);


CREATE TABLE neighborhood (
    neighborhood_id SERIAL PRIMARY KEY,
    location TEXT NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    crime_rate INTEGER NOT NULL 
);



CREATE TABLE property (
    property_id SERIAL PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    location TEXT NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL NOT NULL,
    availability BOOLEAN NOT NULL,
    neighborhood_id INTEGER NOT NULL REFERENCES neighborhood(neighborhood_id),
    agent_id INTEGER NOT NULL REFERENCES agents(agent_id)
);


CREATE TABLE house (
    house_id SERIAL PRIMARY KEY,
    property_id INTEGER UNIQUE REFERENCES property(property_id) ON DELETE SET NULL,
    number_of_rooms INTEGER NOT NULL,
    square_footage DECIMAL NOT NULL,
    location TEXT NOT NULL
);


CREATE TABLE apartment (
    apartment_id SERIAL PRIMARY KEY,
    property_id INTEGER UNIQUE NOT NULL REFERENCES property(property_id) ON DELETE SET NULL,
    building_type VARCHAR(255) NOT NULL,
    number_of_rooms INTEGER NOT NULL,
    square_footage DECIMAL NOT NULL
);


CREATE TABLE commercial_building (
    commercial_building_id SERIAL PRIMARY KEY,
    property_id INTEGER UNIQUE NOT NULL REFERENCES property(property_id),
    business_type VARCHAR(255) NOT NULL,
    square_footage DECIMAL NOT NULL
);


CREATE TABLE vacation_home (
    vacation_home_id SERIAL PRIMARY KEY,
    property_id INTEGER UNIQUE NOT NULL REFERENCES property(property_id),
    number_of_rooms INTEGER NOT NULL,
    square_footage DECIMAL NOT NULL
);


CREATE TABLE land (
    land_id SERIAL PRIMARY KEY,
    property_id INTEGER UNIQUE NOT NULL REFERENCES property(property_id),
    area DECIMAL NOT NULL
);


CREATE TABLE CreditCard (
    Credit_CardID SERIAL PRIMARY KEY,
    Renter_ID INTEGER NOT NULL REFERENCES Renters(Renter_ID),
    CardNumber VARCHAR(255) NOT NULL,
    ExpirationDate DATE NOT NULL,
    PaymentAddress_ID INTEGER NOT NULL REFERENCES Address(Address_ID),
    CVV VARCHAR(255) NOT NULL
);


CREATE TABLE Payment (
    payment_id SERIAL PRIMARY KEY,
    payment_status VARCHAR(255) NOT NULL,
    Credit_card_ID INTEGER UNIQUE NOT NULL REFERENCES CreditCard(Credit_CardID),
    Renter_ID INTEGER NOT NULL REFERENCES Renters(Renter_ID),
    PropertyID INTEGER NOT NULL REFERENCES Property(Property_ID),
    Agent_ID INTEGER NOT NULL REFERENCES Agents(Agent_ID),
    Date DATE NOT NULL,
    Payment_amount NUMERIC(10, 2) NOT NULL
);



CREATE TABLE PropertyBooking (
    PropertyBookingID SERIAL PRIMARY KEY,
    Renter_ID INTEGER NOT NULL REFERENCES Renters(Renter_ID),
    PropertyID INTEGER NOT NULL REFERENCES Property(Property_ID),
    CreditCardID INTEGER NOT NULL REFERENCES CreditCard(Credit_CardID),
    desired_move_in_date DATE NOT NULL,
    BillingAddress_ID INTEGER NOT NULL REFERENCES Address(Address_ID),
    budget NUMERIC(10, 2) NOT NULL,
    AgentID INTEGER NOT NULL REFERENCES Agents(Agent_ID)
);


CREATE TABLE RewardProgram (
    RewardProgramID SERIAL PRIMARY KEY,
    RenterID INTEGER NOT NULL REFERENCES Renters(Renter_ID),
    RewardPoints INTEGER NOT NULL,
    PropertyID INTEGER NOT NULL REFERENCES Property(Property_ID),
    Date_of_Reward DATE NOT NULL
);


CREATE TABLE School (
    SchoolID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    State VARCHAR(255) NOT NULL,
    NeighborhoodID INTEGER UNIQUE NOT NULL REFERENCES Neighborhood(Neighborhood_ID)
);

