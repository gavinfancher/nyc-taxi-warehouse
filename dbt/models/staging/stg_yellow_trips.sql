with source as (

    select * from {{ source('raw', 'yellow_trips') }}

),

renamed as (

    select
        -- ids
        cast(VendorID as int64) as vendor_id,
        cast(RatecodeID as int64) as rate_code_id,
        cast(PULocationID as int64) as pickup_location_id,
        cast(DOLocationID as int64) as dropoff_location_id,
        cast(payment_type as int64) as payment_type_id,

        -- timestamps
        cast(tpep_pickup_datetime as timestamp)  as pickup_datetime,
        cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime,
        cast(tpep_pickup_datetime as date) as pickup_date,

        -- trip details
        cast(passenger_count as int64) as passenger_count,
        cast(trip_distance as numeric) as trip_distance,
        case store_and_fwd_flag
            when 'Y' then true
            when 'N' then false
            else null
        end as store_and_forward_flag,

        -- financials
        cast(fare_amount as numeric) as fare_amount,
        cast(extra as numeric) as extra_charge_amount,
        cast(mta_tax as numeric) as mta_tax_amount,
        cast(tip_amount as numeric) as tip_amount,
        cast(tolls_amount as numeric) as tolls_amount,
        cast(improvement_surcharge as numeric) as improvement_surcharge_amount,
        cast(total_amount as numeric) as total_amount,
        cast(congestion_surcharge as numeric) as congestion_surcharge_amount,
        cast(airport_fee as numeric) as airport_fee_amount

    from source
    where tpep_pickup_datetime is not null
      and tpep_dropoff_datetime is not null

)

select * from renamed
