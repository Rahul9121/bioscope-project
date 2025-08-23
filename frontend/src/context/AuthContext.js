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
  
  console.log("🔴 EMERGENCY AuthProvider - Current user:", user);
  console.log("🔴 EMERGENCY localStorage user:", localStorage.getItem("user"));

  // EMERGENCY FIX: Simple, bulletproof authentication
  const getUserFromStorage = () => {
    try {
      const storedUser = localStorage.getItem("user");
      if (storedUser && storedUser !== "null" && storedUser !== "undefined") {
        return JSON.parse(storedUser);
      }
    } catch (error) {
      console.error("❌ Error parsing stored user:", error);
      localStorage.removeItem("user");
    }
    return null;
  };

  const login = useCallback((userData) => {
    console.log("🔥 EMERGENCY LOGIN - Setting user:", userData);
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
    console.log("✅ EMERGENCY LOGIN - User stored successfully");
    // Force a re-render by triggering a state update
    setTimeout(() => {
      const stored = getUserFromStorage();
      if (stored && !user) {
        console.log("🔄 EMERGENCY - Forcing user state sync");
        setUser(stored);
      }
    }, 100);
  }, [user]);
  
  const logout = useCallback(() => {
    console.log("🔥 EMERGENCY LOGOUT - Clearing user");
    setUser(null);
    localStorage.removeItem("user");
    console.log("✅ EMERGENCY LOGOUT - User cleared");
  }, []);

  // EMERGENCY: Simple session check that doesn't interfere
  const checkSession = useCallback(async () => {
    try {
      const response = await sessionStatus();
      console.log("🔍 EMERGENCY Session check result:", response.data);
      return response.data?.active || false;
    } catch (error) {
      console.log("⚠️ EMERGENCY Session check failed (keeping user logged in):", error.message);
      return true; // Keep user logged in if session check fails
    }
  }, []);

  // EMERGENCY: Initialize auth state from localStorage ONLY
  useEffect(() => {
    console.log("🔥 EMERGENCY AuthContext initialization starting...");
    
    const storedUser = getUserFromStorage();
    if (storedUser) {
      console.log("✅ EMERGENCY Found stored user:", storedUser);
      setUser(storedUser);
    } else {
      console.log("🚪 EMERGENCY No stored user found");
    }
    
    setLoading(false);
    console.log("✅ EMERGENCY AuthContext initialization complete");
  }, []);

  // EMERGENCY: Double-check auth state every second for debugging
  useEffect(() => {
    const interval = setInterval(() => {
      const storedUser = getUserFromStorage();
      if (storedUser && !user) {
        console.log("⚡ EMERGENCY Auto-sync: Found user in storage but not in state");
        setUser(storedUser);
      } else if (!storedUser && user) {
        console.log("⚡ EMERGENCY Auto-sync: User in state but not in storage");
        setUser(null);
      }
    }, 1000);
    
    return () => clearInterval(interval);
  }, [user]);

  const isAuthenticated = useCallback(() => {
    const result = user !== null;
    console.log("🔍 EMERGENCY isAuthenticated check:", result, "User:", user);
    return result;
  }, [user]);

  const refreshAuthStatus = useCallback(async () => {
    console.log("🔄 EMERGENCY Refreshing auth status");
    const storedUser = getUserFromStorage();
    if (storedUser) {
      setUser(storedUser);
    }
  }, []);

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
