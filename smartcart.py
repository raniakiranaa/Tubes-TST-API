from fastapi import FastAPI, Query
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
	cursor = conn.cursor()

	app = FastAPI()
   
	@app.get('/product')
	async def read_all_product():
		query = ("SELECT * FROM product")
		cursor.execute(query)
		result = cursor.fetchall()
		return result
	
	@app.get('/product/{name_product}')
	async def search_info_product(name_product: str):
		query = f"SELECT * FROM product join aisle on product.id_aisle = aisle.id WHERE name_product = '{name_product}'"
		cursor.execute(query)
		result = cursor.fetchall()

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
			return f"No information found for product: {name_product}"
	
	@app.get('/product/{name_category}')
	async def search_info_category(name_category: str):
		query = f"SELECT DISTINCT name_product FROM product join category on product.id_category = category.id WHERE category.name = '{name_category}'"
		cursor.execute(query)
		result = cursor.fetchall()

		if result:
			count = len(result)
			products = ', '.join(item[0] for item in result)
			if count == 1:
				return f"Product available for category {name_category} is: {products}"
			else:
				return f"Products available for category {name_category} are: {products}"
		else:
			return f"No information found for product available in category: {name_category}"

	@app.get('/aisle')
	async def read_all_aisle():
		query = ("SELECT * FROM aisle")
		cursor.execute(query)
		result = cursor.fetchall()
		return result

	@app.get('/category')
	async def read_all_category():
		query = ("SELECT * FROM category")
		cursor.execute(query)
		result = cursor.fetchall()
		return result
	
	# @app.get('/transaction/{id_product}')
	# async def product_recommendation(id_product: int):
	# 	query = "SELECT id, id_product FROM transaction JOIN detail_transaction ON transaction.id = detail_transaction.id_transaction"
	# 	cursor.execute(query)
	# 	result = cursor.fetchall()

	# 	transaction_data = defaultdict(list)
	# 	for item in result:
	# 		id_transaction, id_item = item
	# 		transaction_data[id_transaction].append(id_item)
		
	# 	result = [tuple(trans) for trans in transaction_data.values()]
		# BELOMMMMM P
		
	@app.get('/detail_transaction/')
	async def read_fav_merk(name_product: Optional[str] = Query(None)):
		if name_product:
			query = f"SELECT name_product, merk, SUM(quantity) as total FROM detail_transaction JOIN product ON detail_transaction.id_product = product.id WHERE name_product = '{name_product}' GROUP BY name_product, merk ORDER BY total DESC"
			cursor.execute(query)
			result = cursor.fetchall()

			if result:
				fav_merk = result[0][1]
				return f"The most bought merk for product {name_product} is {fav_merk}"
			else:
				return f"No transaction found for product: {name_product}"
		else:
			query = ("SELECT * FROM detail_transaction")
			cursor.execute(query)
			result = cursor.fetchall()
			return result
		
	@app.get('/detail_transaction/{id_transaction}')
	async def read_detail_transaction(id_transaction: int):
		query = f"SELECT * FROM detail_transaction where id_transaction = {id_transaction}"
		cursor.execute(query)
		result = cursor.fetchall()
		return result

	def check_id_exists(table_name: str, id: int):
		query = f"SELECT * FROM {table_name} WHERE id = {id}"
		cursor.execute(query)
		result = cursor.fetchall()
		return bool(result)

	@app.post('/product')
	async def add_product(name_product: str, price: int, id_category: int, merk: str, stock: int, id_aisle: int):
		aisle_exists = check_id_exists('aisle', id_aisle)
		category_exists = check_id_exists('category', id_category)

		if aisle_exists and category_exists and stock > 0 and price > 0:
			query = f"INSERT INTO product (name_product, price, id_category, merk, stock, id_aisle) VALUES ('{name_product}', {price}, {id_category}, '{merk}', {stock}, {id_aisle})"
			cursor.execute(query)
			conn.commit()
			return f"Product {name_product} has been added"
		else:
			return f"Data is not valid, product {name_product} has not been added"

	@app.put('/product')
	async def update_product(id_product: int, price = int, stock = int):
		query = f"SELECT * FROM product WHERE id={id_product}"
		cursor.execute(query)
		result = cursor.fetchall()
		if result:
			query = f"UPDATE product SET stock = {stock}, price = {price} WHERE id = {id_product}"
			cursor.execute(query)
			conn.commit()
			return f"Stock for id_product = {id_product} is updated"
		else:
			return f"No product found with id = {id_product}"
		
	@app.delete('/product/{id}')
	async def delete_product(id: int):
		query = f"SELECT * FROM product WHERE id = {id}"
		cursor.execute(query)
		result = cursor.fetchall()
		if result:
			query = f"DELETE FROM product WHERE id = {id}"
			cursor.execute(query)
			conn.commit()
			return f"Product with id_product = {id} is deleted"
		else:
			return f"No product found with id = {id}"
