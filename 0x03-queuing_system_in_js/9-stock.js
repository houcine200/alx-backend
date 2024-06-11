const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Data
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

// Data Access
function getItemById(id) {
  return listProducts.find(product => product.id === id);
}

// Server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

// Products Route
app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  })));
});

// In stock in Redis
const client = redis.createClient();
const reserveStockById = promisify(client.set).bind(client);
const getCurrentReservedStockById = promisify(client.get).bind(client);

// Product Detail Route
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(`item.${itemId}`) || 0;

  res.json({
    itemId: item.id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
    currentQuantity: item.stock - currentStock
  });
});

// Reserve a Product Route
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(`item.${itemId}`) || 0;

  if (currentStock >= item.stock) {
    return res.json({ status: 'Not enough stock available', itemId: item.id });
  }

  await reserveStockById(`item.${itemId}`, currentStock + 1);

  res.json({ status: 'Reservation confirmed', itemId: item.id });
});
