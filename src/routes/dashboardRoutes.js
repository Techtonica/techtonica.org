const express = require('express');
const router = express.Router();
const { getApplicationStats } = require('../controllers/applicantDashboardController');
const { authorize } = require('../middleware/auth');

// Rota protegida: Apenas usuários com role 'applicant' ou 'admin' podem acessar
router.get('/applicant/stats', authorize(['applicant', 'admin']), getApplicationStats);

module.exports = router;
