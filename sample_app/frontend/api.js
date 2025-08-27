
/**
 * API client for backend communication
 */
class ApiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    /**
     * Fetch all users from the API
     * @returns {Promise<Array>} List of users
     */
    async getUsers() {
        const response = await fetch(`${this.baseUrl}/api/users`);
        return response.json();
    }
    
    /**
     * Create a new user
     * @param {Object} userData - User data to create
     * @returns {Promise<Object>} Created user
     */
    async createUser(userData) {
        const response = await fetch(`${this.baseUrl}/api/users`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(userData)
        });
        return response.json();
    }
}

export default ApiClient;
