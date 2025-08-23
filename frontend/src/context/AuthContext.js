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
          console.log("✅ AuthContext: User is authenticated");
          
          // Optional: Verify session in background (don't clear user if it fails)
          checkSession().then(sessionActive => {
            if (sessionActive) {
              console.log("✅ Session verified successfully");
            } else {
              console.log("⚠️ Session check failed, but keeping user data for better UX");
              // Don't clear user data - let them stay logged in until they explicitly logout
              // or encounter an actual authentication error
            }
          }).catch(error => {
            console.log("⚠️ Session check failed (network error), keeping user logged in:", error.message);
          });
        } else {
          console.log("🚪 No stored user found");
        }
      } catch (error) {
        console.error("❌ Error during auth initialization:", error);
        // Only clear if there's a parse error, not network errors
        if (error instanceof SyntaxError) {
          localStorage.removeItem("user");
          setUser(null);
        }
      } finally {
        setLoading(false);
      }
    };
    
    initAuth();
  }, []); // Remove checkSession dependency to avoid loops

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
