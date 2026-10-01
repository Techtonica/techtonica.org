const jwt = require('jsonwebtoken');

const authorize = (roles = []) => {
    if (typeof roles === 'string') {
        roles = [roles];
    }

    return (req, res, next) => {
        const token = req.headers.authorization?.split(' ')[1];

        if (!token) {
            return res.status(401).json({ message: 'Authentication token required' });
        }

        try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET);
            req.user = decoded;

            if (roles.length && !roles.includes(decoded.role)) {
                return res.status(403).json({ message: 'Forbidden: Insufficient permissions' });
            }

            next();
        } catch (error) {
            return res.status(401).json({ message: 'Invalid or expired token' });
        }
    };
};

module.exports = { authorize };
