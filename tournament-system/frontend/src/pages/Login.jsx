import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import './Login.css';

const Login = () => {
    const navigate = useNavigate();
    
    // Стани для форми
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [errors, setErrors] = useState({});
    const [apiError, setApiError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    // Стани для UI (тема та мова)
    const [isDarkTheme, setIsDarkTheme] = useState(localStorage.getItem('mapStyle') === 'dark');
    const [language, setLanguage] = useState(localStorage.getItem('appLanguage') || 'uk');

    // Перемикач теми
    const toggleTheme = () => {
        const newTheme = !isDarkTheme;
        setIsDarkTheme(newTheme);
        localStorage.setItem('mapStyle', newTheme ? 'dark' : 'standard');
    };

    // Обробка вводу
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setErrors({ ...errors, [e.target.name]: null }); // Прибираємо помилку при введенні
        setApiError(null);
    };

    // Клієнтська валідація
    const validateForm = () => {
        let newErrors = {};
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!formData.email) {
            newErrors.email = language === 'uk' ? "Email є обов'язковим" : "Email is required";
        } else if (!emailRegex.test(formData.email)) {
            newErrors.email = language === 'uk' ? "Введіть коректну email адресу" : "Enter a valid email address";
        }

        if (!formData.password) {
            newErrors.password = language === 'uk' ? "Пароль є обов'язковим" : "Password is required";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    // Відправка запиту
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) return;

        setIsLoading(true);
        setApiError(null);

        try {
            // Виконуємо POST запит на бекенд
            const response = await api.post('auth/login/', formData);
            
            // Зберігаємо JWT токени
            localStorage.setItem('access', response.data.access);
            localStorage.setItem('refresh', response.data.refresh);
            
            // Перенаправляємо на головну
            navigate('/');
        } catch (error) {
            // Обробка 400/401 помилок
            if (error.response) {
                if (error.response.status === 401) {
                    setApiError(language === 'uk' ? "Невірний email або пароль." : "Invalid email or password.");
                } else if (error.response.status === 400) {
                    // Якщо бекенд повертає об'єкт з помилками для конкретних полів
                    setApiError(language === 'uk' ? "Перевірте правильність введених даних." : "Check your input data.");
                }
            } else {
                setApiError(language === 'uk' ? "Помилка з'єднання із сервером." : "Server connection error.");
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`login-page ${isDarkTheme ? 'dark-theme' : ''}`}>
            {/* Верхні контролери (з вашого дизайну) */}
            <div className="top-controls">
                <select 
                    className="lang-select" 
                    value={language} 
                    onChange={(e) => {
                        setLanguage(e.target.value);
                        localStorage.setItem('appLanguage', e.target.value);
                    }}
                >
                    <option value="uk">УКР</option>
                    <option value="en">ENG</option>
                </select>
                <button className="theme-toggle-btn" onClick={toggleTheme} title="Змінити тему">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                </button>
            </div>

            <div className="form-container">
                <h2 className="form-title">{language === 'uk' ? "Вхід у систему" : "Sign In"}</h2>

                {/* Блок з помилкою від API */}
                {apiError && <div className="api-error-alert">{apiError}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label>Email</label>
                        <input 
                            type="email" 
                            name="email"
                            placeholder="name@example.com"
                            value={formData.email}
                            onChange={handleChange}
                            style={{ borderColor: errors.email ? '#e53935' : '' }}
                        />
                        {errors.email && <span className="error-text">{errors.email}</span>}
                    </div>

                    <div className="input-group">
                        <label>{language === 'uk' ? "Пароль" : "Password"}</label>
                        <input 
                            type={showPassword ? "text" : "password"} 
                            name="password"
                            placeholder={language === 'uk' ? "Введіть пароль" : "Enter password"}
                            value={formData.password}
                            onChange={handleChange}
                            style={{ borderColor: errors.password ? '#e53935' : '' }}
                        />
                        {/* Іконка Ока */}
                        <button 
                            type="button" 
                            className="password-toggle"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? "🙈" : "👁️"}
                        </button>
                        {errors.password && <span className="error-text">{errors.password}</span>}
                    </div>

                    <button type="submit" className="btn btn-primary" disabled={isLoading}>
                        {isLoading 
                            ? (language === 'uk' ? "Зачекайте..." : "Please wait...") 
                            : (language === 'uk' ? "Увійти" : "Sign In")}
                    </button>
                </form>

                <Link to="/register" className="register-link">
                    {language === 'uk' ? "Немає акаунту? Зареєструватись" : "Don't have an account? Sign up"}
                </Link>
            </div>
        </div>
    );
};

export default Login;