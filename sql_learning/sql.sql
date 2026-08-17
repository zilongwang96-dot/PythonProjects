WITH complaint_data AS (
    SELECT 
        complaints.State,
        YEAR(complaints.Date_received) AS complaint_year,
        COUNT(complaints.complaint_ID) AS complaint_count,
        CASE 
            WHEN YEAR(complaints.Date_received) = '2019' THEN population.2019
            WHEN YEAR(complaints.Date_received) = '2020' THEN population.2020
            WHEN YEAR(complaints.Date_received) = '2021' THEN population.2021
            WHEN YEAR(complaints.Date_received) = '2022' THEN population.2022
            WHEN YEAR(complaints.Date_received) = '2023' THEN population.2023
            WHEN YEAR(complaints.Date_received) = '2024' THEN population.2024
            WHEN YEAR(complaints.Date_received) = '2025' THEN population.2025
        END AS population

    FROM
        complaints

    LEFT JOIN 
        clean_population AS population
    ON population.geographic_area = complaints.State

    GROUP BY 
        complaints.State, 
        YEAR(complaints.Date_received),
        CASE 
            WHEN YEAR(complaints.Date_received) = '2019' THEN population.2019
            WHEN YEAR(complaints.Date_received) = '2020' THEN population.2020
            WHEN YEAR(complaints.Date_received) = '2021' THEN population.2021
            WHEN YEAR(complaints.Date_received) = '2022' THEN population.2022
            WHEN YEAR(complaints.Date_received) = '2023' THEN population.2023
            WHEN YEAR(complaints.Date_received) = '2024' THEN population.2024
            WHEN YEAR(complaints.Date_received) = '2025' THEN population.2025
        END
    )

SELECT 
    State, 
    complaint_year, 
    complaint_count, 
    population, 
    (complaint_count / population) * 100000 AS complaint_per_100k
FROM complaint_data
ORDER BY complaint_per_100k DESC;  

