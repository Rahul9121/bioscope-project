import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { healthCheck } from '../services/api';

const AuthContext = createContext({
  user: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: () => false,
  loading: false,
  checkAuthStatus: () => {}
});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  console.log("🔑 SESSION AuthProvider - Current user:", user);

  // Session-based login function
  const login = useCallback((userData) => {
    console.log("🔑 SESSION LOGIN - Setting user:", userData);
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
    console.log("✅ SESSION LOGIN - User stored successfully");
  }, []);
  
  // Session-based logout function
  const logout = useCallback(async () => {
    console.log("🔑 SESSION LOGOUT - Clearing user");
    setUser(null);
    localStorage.removeItem("user");
    
    // Call backend logout to clear session
    try {
      const { logout: apiLogout } = await import('../services/api');
      await apiLogout();
      console.log("✅ SESSION LOGOUT - Backend session cleared");
    } catch (error) {
      console.log("⚠️ SESSION LOGOUT - Backend logout failed (probably offline):", error.message);
    }
    
    console.log("✅ SESSION LOGOUT - User cleared");
  }, []);

  // Check authentication status with backend
  const checkAuthStatus = useCallback(async () => {
    try {
      // Import the API function dynamically to avoid circular dependency
      const { default: api } = await import('../services/api');
      const response = await api.get('/session-status');
      
      if (response.data.active && response.data.debug?.user_id) {
        const userData = {
          id: response.data.debug.user_id,
          email: response.data.debug.email
        };
        setUser(userData);
        localStorage.setItem("user", JSON.stringify(userData));
        console.log("✅ SESSION AUTH STATUS - User authenticated:", userData.email);
        return userData;
      } else {
        setUser(null);
        localStorage.removeItem("user");
        console.log("🚫 SESSION AUTH STATUS - No active session");
        return null;
      }
    } catch (error) {
      console.log("⚠️ SESSION AUTH STATUS - Check failed:", error.message);
      // Keep existing user state if session check fails (backend might be offline)
      const storedUser = localStorage.getItem("user");
      if (storedUser && storedUser !== "null") {
        try {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          return userData;
        } catch (parseError) {
          localStorage.removeItem("user");
          setUser(null);
        }
      }
      return null;
    }
  }, []);

  // Initialize session-based auth state
  useEffect(() => {
    console.log("🔑 SESSION AuthContext initialization starting...");
    
    const initAuth = async () => {
      // First check localStorage for existing user
      const storedUser = localStorage.getItem("user");
      if (storedUser && storedUser !== "null") {
        try {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          console.log("✅ SESSION Found stored user:", userData.email);
        } catch (error) {
          localStorage.removeItem("user");
        }
      }
      
      setLoading(false);
      console.log("✅ SESSION AuthContext initialization complete");
    };
    
    initAuth();
  }, []);

  // Check if user is authenticated (session-based)
  const isAuthenticated = useCallback(() => {
    const result = user !== null;
    console.log("🔍 SESSION isAuthenticated check:", result, "User:", !!user);
    return result;
  }, [user]);

  return (
    <AuthContext.Provider value={{ 
      user,
      login, 
      logout, 
      isAuthenticated, 
      loading,
      checkAuthStatus
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
