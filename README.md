# nyc-taxi-warehouse

## Data Source

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## Raw Data Definitions

### Rideshare (High Volume FHV) Trip Records

Source: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf

Each row represents a single trip in an FHV dispatched by one of NYC's licensed High Volume FHV bases.

| Field Name | Description |
|---|---|
| hvfhs_license_num | The TLC license number of the HVFHS base or business. HV0002 = Juno, HV0003 = Uber, HV0004 = Via, HV0005 = Lyft |
| dispatching_base_num | The TLC Base License Number of the base that dispatched the trip. |
| originating_base_num | Base number of the base that received the original trip request. |
| request_datetime | Date/time when passenger requested to be picked up. |
| on_scene_datetime | Date/time when driver arrived at the pick-up location (Accessible Vehicles only). |
| pickup_datetime | The date and time of the trip pick-up. |
| dropoff_datetime | The date and time of the trip drop-off. |
| PULocationID | TLC Taxi Zone in which the trip began. |
| DOLocationID | TLC Taxi Zone in which the trip ended. |
| trip_miles | Total miles for passenger trip. |
| trip_time | Total time in seconds for passenger trip. |
| base_passenger_fare | Base passenger fare before tolls, tips, taxes, and fees. |
| tolls | Total amount of all tolls paid in trip. |
| bcf | Total amount collected in trip for Black Car Fund. |
| sales_tax | Total amount collected in trip for NYS sales tax. |
| congestion_surcharge | Total amount collected in trip for NYS congestion surcharge. |
| airport_fee | $2.50 for both drop off and pick up at LaGuardia, Newark, and John F. Kennedy airports. |
| tips | Total amount of tips received from passenger. |
| driver_pay | Total driver pay (not including tolls or tips and net of commission, surcharges, or taxes). |
| shared_request_flag | Did the passenger agree to a shared/pooled ride, regardless of whether they were matched? (Y/N) |
| shared_match_flag | Did the passenger share the vehicle with another passenger who booked separately at any point during the trip? (Y/N) |
| access_a_ride_flag | Was the trip administered on behalf of the Metropolitan Transportation Authority (MTA)? (Y/N) |
| wav_request_flag | Did the passenger request a wheelchair-accessible vehicle (WAV)? (Y/N) |
| wav_match_flag | Did the trip occur in a wheelchair-accessible vehicle (WAV)? (Y/N) |
| cbd_congestion_fee | Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025. |

### Yellow Taxi Trip Records

Source: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

Each row represents a single yellow taxi trip.

| Field Name | Description |
|---|---|
| VendorID | A code indicating the TPEP provider that provided the record. 1 = Creative Mobile Technologies, LLC; 2 = Curb Mobility, LLC; 6 = Myle Technologies Inc; 7 = Helix |
| tpep_pickup_datetime | The date and time when the meter was engaged. |
| tpep_dropoff_datetime | The date and time when the meter was disengaged. |
| passenger_count | The number of passengers in the vehicle. |
| trip_distance | The elapsed trip distance in miles reported by the taximeter. |
| RatecodeID | The final rate code in effect at the end of the trip. 1 = Standard rate; 2 = JFK; 3 = Newark; 4 = Nassau or Westchester; 5 = Negotiated fare; 6 = Group ride; 99 = Null/unknown |
| store_and_fwd_flag | Whether the trip record was held in vehicle memory before sending to the vendor. Y = store and forward trip; N = not a store and forward trip |
| PULocationID | TLC Taxi Zone in which the taximeter was engaged. |
| DOLocationID | TLC Taxi Zone in which the taximeter was disengaged. |
| payment_type | A numeric code signifying how the passenger paid for the trip. 0 = Flex Fare trip; 1 = Credit card; 2 = Cash; 3 = No charge; 4 = Dispute; 5 = Unknown; 6 = Voided trip |
| fare_amount | The time-and-distance fare calculated by the meter. |
| extra | Miscellaneous extras and surcharges. |
| mta_tax | Tax that is automatically triggered based on the metered rate in use. |
| tip_amount | Tip amount. Automatically populated for credit card tips. Cash tips are not included. |
| tolls_amount | Total amount of all tolls paid in trip. |
| improvement_surcharge | Improvement surcharge assessed trips at the flag drop. Began being levied in 2015. |
| total_amount | The total amount charged to passengers. Does not include cash tips. |
| congestion_surcharge | Total amount collected in trip for NYS congestion surcharge. |
| airport_fee | For pick up only at LaGuardia and John F. Kennedy Airports. |
| cbd_congestion_fee | Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025. |