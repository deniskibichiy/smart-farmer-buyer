import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const ProtectedRoute = ({ role, children }) => {
    const [status, setStatus] = useState('checking');
    const [userRole, setUserRole] = useState('');

    useEffect(() => {
        let cancelled = false;
        const refreshToken = localStorage.getItem('refreshToken');

        const refreshAccessToken = async () => {
            if (!refreshToken) return null;

            const response = await fetch(`${API_BASE_URL}/api/user/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: refreshToken })
            });
            if (!response.ok) return null;

            const data = await response.json();
            if (!data.access) return null;

            localStorage.setItem('accessToken', data.access);
            return data.access;
        };

        const fetchProfile = (accessToken) => fetch(`${API_BASE_URL}/api/user/profile/`, {
            headers: { Authorization: `Bearer ${accessToken}` }
        });

        const verifySession = async () => {
            try {
                let accessToken = localStorage.getItem('accessToken');
                if (!accessToken) accessToken = await refreshAccessToken();
                if (!accessToken) {
                    if (!cancelled) setStatus('unauthenticated');
                    return;
                }

                let response = await fetchProfile(accessToken);
                if (response.status === 401) {
                    accessToken = await refreshAccessToken();
                    if (accessToken) response = await fetchProfile(accessToken);
                }

                if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    if (!cancelled) setStatus('unauthenticated');
                    return;
                }
                if (!response.ok) throw new Error('Profile request failed.');

                const user = await response.json();
                if (!cancelled) {
                    setUserRole(user.role);
                    setStatus(user.role === role ? 'authorized' : 'wrong-role');
                }
            } catch {
                if (!cancelled) setStatus('error');
            }
        };

        verifySession();
        return () => {
            cancelled = true;
        };
    }, [role]);

    if (status === 'checking') return <div role="status">Checking your session...</div>;
    if (status === 'unauthenticated') return <Navigate to="/login" replace />;
    if (status === 'wrong-role') {
        return <Navigate to={userRole === 'FARMER' ? '/farmer-dashboard' : '/buyer-dashboard'} replace />;
    }
    if (status === 'error') return <div role="alert">Unable to verify your session. Please try again.</div>;

    return children;
};

export default ProtectedRoute;