import json
import logging
from typing import Optional

import aiosqlite
import pandas as pd

from terminal_colors import TerminalColors as tc
from utilities import Utilities

DATA_BASE = "database/contoso-sales.db"

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class SalesData:
    conn: Optional[aiosqlite.Connection]

    def __init__(self: "SalesData", utilities: Utilities) -> None:
        self.conn = None
        self.utilities = utilities

    async def connect(self: "SalesData") -> None:
        db_uri = f"file:{self.utilities.shared_files_path}/{DATA_BASE}?mode=ro"

        try:
            self.conn = await aiosqlite.connect(db_uri, uri=True)
            logger.debug("Database connection opened.")
        except aiosqlite.Error as e:
            logger.exception("An error occurred", exc_info=e)
            self.conn = None

    async def close(self: "SalesData") -> None:
        if self.conn:
            await self.conn.close()
            logger.debug("Database connection closed.")

    async def _get_table_names(self: "SalesData") -> list:
        """Return a list of table names."""
        table_names = []
        async with self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';") as tables:
            return [table[0] async for table in tables if table[0] != "sqlite_sequence"]

    async def _get_column_info(self: "SalesData", table_name: str) -> list:
        """Return a list of tuples containing column names and their types."""
        column_info = []
        async with self.conn.execute(f"PRAGMA table_info('{table_name}');") as columns:
            # col[1] is the column name, col[2] is the column type
            return [f"{col[1]}: {col[2]}" async for col in columns]

    async def _get_regions(self: "SalesData") -> list:
        """Return a list of unique regions in the database."""
        async with self.conn.execute("SELECT DISTINCT region FROM sales_data;") as regions:
            result = await regions.fetchall()
        return [region[0] for region in result]

    async def _get_product_types(self: "SalesData") -> list:
        """Return a list of unique product types in the database."""
        async with self.conn.execute("SELECT DISTINCT product_type FROM sales_data;") as product_types:
            result = await product_types.fetchall()
        return [product_type[0] for product_type in result]

    async def _get_product_categories(self: "SalesData") -> list:
        """Return a list of unique product categories in the database."""
        async with self.conn.execute("SELECT DISTINCT main_category FROM sales_data;") as product_categories:
            result = await product_categories.fetchall()
        return [product_category[0] for product_category in result]

    async def _get_reporting_years(self: "SalesData") -> list:
        """Return a list of unique reporting years in the database."""
        async with self.conn.execute("SELECT DISTINCT year FROM sales_data ORDER BY year;") as reporting_years:
            result = await reporting_years.fetchall()
        return [str(reporting_year[0]) for reporting_year in result]

    async def get_database_info(self: "SalesData") -> str:
        """Return a string containing the database schema information and common query fields."""
        table_dicts = []
        for table_name in await self._get_table_names():
            columns_names = await self._get_column_info(table_name)
            table_dicts.append(
                {"table_name": table_name, "column_names": columns_names})

        database_info = "\n".join(
            [
                f"Table {table['table_name']} Schema: Columns: {', '.join(table['column_names'])}"
                for table in table_dicts
            ]
        )
        regions = await self._get_regions()
        product_types = await self._get_product_types()
        product_categories = await self._get_product_categories()
        reporting_years = await self._get_reporting_years()

        database_info += f"\nRegions: {', '.join(regions)}"
        database_info += f"\nProduct Types: {', '.join(product_types)}"
        database_info += f"\nProduct Categories: {', '.join(product_categories)}"
        database_info += f"\nReporting Years: {', '.join(reporting_years)}"
        database_info += "\n\n"

        return database_info

    async def async_fetch_sales_data_using_sqlite_query(self: "SalesData", sqlite_query: str) -> str:
        """
        この関数は、データベースに対して SQLite クエリを実行することにより、Contoso の売上データに関するユーザーの質問に答えるために使用されます。

        :param sqlite_query: 入力は、ユーザーの質問に基づいて情報を抽出するための、整ったフォーマットの SQLite クエリである必要があります。クエリ結果は JSON オブジェクトとして返されます。
        :return: JSON シリアライズ可能な形式でデータを返します。
        :rtype: str
        """

        print(
            f"\n{tc.BLUE}Function Call Tools: async_fetch_sales_data_using_sqlite_query{tc.RESET}\n")
        print(f"{tc.BLUE}Executing query: {sqlite_query}{tc.RESET}\n")

        try:
            # Perform the query asynchronously
            async with self.conn.execute(sqlite_query) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0]
                           for description in cursor.description]

            if not rows:  # No need to create DataFrame if there are no rows
                return json.dumps("The query returned no results. Try a different question.")
            data = pd.DataFrame(rows, columns=columns)
            return data.to_json(index=False, orient="split")

        except Exception as e:
            return json.dumps({"SQLite query failed with error": str(e), "query": sqlite_query})
