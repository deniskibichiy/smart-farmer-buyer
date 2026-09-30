import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        // Placeholder for Django backend authentication
        console.log('Login submitted:', { email, password });
        
        // For demonstration, let's navigate to the buyer dashboard
        // In a real app, this would depend on the user's role returned by the backend
        navigate('/buyer-dashboard');
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Email:</label>
                    <input 
                        type="email" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input 
                        type="password" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Login</button>
            </form>
            <p>Don't have an account? <Link to="/register">Register here</Link></p>
        </div>
    );
};

export default Login;
