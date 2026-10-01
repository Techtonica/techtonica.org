const db = require('../db');

const getApplicationStats = async (req, res) => {
    try {
        const userId = req.user.id;
        
        // Se for admin, pode ver estatísticas globais, se for applicant, apenas as dele
        const isAdmin = req.user.role === 'admin';
        
        let statsQuery = db('applications')
            .select('status')
            .count('id as count')
            .groupBy('status');

        if (!isAdmin) {
            statsQuery = statsQuery.where('user_id', userId);
        }

        const stats = await statsQuery;
        
        // Formata os dados para o frontend (ex: { pending: 1, approved: 0, rejected: 0 })
        const formattedStats = stats.reduce((acc, curr) => {
            acc[curr.status] = parseInt(curr.count);
            return acc;
        }, {});

        // Busca detalhes da aplicação do usuário logado
        const applicationDetails = await db('applications')
            .where('user_id', userId)
            .first();

        res.json({
            stats: formattedStats,
            details: applicationDetails || null
        });
    } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
};

module.exports = { getApplicationStats };
