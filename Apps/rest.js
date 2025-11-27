const fs = require('fs');
const path = require('path');
const express = require('express');
const app = express();
const port = 3000;


const caminhoArquivo = path.join(__dirname, 'database.json');
const rawData = fs.readFileSync(caminhoArquivo, 'utf-8');
const COMMENTS_DATA = JSON.parse(rawData);


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