drop table if exists Options;
drop table if exists DayOptions;
drop table if exists Listings;
drop table if exists DayListings;


create table Listings(
    ListingID int primary key,
    CarYear int,
    Mileage int,
    Price decimal,
    DaysOnMarket int,
    AccidentCount int,
    OwnerCount int,
    Transmission varchar(255),
    ExteriorColor varchar(255),
    listingdate date,
    model varchar(255),
    insertDate date
);

create table DayListings(
    ListingID int primary key,
    CarYear int,
    Mileage int,
    Price decimal,
    DaysOnMarket int,
    AccidentCount int,
    OwnerCount int,
    Transmission varchar(255),
    ExteriorColor varchar(255),
    model varchar(255)
);


create table Options(
    OptionID int primary key,
    ListingID int,
    Option varchar(255),
    FOREIGN KEY(ListingID) REFERENCES Listings(ListingID)
);

create table DayOptions(
    OptionID SERIAL primary key,
    ListingID int,
    Option varchar(255),
    FOREIGN KEY(ListingID) REFERENCES DayListings(ListingID)
);
--made in heroku postgres 2
create table Regression(
    value var1 int
)
