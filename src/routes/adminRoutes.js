const express = require('express');
const router = express.Router();
const adminAuth = require('../middleware/adminAuth');
const adminController = require('../controllers/adminController');

// All routes in this file require admin privileges
router.use(adminAuth);

router.get('/stats', adminController.getDashboardStats);

module.exports = router;
