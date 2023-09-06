import { auth } from '../../firebase';

const determineUserRole = () => {
    // You can access the currently authenticated user from Firebase Auth
    const user = auth.currentUser;

    if (user) {
        // Check if the user has custom claims indicating their role
        // user.customClaims = {role: 'admin'};
        const customClaims = user.customClaims;

        if (customClaims) {
            // Assuming you set a 'role' claim for the user (e.g., 'user' or 'admin')
            const userRole = customClaims.role;

            if (userRole) {
                return userRole;
            }
        }

        // If custom claims don't exist or don't specify a role, you might check other criteria
        // For example, you can check the user's email or other attributes and determine their role

        // Example: Check if the user's email matches a known admin email
        const adminEmails = ['admin@example.com', 'anotheradmin@example.com'];
        if (adminEmails.includes(user.email)) {
            return 'admin';
        }
    }

    // If no role is determined, return a default role (e.g., 'user')
    return 'user';
};

export default determineUserRole;
