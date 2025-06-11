import {NavLink, useLocation, useNavigate} from "react-router-dom";
import { useState, useRef } from "react";
import axios from "axios";
import style from "../Verify/Verify.module.css";
import { Navbar } from "reactstrap";
import logoColor from "../../assets/images/logoColor.png";
import { useTheme } from "../../hooks/useTheme.js";

const EnterOTP = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [otp, setOtp] = useState(new Array(6).fill(""));
    const [error, setError] = useState("");
    const inputRefs = useRef([]);
    const { darkMode } = useTheme();

    // NEW: Check if email is present in location.state
    const email = location.state && location.state.email ? location.state.email : "";

    // Optional: Redirect if email is missing
    if (!email) {
        return (
            <div className={`${darkMode ? style.dark : ''}`}>
                <Navbar expand="md" className={style.navBar}>
                    <NavLink to="/" className="logoContainer">
                        <img className="logo" src={logoColor} alt="LogoColor"/>
                        <span className={style.name}>PassGuard</span>
                    </NavLink>
                </Navbar>
                <div className={style.container}>
                    <h2>Error</h2>
                    <p>Email not found. Please login again.</p>
                </div>
            </div>
        );
    }

    const handleChange = (e, index) => {
        const value = e.target.value;
        if (/^[0-9]$/.test(value)) {
            const newOtp = [...otp];
            newOtp[index] = value;
            setOtp(newOtp);
            if (index < 5) inputRefs.current[index + 1].focus();
        } else if (value === "") {
            const newOtp = [...otp];
            newOtp[index] = "";
            setOtp(newOtp);
        }
    };

    const handleKeyDown = (e, index) => {
        if (e.key === "Backspace" || e.key === "Delete") {
            e.preventDefault();
            const newOtp = [...otp];
            if (newOtp[index] === "" && index > 0) {
                newOtp[index - 1] = "";
                setOtp(newOtp);
                inputRefs.current[index - 1].focus();
            } else {
                newOtp[index] = "";
                setOtp(newOtp);
            }
        }
    };

    const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
            const email = location.state && location.state.email ? location.state.email : "";
if (!email) {
    return <p>Email not found. Please login again.</p>;
}
        await axios.post("/api/login-otp", { email, otp: otp.join("") });
        navigate("/vault");
    } catch {
        setError("Invalid OTP. Retry.");
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
                <h2>Enter OTP</h2>
                <p>Enter the 6-digit code from your authenticator app.</p>
                <form onSubmit={handleSubmit}>
                    <div className={style.codeContainer}>
                        {otp.map((digit, index) => (
                            <input
                                key={index}
                                type="text"
                                maxLength="1"
                                value={digit}
                                onChange={(e) => handleChange(e, index)}
                                onKeyDown={(e) => handleKeyDown(e, index)}
                                ref={(el) => (inputRefs.current[index] = el)}
                                required
                            />
                        ))}
                    </div>
                    {error && <p className={style.error}>{error}</p>}
                    <button type="submit" className={style.verifyButton}>Verify</button>
                </form>
            </div>
        </div>
    );
};

export default EnterOTP;