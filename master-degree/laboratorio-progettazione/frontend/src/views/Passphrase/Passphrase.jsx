import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import style from "./Passphrase.module.css";
import '@fortawesome/fontawesome-free/css/all.min.css';
import { useTheme } from "../../hooks/useTheme.js";
import { Navbar } from "reactstrap";
import logoColor from "../../assets/images/logoColor.png";

const Passphrase = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [passphrase, setPassphrase] = useState("");
    const { darkMode } = useTheme();

    useEffect(() => {
        if (location.state && location.state.passphrase) {
            setPassphrase(location.state.passphrase);
        } else {
            navigate("/error");
        }
    }, [location, navigate]);

    const handleSave = () => {
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
                <h2>Your Recovery Passphrase</h2>
                <p>Please save this passphrase in a secure location. You will need it to recover your account if you
                    forget
                    your password.</p>
                <div className={style.passphraseContainer}>
                    <div className={style.passphrase}>{passphrase}</div>
                    <button onClick={() => navigator.clipboard.writeText(passphrase)} className={style.copyBtn}>
                        <i className="fas fa-copy"></i>
                    </button>
                </div>
                <button onClick={handleSave} className={style.saveBtn}>I have saved the passphrase</button>
            </div>
        </div>
    );
};

export default Passphrase;