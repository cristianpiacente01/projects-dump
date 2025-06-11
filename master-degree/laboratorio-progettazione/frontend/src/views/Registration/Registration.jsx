import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { Navbar } from 'reactstrap';
import logoColor from '../../assets/images/logoColor.png';
import style from "./Registration.module.css";
import axios from "axios";
import eyeIcon from '../../assets/icons/eye.svg';
import eyeSlashIcon from '../../assets/icons/eye-slash.svg';
import { useTheme } from "../../hooks/useTheme.js";

const Registration = () => {
    const [email, setEmail] = useState("");
    const [confirmEmail, setConfirmEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [emailError, setEmailError] = useState(false);
    const [confirmEmailError, setConfirmEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const [confirmPasswordError, setConfirmPasswordError] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const navigate = useNavigate();
    const { darkMode } = useTheme();

    const validateForm = () => {
        const errors = [];
        const validDomains = ["gmail", "yahoo", "hotmail", "outlook", "proton", "duck", "example"];
        const emailDomain = email.split("@")[1];

        if (!email) errors.push("Email is required.");
        if (!confirmEmail) errors.push("Confirm email is required.");
        if (!password) errors.push("Password is required.");
        if (!confirmPassword) errors.push("Confirm password is required.");
        if (email && confirmEmail && email !== confirmEmail) {
            errors.push("Emails do not match.");
            setEmailError(true);
            setConfirmEmailError(true);
        }
        if (password && confirmPassword && password !== confirmPassword) {
            errors.push("Passwords do not match.");
            setPasswordError(true);
            setConfirmPasswordError(true);
        }
        if (password && password.length < 8) {
            errors.push("Password must be at least 8 characters.");
            setPasswordError(true);
        }
        if (email && !validDomains.some(domain => emailDomain.includes(domain))) {
            errors.push("Email domain not valid.");
            setEmailError(true);
            setConfirmEmailError(true);
        }
        return errors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setEmailError(false);
        setConfirmEmailError(false);
        setPasswordError(false);
        setConfirmPasswordError(false);

        const errors = validateForm();
        if (errors.length > 0) {
            setError(errors.join("\n"));
            return;
        }

        try {
            await axios.post("/api/register", {
                email,
                confirm_email: confirmEmail,
                password,
                confirm_password: confirmPassword,
            });
            navigate("/verify", { state: { email } });
        } catch (err) {
            if (err.response && err.response.data && err.response.data.detail) {
                setError(err.response.data.detail);
            } else {
                setError("Error in registration. Retry.");
            }
        }
    };

    return (
        <div className={`${darkMode ? style.dark : ''}`}>
            <Navbar expand="md" className={style.navBar}>
                <NavLink to="/" className="logoContainer">
                    <img className="logo" src={logoColor} alt="LogoColor"/>
                    <span className={style.name}>PassGuard</span>
                </NavLink>
            </Navbar>
            <div className={style.container}>
                <div className="formWrapper">
                    <h2>Create your account</h2>
                    <form onSubmit={handleSubmit}>
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className={emailError ? style.errorInput : ""}
                            required
                        />
                        <input
                            type="email"
                            placeholder="Confirm email"
                            value={confirmEmail}
                            onChange={(e) => setConfirmEmail(e.target.value)}
                            className={confirmEmailError ? style.errorInput : ""}
                            required
                        />
                        <div className="eyeContainer">
                            <input
                                type={showPassword ? "text" : "password"}
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className={passwordError ? style.errorInput : ""}
                                required
                            />
                            <div className="eyeButtons">
                                <button type="button" onClick={() => setShowPassword(!showPassword)}
                                        className="eyeButton">
                                    <img src={showPassword ? eyeSlashIcon : eyeIcon} alt="Toggle Password Visibility"/>
                                </button>
                            </div>
                        </div>
                        <div className="eyeContainer">
                            <input
                                type={showConfirmPassword ? "text" : "password"}
                                placeholder="Confirm password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className={confirmPasswordError ? style.errorInput : ""}
                                required
                            />
                            <div className="eyeButtons">
                                <button type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                        className="eyeButton">
                                    <img src={showConfirmPassword ? eyeSlashIcon : eyeIcon} alt="Toggle Password Visibility"/>
                                </button>
                            </div>
                        </div>
                        {error && <p className={style.error}>{error.split("\n").map((msg, index) => <span
                            key={index}>{msg}<br/></span>)}</p>}
                        <button type="submit" className="button">Register</button>
                    </form>
                    <p>Already have an account? <NavLink className="link" to="/">Login</NavLink></p>
                </div>
            </div>
        </div>
    );
};
export default Registration;