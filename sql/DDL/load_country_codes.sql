CREATE TABLE country_codes
(
country_id int,
country_code varchar(5),
country varchar (100)
);


COPY country_codes
FROM 's3://factored-datathon-2024-voyager/docs/country_list.csv'
IAM_ROLE 'arn:aws:iam::975691492030:role/redshift_role'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1
REGION 'us-east-1'; 