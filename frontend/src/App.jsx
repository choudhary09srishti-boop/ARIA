import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { TodoProvider } from './context/TodoContext';

const ProtectedRoute = ({ children }) => {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? children : <Navigate to="/login" />;
};

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<div>Login Page Coming Soon</div>} />
      <Route path="/signup" element={<div>Signup Page Coming Soon</div>} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <TodoProvider>
              <div>Main App Coming Soon</div>
            </TodoProvider>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

const App = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;