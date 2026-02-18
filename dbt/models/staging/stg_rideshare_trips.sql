with source as (

    select * from {{ source('raw', 'rideshare_trips') }}

),

renamed as (

    select
        -- ids
        cast(hvfhs_license_num as string) as rideshare_license_num,
        cast(dispatching_base_num as string) as dispatching_base_num,
        cast(originating_base_num as string) as originating_base_num,
        cast(PULocationID as int64) as pickup_location_id,
        cast(DOLocationID as int64) as dropoff_location_id,

        -- timestamps
        cast(request_datetime as timestamp) as request_datetime,
        cast(on_scene_datetime as timestamp) as on_scene_datetime,
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropoff_datetime as timestamp) as dropoff_datetime,
        cast(pickup_datetime as date) as pickup_date,

        -- trip details
        cast(trip_miles as numeric) as trip_miles,
        cast(trip_time as int64) as trip_time,
        case shared_request_flag
            when 'Y' then true
            when 'N' then false
            else null
        end as shared_request_flag,
        case shared_match_flag
            when 'Y' then true
            when 'N' then false
            else null
        end as shared_match_flag,
        case access_a_ride_flag
            when 'Y' then true
            when 'N' then false
            else null
        end as access_a_ride_flag,
        case wav_request_flag
            when 'Y' then true
            when 'N' then false
            else null
        end as wav_request_flag,
        case wav_match_flag
            when 'Y' then true
            when 'N' then false
            else null
        end as wav_match_flag,

        -- financials
        cast(base_passenger_fare as numeric) as base_passenger_fare_amount,
        cast(tolls as numeric) as tolls_amount,
        cast(bcf as numeric) as black_car_fund_amount,
        cast(sales_tax as numeric) as sales_tax_amount,
        cast(congestion_surcharge as numeric) as congestion_surcharge_amount,
        cast(airport_fee as numeric) as airport_fee_amount,
        cast(tips as numeric) as tips_amount,
        cast(driver_pay as numeric) as driver_pay_amount

    from source
    where pickup_datetime is not null
      and dropoff_datetime is not null

)

select * from renamed
