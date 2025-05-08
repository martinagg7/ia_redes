SELECT
    -- Clave única del paciente
    soc.paciente_id,

    -- Sociodemográficos
    soc.edad, soc.sexo, soc.estado_civil, soc.nivel_educativo, soc.ocupacion,
    soc.region, soc.pais_nacimiento, soc.codigo_postal,

    -- Generales
    genl.fumador, genl.alcohol, genl.actividad_fisica, genl.vive,

    -- Clínicos
    cli.diabetes, cli.hipertension, cli.obesidad, cli.cancer,
    cli.enfermedad_cardiaca, cli.asma, cli.epoc,

    -- Bioquímicos
    bio.glucosa, bio.colesterol, bio.trigliceridos,
    bio.hemoglobina, bio.leucocitos, bio.plaquetas, bio.creatinina,

    -- Genéticos
    gen.mut_BRCA1, gen.mut_TP53, gen.mut_EGFR,
    gen.mut_KRAS, gen.mut_PIK3CA, gen.mut_ALK, gen.mut_BRAF,

    -- Económicos
    eco.ingresos_mensuales, eco.gastos_salud, eco.seguro_salud,
    eco.deudas, eco.tipo_empleo, eco.ayudas_publicas

FROM [DATAEX].[MONGO06_Sociodemograficos] soc
LEFT JOIN [DATAEX].[MONGO05_Generales] genl
    ON soc.paciente_id = genl.paciente_id
LEFT JOIN  [DATAEX].[MONGO02_Clinicos]cli
    ON soc.paciente_id = cli.paciente_id
LEFT JOIN [DATAEX].[MONGO01_Bioquimicos] bio
    ON soc.paciente_id = bio.paciente_id
LEFT JOIN [DATAEX].[MONGO03_Geneticos] gen
    ON soc.paciente_id = gen.paciente_id
LEFT JOIN [DATAEX].[MONGO04_Economicos] eco
    ON soc.paciente_id = eco.paciente_id