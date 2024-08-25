CREATE TABLE cameo_codes
(
cameo_code varchar(10),
cameo varchar (255)
);


COPY cameo_codes
FROM 's3://factored-datathon-2024-voyager/docs/cameo_codes.csv'
IAM_ROLE 'arn:aws:iam::975691492030:role/redshift_role'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1
REGION 'us-east-1'; 