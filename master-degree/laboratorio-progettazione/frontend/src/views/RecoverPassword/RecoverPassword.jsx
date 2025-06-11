import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { Navbar } from "reactstrap";
import style from "./RecoverPassword.module.css";
import passphraseStyle from "../Passphrase/Passphrase.module.css";
import logoColor from '../../assets/images/logoColor.png';
import { useTheme } from "../../hooks/useTheme.js";

const RecoverPassword = () => {
    const [email, setEmail] = useState("");
    const [passphrase, setPassphrase] = useState("");
    const [isVerified, setIsVerified] = useState(false);
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [userId, setUserId] = useState(null);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [showPassphrase, setShowPassphrase] = useState(false);
    const [generatedPassphrase, setGeneratedPassphrase] = useState("");
    const navigate = useNavigate();
    const { darkMode } = useTheme();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        try {
            const res = await fetch("/api/recover/verify-passphrase", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, passphrase }),
            });
            if (res.ok) {
                const data = await res.json();
                setUserId(data.user_id);
                setIsVerified(true);
            } else {
                const err = await res.json();
                setError(err.detail || "Invalid email or passphrase");
            }
        } catch {
            setError("Server error");
        }
    };

    const handlePasswordReset = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        if (newPassword !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }
        try {
            const res = await fetch("/api/recover/reset-password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, new_password: newPassword }),
            });
            if (res.ok) {
                const data = await res.json();
                setGeneratedPassphrase(data.new_passphrase);
                setShowPassphrase(true);
                setSuccess("Password reset successful! Please save your new recovery passphrase.");
            } else {
                const err = await res.json();
                setError(err.detail || "Failed to reset password");
            }
        } catch {
            setError("Server error");
        }
    };

    const handleContinue = () => {
        setShowPassphrase(false);
        navigate("/");
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
                {showPassphrase ? (
                    <div className="formWrapper">
                        <h2>New Recovery Passphrase</h2>
                        <p>
                            For your security, your recovery passphrase has been regenerated.<br/>
                            Please save it in a secure place. You will need it to recover your account in the future.
                        </p>
                        <div className={passphraseStyle.passphraseContainer}>
                            <span className={passphraseStyle.passphrase}>{generatedPassphrase}</span>
                            <button
                                className={passphraseStyle.copyBtn}
                                onClick={() => navigator.clipboard.writeText(generatedPassphrase)}
                            >
                                <i className="fas fa-copy"></i>
                            </button>
                        </div>
                        <button
                            className={passphraseStyle.saveBtn}
                            onClick={handleContinue}
                        >
                            I have saved the passphrase
                        </button>
                    </div>
                ) : !isVerified ? (
                    <>
                        <div className="formWrapper">
                            <h2>Recover your password</h2>
                            <p>Insert your email and recovery passphrase to proceed</p>
                            <form onSubmit={handleSubmit}>
                                <input
                                    type="email"
                                    placeholder="Email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                                <input
                                    type="text"
                                    placeholder="Passphrase"
                                    value={passphrase}
                                    onChange={(e) => setPassphrase(e.target.value)}
                                    required
                                />
                                {error && <p className={style.error}>{error}</p>}
                                <button type="submit" className="button">Submit</button>
                            </form>
                        </div>
                    </>
                ) : (
                    <>
                        <div className="formWrapper">
                            <h2>Set a new password</h2>
                            <form onSubmit={handlePasswordReset}>
                                <input
                                    type="password"
                                    placeholder="New password"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    required
                                />
                                <input
                                    type="password"
                                    placeholder="Confirm new password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    required
                                />
                                {error && <p className={style.error}>{error}</p>}
                                {success && <p className={style.success}>{success}</p>}
                                <button type="submit" className="button">Reset Password</button>
                            </form>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default RecoverPassword;
