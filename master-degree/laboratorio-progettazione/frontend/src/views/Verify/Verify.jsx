import {NavLink, useLocation, useNavigate} from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import axios from "axios";
import style from "./Verify.module.css";
import { useTheme } from "../../hooks/useTheme.js";
import {Navbar} from "reactstrap";
import logoColor from "../../assets/images/logoColor.png";

const Verify = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [code, setCode] = useState(new Array(6).fill(""));
    const [error, setError] = useState("");
    const [email, ] = useState(location.state.email);
    const [timer, setTimer] = useState(60);
    const inputRefs = useRef([]);
    const { darkMode } = useTheme();

    useEffect(() => {
        if (timer > 0) {
            const interval = setInterval(() => {
                setTimer((prev) => prev - 1);
            }, 1000);
            return () => clearInterval(interval);
        }
    }, [timer]);

    const handleChange = (e, index) => {
        const value = e.target.value;
        if (/^[0-9A-Z]$/.test(value)) {
            const newCode = [...code];
            newCode[index] = value;
            setCode(newCode);
            if (index < 5) {
                inputRefs.current[index + 1].focus();
            }
        } else if (value === "") {
            const newCode = [...code];
            newCode[index] = "";
            setCode(newCode);
        }
    };

    const handleKeyDown = (e, index) => {
        if (e.key === "Backspace") {
            const newCode = [...code];
            if (newCode[index] === "") {
                if (index > 0) {
                    newCode[index - 1] = "";
                    setCode(newCode);
                    inputRefs.current[index - 1].focus();
                }
            } else {
                newCode[index] = "";
                setCode(newCode);
            }
        }
    };

    const handlePaste = (e) => {
        const paste = e.clipboardData.getData("text");
        if (/^[0-9A-Z]{6}$/.test(paste)) {
            const newCode = paste.split("");
            setCode(newCode);
            newCode.forEach((digit, index) => {
                inputRefs.current[index].value = digit;
            });
            inputRefs.current[5].focus();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const response = await axios.post("/api/verify", {
                email,
                code: code.join(""),
            });
            navigate("/passphrase", { state: { passphrase: response.data.passphrase } });
        } catch (err) {
            if (err.response && err.response.data && err.response.data.detail) {
                setError(err.response.data.detail);
            } else {
                setError("Error in verification. Retry.");
            }
        }
    };

    const handleResend = async () => {
        if (timer === 0) {
            setError("");
            setTimer(60);

            try {
                await axios.post("/api/resend-code", { email });
            } catch {
                setError("Error in resending code. Retry.");
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
                <h2>Verify your account</h2>
                <p>An email has been sent to the email address used. Fill in the verification code below to verify your
                    account.</p>
                <form onSubmit={handleSubmit}>
                    <div className={style.codeContainer} onPaste={handlePaste}>
                        {code.map((digit, index) => (
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
                    <div className={style.buttonContainer}>
                        <div className={style.resendContainer}>
                            <button
                                onClick={handleResend}
                                className={style.resendButton}
                                disabled={timer > 0}
                            >
                                Resend Code
                            </button>
                            {timer > 0 && <span className={style.timer}>:{timer}</span>}
                        </div>
                        <button type="submit" className={style.verifyButton}>Verify</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Verify;