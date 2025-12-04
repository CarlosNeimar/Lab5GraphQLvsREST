const express = require('express');
const fs = require('fs');
const app = express();
const PORT = 4000;

// Carregar dados na memória
const rawData = fs.readFileSync('../Data/database_100k_user.json');
const db = JSON.parse(rawData);

app.use(express.json());

// Endpoint 1: Lista todos usuários (Simples)
app.get('/users', (req, res) => {
    res.json(db.users);
});

// Endpoint 2: Detalhe do usuário + Posts (Simulação de relacionamento)
app.get('/users/:id/full', (req, res) => {
    const userId = parseInt(req.params.id);
    const user = db.users.find(u => u.id === userId);
    if (!user) return res.status(404).send();

    const posts = db.posts.filter(p => p.user_id === userId);
    res.json({ ...user, posts });
});

app.listen(PORT, () => {
    console.log(`Node REST rodando em http://localhost:${PORT}`);
});