drop if exists table Listings;
drop if exists table DayListings;

create table Listings{
    ListingID int primary key,
    CarYear int,
    Mileage int,
    Price decimal,
    DaysOnMarket int,
    AccidentCount int,
    OwnerCount int,
    Transmission varchar(255),
    ExteriorColor varchar(255)
};

create table Options{
    OptionID int not null identity(1,1) primary key,
    ListingID int,
    Option varchar(255)
    FOREIGN KEY(ListingID) REFERENCES Listings(ListingID)
};

