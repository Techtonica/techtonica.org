const db = require('../models'); // Assumindo a pasta de modelos do ORM

const getDashboardStats = async (req, res) => {
  try {
    // 1. Total number of users
    const totalUsers = await db.User.count();

    // 2. Total number of applications
    const totalApplications = await db.Application.count();

    // 3. Applications by status
    const statusCounts = await db.Application.findAll({
      attributes: [
        'status',
        [db.sequelize.fn('COUNT', db.sequelize.col('id')), 'count']
      ],
      group: ['status']
    });

    // Format status counts for the frontend
    const applicationsByStatus = statusCounts.reduce((acc, curr) => {
      acc[curr.status] = curr.dataValues.count;
      return acc;
    }, {});

    res.json({
      summary: {
        totalUsers,
        totalApplications
      },
      breakdown: {
        applicationsByStatus
      }
    });
  } catch (error) {
    console.error('Error fetching dashboard stats:', error);
    res.status(500).json({ error: 'Internal server error while fetching statistics' });
  }
};

module.exports = {
  getDashboardStats
};
