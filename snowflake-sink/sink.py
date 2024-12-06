import snowflake.connector

from quixstreams.sinks import Sink


class SnowflakeSink(Sink):
    def __init__(self, account, user, password, role, warehouse, database, schema, table, logger):
        self.account = account
        self.user = user
        self.password = password
        self.role = role
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.table = table
        self.logger = logger

    def connect(self):
        self.conn = snowflake.connector.connect(
            user=self.user,
            password=self.password,
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
            role=self.role,
        )

    def write(self, batch):
        with self.conn.cursor() as cur:
            for item in batch:
                cur.execute(
                    f"INSERT INTO {self.table} VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (item.key, item.value, item.timestamp, item.headers, item.topic, item.partition, item.offset)
                )