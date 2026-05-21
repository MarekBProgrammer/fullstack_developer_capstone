const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(express.json());

// Load JSON data
let reviews_data, dealerships_data;

try {
  reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'));
  dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'));
} catch (err) {
  console.error("Error loading JSON files", err);
}

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

// Load models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Reset and insert initial data
Reviews.deleteMany({}).then(() => {
  Reviews.insertMany(reviews_data['reviews']);
});

Dealerships.deleteMany({}).then(() => {
  Dealerships.insertMany(dealerships_data['dealerships']);
});

// Home
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch reviews by dealer ID
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: Number(req.params.id) });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealerships.findOne({ id: Number(req.params.id) });
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching document' });
  }
});

// Insert review
app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;

    const documents = await Reviews.find().sort({ id: -1 });
    const new_id = documents.length > 0 ? documents[0].id + 1 : 1;

    const review = new Reviews({
      id: new_id,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.json(savedReview);

  } catch (error) {
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
