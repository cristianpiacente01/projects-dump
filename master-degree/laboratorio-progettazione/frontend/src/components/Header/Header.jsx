import useIdleTimer from "../../hooks/useIdleTimer";
import { useState, useEffect } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { Collapse, Nav, Navbar, NavbarToggler, NavItem } from 'reactstrap';
import style from "./Header.module.css";
import settings from "../../assets/icons/settings.png";
import logout from "../../assets/icons/logout.png";
import vault from "../../assets/icons/vault.png";
import profile from "../../assets/icons/profile.png";
import axios from 'axios';
import moon from "../../assets/icons/moon.png";
import light from "../../assets/icons/sun.png";
import { useTheme } from "../../hooks/useTheme.js";

const Header = ({logo}) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [showIdleWarning, setShowIdleWarning] = useState(false);
    const [isOpen, _] = useState(false);
    const [isProfilePopupOpen, setIsProfilePopupOpen] = useState(false);
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();
    const { darkMode, toggleTheme } = useTheme();

    const handleLogout = async () => {
        try {
            await axios.post("/api/logout", {}, { withCredentials: true });
            window.location.href = "/";
        } catch (err) {
            console.error("Error during logout", err);
        }
    };

    // by default warn 30s before the timeout of 10m, see useIdleTimer.js
    const { resetTimer, warningTime } = useIdleTimer(
        handleLogout,
        () => {
            setShowIdleWarning(true);
        },
        isAuthenticated,
        30, // warning before in seconds, change it to lower for the demo (e.g., 2)
        600 // total timeout in seconds, change it to lower for the demo (e.g., 10)
    );

    useEffect(() => {
        if (location.pathname === "/") return;  // skip auth check on login page

        const checkAuth = async () => {
            try {
                const res = await axios.get("/api/me", { withCredentials: true });
                if (res.status === 200) {
                    setIsAuthenticated(true);
                }
            } catch {
                setIsAuthenticated(false);
            }
        };

        checkAuth();
    }, [location.pathname]);


    useEffect(() => {
        if (!isAuthenticated) return;

        resetTimer(); // Reset idle timer after successful login
        const showWarning = () => setShowIdleWarning(true);
        window.addEventListener("user-will-be-logged-out", showWarning);

        return () => {
            window.removeEventListener("user-will-be-logged-out", showWarning);
        };
    }, [isAuthenticated, resetTimer]);

    const toggleProfile = (event) => {
        event.stopPropagation();
        setIsProfilePopupOpen(!isProfilePopupOpen);
    };

    return (
        <div className={`${style.container} ${darkMode ? style.dark : ''}`}>
            <Navbar expand="md" className={style.navBar}>
                <div
                    className="logoContainer"
                    onClick={() => navigate(location.pathname !== "/" ? "/vault" : "/")}
                >
                    <img className="logo" src={logo} alt="Logo"/>
                    <span className="name">PassGuard</span>
                </div>
                <Collapse isOpen={isOpen} navbar className={style.collapseMenu}>
                    {location.pathname === "/" ? (
                        <NavLink to="/registration">
                            <button className={style.registerBtn}>Register</button>
                        </NavLink>
                    ) : (
                        <Nav className="mr-auto" navbar>
                            <NavItem key="/vault" className={style.navItem}>
                                <NavLink exact="true" to="/vault">
                                    <img src={vault} alt="Vault"/>
                                    <span>Vault</span>
                                </NavLink>
                            </NavItem>
                            <NavItem key="/profile" style={{position: "relative"}}>
                                <div className={style.profileTrigger}>
                                    <NavLink exact="true" to="#" onClick={toggleProfile}>
                                        <img src={profile} alt="Profile" />
                                        <span>Profile</span>
                                    </NavLink>
                                </div>

                                {isProfilePopupOpen && (
                                    <div className={style.profilePopup}>
                                        <button
                                            onClick={() => {
                                                setIsProfilePopupOpen(false);
                                                navigate("/settings");
                                            }}
                                            className={style.profileButtonContent}
                                        >
                                            <img src={settings} alt="Settings"/>
                                            <span>Settings</span>
                                        </button>
                                        <button
                                            onClick={() => {
                                                setIsProfilePopupOpen(false);
                                                setIsPopupOpen(true);
                                            }}
                                            className={style.profileButtonContent}
                                        >
                                            <img src={logout} alt="Logout"/>
                                            <span>Logout</span>
                                        </button>
                                    </div>
                                )}
                            </NavItem>
                        </Nav>
                    )}
                    <img
                        src={darkMode ? light : moon}
                        alt="Toggle Theme"
                        onClick={toggleTheme}
                        className={style.themeToggle}
                    />
                </Collapse>
            </Navbar>

            {showIdleWarning && (
                <div className={style.popupOverlay}>
                    <div className={style.popupContent}>
                        <h3>Session Timeout Warning</h3>
                        <p>Your session will expire in <strong>{warningTime}</strong> seconds due to inactivity.</p>
                    <div className={style.popupButtons}>
                        <button className="button" onClick={() => {
                          resetTimer();
                          setShowIdleWarning(false);
                        }}>
                          I'm still here
                        </button>
                    </div>
                    </div>
                </div>
            )}

            {isPopupOpen && (
                <div className={style.popupOverlay}>
                    <div className={style.popupContent}>
                        <h3>Confirm logout?</h3>
                        <p>This action will end your session.</p>
                        <div className={style.popupButtons}>
                            <button className="redButton" onClick={handleLogout}>Logout</button>
                            <button className="button" onClick={() => setIsPopupOpen(false)}>
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Header;