from pydantic import BaseModel
from typing import Optional

class WaterBodyCoordinates(BaseModel):
    lat: float
    lon: float

class LandCover(BaseModel):
    Pasture_Hay: Optional[float] = None
    Developed_Low_Intensity: Optional[float] = None
    Open_Water: Optional[float] = None
    Mixed_Forest: Optional[float] = None
    Developed_Open_Space: Optional[float] = None
    Developed_Medium_Intensity: Optional[float] = None
    Grassland_Herbaceous: Optional[float] = None

class CropCover(BaseModel):
    Other_Hay_Non_Alfalfa: Optional[float] = None
    Grassland_Pasture: Optional[float] = None
    Developed_Low_Intensity: Optional[float] = None
    Mixed_Forest: Optional[float] = None
    Open_Water: Optional[float] = None
    Developed_Open_Space: Optional[float] = None
    Deciduous_Forest: Optional[float] = None
    Corn: Optional[float] = None
    Developed_Med_Intensity: Optional[float] = None
    Shrubland: Optional[float] = None
    Soybeans: Optional[float] = None

class Parcel(BaseModel):
    parcel_id: str
    county_id: int
    cty_row_id: int
    county_name: str
    muni_name: str
    state_abbr: str
    county_link: str
    address: str
    addr_number: str
    addr_street_name: str
    addr_street_type: str
    addr_city: str
    addr_zip: str
    census_zip: str
    owner: str
    mail_address1: str
    mail_address3: str
    sale_price: float
    mkt_val_land: float
    mkt_val_bldg: float
    mkt_val_tot: float
    bldg_sqft: int
    year_built: int
    land_use_code: str
    story_height: float
    muni_id: int
    school_district: str
    acreage: float
    acreage_calc: float
    latitude: float
    longitude: float
    acreage_adjacent_with_sameowner: float
    census_block: int
    census_tract: int
    robust_id: str
    elevation: float
    last_updated: str
    mail_addressnumber: str
    mail_streetname: str
    mail_streetnameposttype: str
    mail_placename: str
    mail_statename: str
    mail_zipcode: str
    land_cover: LandCover
    crop_cover: CropCover
    geom_as_wkt: str

