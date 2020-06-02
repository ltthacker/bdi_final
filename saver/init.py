import pymysql

def init(config):
    conn = pymysql.connect(host=config['host'],
                           user=config['user'],
                           password=config['password'],
                           db=config['database'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()

    # drop table if needed
    sql = 'DROP TABLE IF EXISTS news'
    cur.execute(sql)
    conn.commit()

    # alter database to support full utf-8
    sql = 'ALTER DATABASE {} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci'.format(config['database'])
    cur.execute(sql)
    conn.commit()

    # create table
    sql = 'CREATE TABLE news (truth BIT(1), url TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, paragraph TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci)'
    cur.execute(sql)
    sql = 'ALTER TABLE news CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
    cur.execute(sql)
    conn.commit()


