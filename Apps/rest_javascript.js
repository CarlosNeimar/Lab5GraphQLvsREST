// rest_server.js
const express = require('express');
const app = express();
const port = 3000;

const COMMENTS_DATA = [
    { id: "1", userId: "13", score: 3, text: "This is okay." },
    { id: "2", userId: "10", score: 8, text: "Amazing!" },
    { id: "3", userId: "13", score: 9, text: "My favorite one." },
    { id: "4", userId: "11", score: 5, text: "Not bad." },
    { id: "5", userId: "10", score: 1, text: "Terrible." },
];

app.get('/comments', (req, res) => {
    res.json(COMMENTS_DATA);
});

app.get('/comments/:id', (req, res) => {
    const comment = COMMENTS_DATA.find(c => c.id === req.params.id);
    res.json(comment);
});

app.get('/comments/user/:userId', (req, res) => {
    const comments = COMMENTS_DATA.filter(c => c.userId === req.params.userId);
    res.json(comments);
});

app.get('/comments/min-score/:score', (req, res) => {
    const minScore = parseInt(req.params.score, 10);
    const comments = COMMENTS_DATA.filter(c => c.score >= minScore);
    res.json(comments);
});

app.listen(port, () => {
    console.log(`[JS] Servidor REST rodando em http://localhost:${port}`);
});