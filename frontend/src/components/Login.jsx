import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsSubmitting(true);

        try {
            const response = await fetch('http://localhost:8000/api/user/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                setError(data.detail || data.email?.[0] || 'Login failed. Check your email and password.');
                return;
            }

            if (!data.tokens?.access || !data.tokens?.refresh || !data.user?.role) {
                setError('The server returned an incomplete login response.');
                return;
            }

            localStorage.setItem('accessToken', data.tokens.access);
            localStorage.setItem('refreshToken', data.tokens.refresh);
            navigate(data.user.role === 'FARMER' ? '/farmer-dashboard' : '/buyer-dashboard');
        } catch {
            setError('Unable to reach the server. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            {error && <div className="error-message" role="alert" style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
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
                <button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Logging in...' : 'Login'}</button>
            </form>
            <p>Don't have an account? <Link to="/register">Register here</Link></p>
        </div>
    );
};

export default Login;
