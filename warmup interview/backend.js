const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'colloquium'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Connected to database');
});

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

app.post('/submit-answer', (req, res) => {
    const { category, question, answer, timeTaken } = req.body; // Add timeTaken here
    const sql = 'INSERT INTO warmup_responses (category, question, answer, time_taken) VALUES (?, ?, ?, ?)';
    db.query(sql, [category, question, answer, timeTaken], (err, result) => {
        if (err) {
            console.error(err);
            res.status(500).json({ error: 'Error saving response' });
        } else {
            res.json({ message: 'Response saved successfully' });
        }
    });
});

app.listen(3001, () => console.log('Server running on port 3001'));
