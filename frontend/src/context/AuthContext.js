import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext({
  user: null,
  token: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: () => false,
  loading: false,
  getAuthHeader: () => ({})
});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  
  console.log("🔑 JWT AuthProvider - Current user:", user);
  console.log("🔑 JWT AuthProvider - Has token:", !!token);

  // Get user and token from localStorage
  const getAuthDataFromStorage = () => {
    try {
      const storedUser = localStorage.getItem("user");
      const storedToken = localStorage.getItem("auth_token");
      
      const userData = storedUser && storedUser !== "null" && storedUser !== "undefined" 
        ? JSON.parse(storedUser) : null;
      const tokenData = storedToken && storedToken !== "null" && storedToken !== "undefined" 
        ? storedToken : null;
        
      return { user: userData, token: tokenData };
    } catch (error) {
      console.error("❌ Error parsing stored auth data:", error);
      localStorage.removeItem("user");
      localStorage.removeItem("auth_token");
      return { user: null, token: null };
    }
  };

  // JWT-based login function
  const login = useCallback((userData, authToken) => {
    console.log("🔑 JWT LOGIN - Setting user:", userData);
    console.log("🔑 JWT LOGIN - Setting token:", authToken ? "[PRESENT]" : "[MISSING]");
    
    setUser(userData);
    setToken(authToken);
    
    // Store in localStorage
    localStorage.setItem("user", JSON.stringify(userData));
    if (authToken) {
      localStorage.setItem("auth_token", authToken);
    }
    
    console.log("✅ JWT LOGIN - User and token stored successfully");
  }, []);
  
  // JWT-based logout function
  const logout = useCallback(() => {
    console.log("🔑 JWT LOGOUT - Clearing user and token");
    setUser(null);
    setToken(null);
    localStorage.removeItem("user");
    localStorage.removeItem("auth_token");
    console.log("✅ JWT LOGOUT - User and token cleared");
  }, []);

  // Get Authorization header for API requests
  const getAuthHeader = useCallback(() => {
    if (token) {
      return { Authorization: `Bearer ${token}` };
    }
    return {};
  }, [token]);

  // Initialize JWT auth state from localStorage
  useEffect(() => {
    console.log("🔑 JWT AuthContext initialization starting...");
    
    const { user: storedUser, token: storedToken } = getAuthDataFromStorage();
    if (storedUser && storedToken) {
      console.log("✅ JWT Found stored user and token:", storedUser.email);
      setUser(storedUser);
      setToken(storedToken);
    } else {
      console.log("🚶 JWT No stored auth data found");
    }
    
    setLoading(false);
    console.log("✅ JWT AuthContext initialization complete");
  }, []);

  // Check if user is authenticated (has both user data and token)
  const isAuthenticated = useCallback(() => {
    const result = user !== null && token !== null;
    console.log("🔍 JWT isAuthenticated check:", result, "User:", !!user, "Token:", !!token);
    return result;
  }, [user, token]);

  // Refresh auth status from storage
  const refreshAuthStatus = useCallback(() => {
    console.log("🔄 JWT Refreshing auth status");
    const { user: storedUser, token: storedToken } = getAuthDataFromStorage();
    if (storedUser && storedToken) {
      setUser(storedUser);
      setToken(storedToken);
    } else {
      setUser(null);
      setToken(null);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ 
      user, 
      token,
      login, 
      logout, 
      isAuthenticated, 
      loading, 
      refreshAuthStatus,
      getAuthHeader
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
