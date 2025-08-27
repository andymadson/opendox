
import React, { useState, useEffect } from 'react';

interface User {
    id: number;
    name: string;
    email: string;
}

interface UserListProps {
    apiClient: any;
}

/**
 * Component to display a list of users
 */
const UserList: React.FC<UserListProps> = ({ apiClient }) => {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        loadUsers();
    }, []);
    
    const loadUsers = async () => {
        try {
            const data = await apiClient.getUsers();
            setUsers(data);
        } finally {
            setLoading(false);
        }
    };
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div>
            <h2>Users</h2>
            {users.map(user => (
                <div key={user.id}>
                    {user.name} - {user.email}
                </div>
            ))}
        </div>
    );
};

export default UserList;
