// Adicionando a rota de admin ao arquivo principal da aplicação
const express = require('express');
const app = express();
const adminRoutes = require('./routes/adminRoutes');

// ... outras configurações de middleware (cors, json, etc)

app.use('/api/admin', adminRoutes);

// ... restante do arquivo
