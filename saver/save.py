
def save(sqlc, config, table, rdd):
    df = sqlc.createDataFrame(rdd)
    df.write.format('jdbc').options(
            url='jdbc:mysql://localhost/{}'.format(config['database']),
            driver='com.mysql.jdbc.Driver',
            dbtable=table,
            user=config['user'],
            password=config['password'],
            charset='utf8mb4').mode('append').save()

