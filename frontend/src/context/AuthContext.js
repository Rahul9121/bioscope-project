import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { sessionStatus } from '../services/api';

const AuthContext = createContext({
  user: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: () => false,
  loading: false,
  refreshAuthStatus: () => {},
  checkSession: () => {}
});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = useCallback((userData) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
    console.log("✅ User logged in and stored:", userData);
  }, []);
  
  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem("user");
    console.log("✅ User logged out");
  }, []);

  // Check server session status
  const checkSession = useCallback(async () => {
    try {
      const response = await sessionStatus();
      if (response.data.active) {
        // If server session is active, ensure localStorage is in sync
        const storedUser = localStorage.getItem("user");
        if (!storedUser) {
          console.log("🔄 Session active but no local user data. Refreshing...");
          return false; // Need to re-login to get user data
        }
      } else {
        // Server session expired, clear local data
        if (user) {
          console.log("🚨 Server session expired, clearing local auth");
          logout();
        }
      }
      return response.data.active;
    } catch (error) {
      console.log("⚠️ Session check failed, assuming logged out:", error.message);
      if (user) {
        logout();
      }
      return false;
    }
  }, [user, logout]);

  // Load user from localStorage and verify session on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        const storedUser = localStorage.getItem("user");
        if (storedUser && storedUser !== "undefined" && storedUser !== "null") {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          console.log("✅ User loaded from localStorage:", userData);
          
          // Verify session is still valid
          const sessionActive = await checkSession();
          if (!sessionActive) {
            console.log("🚨 Stored user found but session invalid, clearing auth");
            setUser(null);
            localStorage.removeItem("user");
          }
        } else {
          // No stored user, check if there's an active session we missed
          await checkSession();
        }
      } catch (error) {
        console.error("❌ Error during auth initialization:", error);
        localStorage.removeItem("user");
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    
    initAuth();
  }, [checkSession]);

  const isAuthenticated = useCallback(() => {
    return user !== null;
  }, [user]);

  const refreshAuthStatus = useCallback(async () => {
    setLoading(true);
    await checkSession();
    setLoading(false);
  }, [checkSession]);

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      logout, 
      isAuthenticated, 
      loading, 
      refreshAuthStatus,
      checkSession
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
