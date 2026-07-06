import { createContext, useContext, useState, useEffect } from 'react';
import { todoService } from '../services/api/todoService';
import { useAuth } from './AuthContext';

const TodoContext = createContext(null);

export const TodoProvider = ({ children }) => {
  const [todos, setTodos] = useState([]);
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    if (isLoggedIn) fetchTodos();
  }, [isLoggedIn]);

  const fetchTodos = async () => {
    const data = await todoService.getTodos();
    setTodos(data);
  };

  const addTodo = async (title, description) => {
    const todo = await todoService.createTodo(title, description);
    setTodos((prev) => [...prev, todo]);
  };

  const updateTodo = async (id, updates) => {
    const updated = await todoService.updateTodo(id, updates);
    setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
  };

  const deleteTodo = async (id) => {
    await todoService.deleteTodo(id);
    setTodos((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <TodoContext.Provider value={{ todos, addTodo, updateTodo, deleteTodo, fetchTodos }}>
      {children}
    </TodoContext.Provider>
  );
};

export const useTodo = () => useContext(TodoContext);
