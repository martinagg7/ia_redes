/*Para integrar la información de todas las tablas disponibles hacemos  LEFT JOIN
 tomando como tabla base MONGO06_Sociodemograficos, que contiene los datos sociodemográficos de todos los pacientes*/
 
SELECT *
FROM [DATAEX].[MONGO06_Sociodemograficos] soc
LEFT JOIN [DATAEX].[MONGO05_Generales] gen
    ON soc.paciente_id = gen.paciente_id
LEFT JOIN [DATAEX].[MONGO02_Clinicos] cli
    ON soc.paciente_id = cli.paciente_id
LEFT JOIN [DATAEX].[MONGO01_Bioquimicos] bio
    ON soc.paciente_id = bio.paciente_id
LEFT JOIN [DATAEX].[MONGO03_Geneticos] genm
    ON soc.paciente_id = genm.paciente_id
LEFT JOIN [DATAEX].[MONGO04_Economicos] eco
    ON soc.paciente_id = eco.paciente_id