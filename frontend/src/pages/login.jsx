import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h1 style={styles.title}>ARIA</h1>
        <p style={styles.subtitle}>Your personal assistant</p>
        <input
          style={styles.input}
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="off"
        />
        <div style={styles.passwordWrapper}>
          <input
            style={styles.passwordInput}
            type={showPassword ? 'text' : 'password'}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="off"
          />
          <span
            style={styles.toggle}
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? '🙈' : '👁️'}
          </span>
        </div>
        {error && <p style={styles.error}>{error}</p>}
        <button style={styles.button} onClick={handleLogin} disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
        <p style={styles.link}>
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#0a0a0a',
  },
  box: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '40px',
    backgroundColor: '#111',
    borderRadius: '16px',
    width: '320px',
    gap: '12px',
  },
  title: { color: '#fff', fontSize: '2rem', margin: 0 },
  subtitle: { color: '#888', margin: 0 },
  input: {
    width: '100%',
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid #333',
    backgroundColor: '#1a1a1a',
    color: '#fff',
    fontSize: '14px',
    boxSizing: 'border-box',
  },
  passwordWrapper: {
    width: '100%',
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
  },
  passwordInput: {
    width: '100%',
    padding: '12px',
    paddingRight: '40px',
    borderRadius: '8px',
    border: '1px solid #333',
    backgroundColor: '#1a1a1a',
    color: '#fff',
    fontSize: '14px',
    boxSizing: 'border-box',
  },
  toggle: {
    position: 'absolute',
    right: '12px',
    cursor: 'pointer',
    fontSize: '16px',
  },
  button: {
    width: '100%',
    padding: '12px',
    borderRadius: '8px',
    border: 'none',
    backgroundColor: '#6c63ff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer',
  },
  error: { color: '#ff4444', fontSize: '13px' },
  link: { color: '#888', fontSize: '13px' },
};

export default Login;