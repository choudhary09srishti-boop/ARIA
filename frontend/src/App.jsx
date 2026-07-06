import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { TodoProvider } from './context/TodoContext';
import Login from './pages/Login';
import Signup from './pages/Signup';

const ProtectedRoute = ({ children }) => {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? children : <Navigate to="/login" />;
};

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
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