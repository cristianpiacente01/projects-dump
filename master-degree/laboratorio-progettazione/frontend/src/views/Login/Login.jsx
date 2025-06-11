import { NavLink, useNavigate } from "react-router-dom";
import illustration from '../../assets/images/illustration.png';
import style from "./Login.module.css";
import { useState } from "react";
import axios from "axios";
import eyeIcon from '../../assets/icons/eye.svg';
import eyeSlashIcon from '../../assets/icons/eye-slash.svg';
import { useTheme } from "../../hooks/useTheme.js";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [emailError, setEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();
    const { darkMode } = useTheme();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setEmailError(false);
        setPasswordError(false);


        try {
            const response = await axios.post("/api/login", { email, password }, { withCredentials: true });
            if (response.data.otp_required) {
                navigate("/enter-otp", { state: { email: response.data.email } });
            } else if (response.status === 200) {
                navigate("/vault");
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.detail) {
                setError(err.response.data.detail);
                if (err.response.data.detail === "User not found") {
                    setEmailError(true);
                    setPasswordError(true);
                } else if (err.response.data.detail === "Incorrect password") {
                    setPasswordError(true);
                } else if (err.response.data.detail === "Email not verified") {
                    navigate("/verify", { state: { email } });
                }
            } else {
                setError("Error in login. Retry.");
            }
        }
    };

    return (
        <div className={`${style.container} ${darkMode ? style.dark : ''}`}>
            <div className={style.row}>
                <div className={style.left}>
                    <h1>Manage your passwords safely and securely</h1>
                    <p>Discover all the features of PassGuard</p>
                    <img className={style.image} src={illustration} alt="Illustration"/>
                </div>
                <div className={style.right}>
                    <div className="formWrapper">
                        <h2>Unlock your <span className={style.name}>PassGuard</span></h2>
                        <form onSubmit={handleSubmit}>
                            <div className={`${emailError ? style.errorInput : ""}`}>
                                <input
                                    type="email"
                                    placeholder="Email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div className={`eyeContainer ${passwordError ? style.errorInput : ""}`}>
                                <input
                                    type={showPassword ? "text" : "password"}
                                    placeholder="Password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                                <div className="eyeButtons">
                                    <button type="button" onClick={() => setShowPassword(!showPassword)}
                                            className="eyeButton">
                                        <img src={showPassword ? eyeSlashIcon : eyeIcon}
                                             alt="Toggle Password Visibility"/>
                                    </button>
                                </div>
                            </div>
                            {error && <p className={style.error}>{error}</p>}
                            <NavLink className={style.forgotButton} to="/recover-password">Forgot password?</NavLink>
                            <button type="submit" className="button">Login</button>
                        </form>
                        <p>Don't have an account? <NavLink className="link" to="/registration">Register</NavLink></p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;