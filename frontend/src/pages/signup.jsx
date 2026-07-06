import { useState } from 'react';
import { authService } from '../services/auth/authService';
import { useNavigate, Link } from 'react-router-dom';

const Signup = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignup = async () => {
    setLoading(true);
    setError('');
    try {
      await authService.signup(email, password, fullName);
      alert('Account created! Please check your email to confirm your account, then login.');
      navigate('/login');
    } catch (err) {
      const msg = err?.response?.data?.detail || '';
      if (msg.includes('already registered')) {
        setError('This email is already registered. Please login.');
      } else if (password.length < 8) {
        setError('Password must be at least 8 characters.');
      } else if (!/[A-Z]/.test(password)) {
        setError('Password must contain at least one uppercase letter.');
      } else if (!/[0-9]/.test(password)) {
        setError('Password must contain at least one number.');
      } else {
        setError('Signup failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h1 style={styles.title}>ARIA</h1>
        <p style={styles.subtitle}>Create your account</p>
        <input
          style={styles.input}
          type="text"
          placeholder="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
        />
        <input
          style={styles.input}
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p style={styles.error}>{error}</p>}
        <button style={styles.button} onClick={handleSignup} disabled={loading}>
          {loading ? 'Creating account...' : 'Sign Up'}
        </button>
        <p style={styles.link}>
          Already have an account? <Link to="/login">Login</Link>
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

export default Signup;
