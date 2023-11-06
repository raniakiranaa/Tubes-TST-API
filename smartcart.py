from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import mysql.connector
from mysql.connector import errorcode
from collections import defaultdict, Counter

config = {
	'host':'cartdb.mysql.database.azure.com',
	'user':'sasi',
	'password':'rania#15',
	'database':'cartdb',
	'client_flags': [mysql.connector.ClientFlag.SSL],
	'ssl_ca': './ssl/DigiCertGlobalRootCA.crt (2).pem'
}

try:
	conn = mysql.connector.connect(**config)
	print("Connection established")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with the user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	app = FastAPI()
   
	@app.get('/product')
	async def read_all_product():
		cursor = conn.cursor()
		query = ("SELECT * FROM product")
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()
		return result
	
	@app.get('/product/{name_product}')
	async def search_info_product(name_product: str):
		cursor = conn.cursor()
		query = f"SELECT * FROM product join aisle on product.id_aisle = aisle.id WHERE name_product = '{name_product}'"
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()

		if result:
			aisle_name = result[0][8]
			aisle_num = result[0][9]
			response = f"{name_product} is in aisle {aisle_num} - {aisle_name}\n"
			
			for item in result:
				merk = item[4]
				price = item[2]
				stock = item[5]
				if stock > 0:
					response += f" {stock} items are available with merk {merk} for Rp.{price}\n"
			
			return response
		else:
			raise HTTPException(status_code=404, detail=f"No information found for product: {name_product}")

	@app.get('/aisle/{name}')
	async def get_products_by_aisle(name: str):
		cursor = conn.cursor()
		query = f"SELECT id FROM aisle WHERE name = '{name}'"
		cursor.execute(query)
		aisle_id = cursor.fetchone()
		if aisle_id:
			aisle_id = aisle_id[0]
			query = f"SELECT DISTINCT name_product FROM product WHERE id_aisle = {aisle_id}"
			cursor.execute(query)
			products = cursor.fetchall()
			cursor.close
			return f"Products in aisle {name}: {[product[0] for product in products]}"
		else:
			cursor.close()
			raise HTTPException(status_code=404, detail=f"No information found for aisle {name}")

	@app.get('/category/{name}')
	async def get_products_by_category(name: str):
		cursor = conn.cursor()
		query = f"SELECT id FROM category WHERE name = '{name}'"
		cursor.execute(query)
		category_id = cursor.fetchone()
		if category_id:
			category_id = category_id[0]
			query = f"SELECT DISTINCT name_product FROM product WHERE id_category = {category_id}"
			cursor.execute(query)
			products = cursor.fetchall()
			cursor.close
			return f"Products in category {name}: {[product[0] for product in products]}"
		else:
			cursor.close()
			raise HTTPException(status_code=404, detail=f"No information found for category {name}")

	@app.get('/detail_transaction/')
	async def get_information_transaction(name_product: Optional[str] = Query(None)):
		cursor = conn.cursor()
		if name_product:
			query = f"SELECT * FROM product WHERE name_product = '{name_product}'"
			cursor.execute(query)
			result = cursor.fetchall()
			if result:
				query = f"SELECT name_product, merk, SUM(quantity) as total FROM detail_transaction JOIN product ON detail_transaction.id_product = product.id WHERE name_product = '{name_product}' GROUP BY name_product, merk ORDER BY total DESC"
				cursor.execute(query)
				result = cursor.fetchall()
				cursor.close()

				if result:
					fav_merk = result[0][1]
					return f"The most bought merk for product {name_product} is {fav_merk}"
				else:
					raise HTTPException(status_code=404, detail=f"No transaction found for product: {name_product}")
			else:
				cursor.close()
				raise HTTPException(status_code=404, detail=f"No product found with name = {name_product}")
		else:
			query = ("SELECT * FROM detail_transaction")
			cursor.execute(query)
			result = cursor.fetchall()
			cursor.close()
			return result

	@app.get('/detail_transaction/{id_product}')
	async def product_recommendation(id_product: int):
		cursor = conn.cursor()
		query = "SELECT name_product FROM product WHERE id = %s"
		cursor.execute(query, (id_product,))
		name = cursor.fetchone()
		if name:
			query = "SELECT id_transaction, id_product FROM detail_transaction"
			cursor.execute(query)
			result = cursor.fetchall()

			transaction_data = defaultdict(list)
			for item in result:
				id_transaction, id_item = item
				transaction_data[id_transaction].append(id_item)
			
			result = [tuple(trans) for trans in transaction_data.values()]
			related_transactions = [transaction for transaction in result if id_product in transaction]
			items = [item for transaction in related_transactions for item in transaction if item != id_product]

			counter = Counter(items)
			most_common = counter.most_common()
			list_item = []
			for item in most_common:
				query = "SELECT name_product FROM product WHERE id = %s"
				cursor.execute(query, (item[0],))
				item_name = cursor.fetchone()
				if item_name and item_name != name:
					list_item.append(item_name)

			cursor.close()

			list_frequent = list(set(list_item))[:3]
			list_new = [item[0] for item in list_frequent]
			if list_new:
				return f"Product frequently bought with {name[0]}: {list_new}"
			else:
				return "We have no information on this. Be the first to try it out!"
			
		else:
			cursor.close()
			raise HTTPException(status_code=404, detail=f"No information found for product with ID = {id_product}")

	def check_id_exists(table_name: str, id: int):
		cursor = conn.cursor()
		query = f"SELECT * FROM {table_name} WHERE id = {id}"
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()
		return bool(result)

	@app.post('/product')
	async def add_product(name_product: str, price: int, id_category: int, merk: str, stock: int, id_aisle: int):
		aisle_exists = check_id_exists('aisle', id_aisle)
		category_exists = check_id_exists('category', id_category)

		if aisle_exists and category_exists and stock > 0 and price > 0:
			cursor = conn.cursor()
			query = f"INSERT INTO product (name_product, price, id_category, merk, stock, id_aisle) VALUES ('{name_product}', {price}, {id_category}, '{merk}', {stock}, {id_aisle})"
			cursor.execute(query)
			conn.commit()
			cursor.close()
			return f"Product {name_product} has been added"
		else:
			raise HTTPException(status_code=422, detail=f"Data is not valid, product {name_product} has not been added")

	@app.put('/product')
	async def update_product(id_product: int, price = int, stock = int):
		cursor = conn.cursor()
		query = f"SELECT * FROM product WHERE id={id_product}"
		cursor.execute(query)
		result = cursor.fetchall()
		if result:
			query = f"UPDATE product SET stock = {stock}, price = {price} WHERE id = {id_product}"
			cursor.execute(query)
			conn.commit()
			cursor.close()
			return f"Stock for id_product = {id_product} is updated"
		else:
			cursor.close()
			raise HTTPException(status_code=404, detail=f"No product found with id = {id_product}")
		
	@app.delete('/product/{id}')
	async def delete_product(id: int):
		cursor = conn.cursor()
		query = f"SELECT * FROM product WHERE id = {id}"
		cursor.execute(query)
		result = cursor.fetchall()
		if result:
			query = f"DELETE FROM product WHERE id = {id}"
			cursor.execute(query)
			conn.commit()
			cursor.close()
			return f"Product with id_product = {id} is deleted"
		else:
			cursor.close()
			raise HTTPException(status_code=404, detail=f"No product found with id = {id}")
