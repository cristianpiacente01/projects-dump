import { useState, useEffect } from 'react';
import style from "../Settings/Settings.module.css";
import axios from "axios";
import closeIcon from "../../assets/icons/close.svg";
import eyeSlashIcon from "../../assets/icons/eye-slash.svg";
import eyeIcon from "../../assets/icons/eye.svg";
import logoutIcon from "../../assets/icons/logout.svg";
import trashIcon from "../../assets/icons/trash.svg";
import { useTheme } from "../../hooks/useTheme.js";

const ChevronIcon = ({ open }) => (
    <svg
        className={style.accordionIcon}
        style={{ transform: open ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.2s" }}
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="#007bb8"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
    >
        <polyline points="9 6 15 12 9 18" />
    </svg>
);

const Settings = () => {
    const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [qrCode, setQrCode] = useState(null);
    const [manualCode, setManualCode] = useState(null);
    const [otp, setOtp] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmNewPassword, setConfirmNewPassword] = useState("");
    const [showOldPassword, setShowOldPassword] = useState(false);
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showConfirmNewPassword, setShowConfirmNewPassword] = useState(false);
    const [error, setError] = useState("");
    const [pendingSecret, setPendingSecret] = useState(null);
    const [openAccordion, setOpenAccordion] = useState("2fa");
    const [passwordChangeError, setPasswordChangeError] = useState("");
    const [passwordChangeSuccess, setPasswordChangeSuccess] = useState("");
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const { darkMode } = useTheme();

    useEffect(() => {
        const fetch2FAStatus = async () => {
            try {
                const response = await axios.get("/api/2fa-status", {withCredentials: true});
                setTwoFactorEnabled(response.data.enabled);
            } catch (error) {
                console.error("Error fetching 2FA status:", error);
            }
        };
        fetch2FAStatus();
    }, []);

    const handleEnable2FA = async () => {
        try {
            const response = await axios.post("/api/enable-2fa", {}, {withCredentials: true});
            setQrCode(response.data.qrCode);
            setManualCode(response.data.manualCode);
            setPendingSecret(response.data.manualCode);
            setIsModalOpen(true);
            setOtp("");
            setError("");
        } catch (error) {
            console.error("Error enabling 2FA:", error);
        }
    };

    const handleDisable2FA = async () => {
        try {
            await axios.post("/api/disable-2fa", {}, {withCredentials: true});
            setQrCode(null);
            setManualCode(null);
            setPendingSecret(null);
            setTwoFactorEnabled(false);
        } catch (error) {
            console.error("Error disabling 2FA:", error);
        }
    };

    const handleVerifyAndEnable2FA = async () => {
        try {
            setError("");
            await axios.post("/api/enable-2fa-verify", {
                otp: otp.trim(),
                secret: pendingSecret
            }, {withCredentials: true});
            setTwoFactorEnabled(true);
            setIsModalOpen(false);
            setQrCode(null);
            setManualCode(null);
            setPendingSecret(null);
            setOtp("");
        } catch (error) {
            console.error("Invalid OTP:", error);
            if (error.response && error.response.status === 422) {
                setError("Please enter a valid 6-digit OTP.");
            } else {
                setError("Invalid OTP. Please try again.");
            }
        }
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setQrCode(null);
        setManualCode(null);
        setPendingSecret(null);
        setOtp("");
        setError("");
    };

    // Accordion toggle
    const toggleAccordion = (section) => {
        setOpenAccordion(openAccordion === section ? null : section);
    };

    const handleChangeMainPassword = async () => {
        setPasswordChangeError("");
        setPasswordChangeSuccess("");
        if (newPassword !== confirmNewPassword) {
            setPasswordChangeError("New passwords do not match.");
            return;
        }
        try {
            await axios.post(
                "/api/change-password",
                {
                    old_password: oldPassword,
                    new_password: newPassword,
                },
                { withCredentials: true }
            );
            setPasswordChangeSuccess("Password changed successfully.");
            setOldPassword("");
            setNewPassword("");
            setConfirmNewPassword("");
        } catch (err) {
            setPasswordChangeError(
                err?.response?.data?.detail || "Error changing password."
            );
        }
    };

    const handleLogout = async () => {
        try {
            await axios.post("/api/logout", {}, { withCredentials: true });
            window.location.href = "/";
        } catch (err) {
            console.error("Error during logout", err);
        }
    };

    const handleDeleteAccount = async () => {
    try {
        await axios.delete("/api/delete-account", { withCredentials: true });
        window.location.href = "/";
    } catch (error) {
        console.error("Error while deleting the account:", error);
        alert(
            error?.response?.data?.detail ||
            "An error occurred while deleting the account."
        );
    }
    };


    return (
        <div className={`${darkMode ? style.dark : ''}`}>
            <div className="container">
                <div className={style.header}>
                    <h1>Settings</h1>
                </div>
                <div className={style.settingsSection}>
                    {/* Accordion Item: Edit Main Password */}
                    <div className={style.accordionItem}>
                        <div
                            className={openAccordion === "mainPassword" ? style.accordionHeaderClosed : style.accordionHeader}
                            tabIndex={0}
                            onClick={() => toggleAccordion("mainPassword")}
                            onKeyPress={e => {
                                if (e.key === "Enter" || e.key === " ") toggleAccordion("mainPassword");
                            }}
                            aria-expanded={openAccordion === "mainPassword"}
                        >
                            <span>Edit Main Password</span>
                            <ChevronIcon open={openAccordion === "mainPassword"}/>
                        </div>
                        <div
                            className={openAccordion === "mainPassword" ? style.accordionContent : style.accordionContentClosed}>
                            {openAccordion === "mainPassword" && (
                                <form
                                    onSubmit={e => {
                                        e.preventDefault();
                                        handleChangeMainPassword();
                                    }}
                                    style={{display: "flex", flexDirection: "column", gap: 12}}
                                >
                                    <div className="eyeContainer">
                                        <input
                                            type={showOldPassword ? "text" : "password"}
                                            name="old password"
                                            placeholder="Old Password"
                                            value={oldPassword}
                                            onChange={(e) => setOldPassword(e.target.value)}
                                            required
                                        />
                                        <div className="eyeButtons">
                                            <button type="button" onClick={() => setShowOldPassword(!showOldPassword)}
                                                    className="eyeButton">
                                                <img src={showOldPassword ? eyeSlashIcon : eyeIcon}
                                                     alt="Toggle Password Visibility"/>
                                            </button>
                                        </div>
                                    </div>
                                    <div className="eyeContainer">
                                        <input
                                            type={showNewPassword ? "text" : "password"}
                                            name="new password"
                                            placeholder="New Password"
                                            value={newPassword}
                                            onChange={(e) => setNewPassword(e.target.value)}
                                            required
                                        />
                                        <div className="eyeButtons">
                                            <button type="button" onClick={() => setShowNewPassword(!showNewPassword)}
                                                    className="eyeButton">
                                                <img src={showNewPassword ? eyeSlashIcon : eyeIcon}
                                                     alt="Toggle Password Visibility"/>
                                            </button>
                                        </div>
                                    </div>
                                    <div className="eyeContainer">
                                        <input
                                            type={showConfirmNewPassword ? "text" : "password"}
                                            name="confirm new password"
                                            placeholder="Confirm New Password"
                                            value={confirmNewPassword}
                                            onChange={(e) => setConfirmNewPassword(e.target.value)}
                                            required
                                        />
                                        <div className="eyeButtons">
                                            <button type="button"
                                                    onClick={() => setShowConfirmNewPassword(!showConfirmNewPassword)}
                                                    className="eyeButton">
                                                <img src={showConfirmNewPassword ? eyeSlashIcon : eyeIcon}
                                                     alt="Toggle Password Visibility"/>
                                            </button>
                                        </div>
                                    </div>
                                    {passwordChangeError && (
                                        <div className={style.error}>{passwordChangeError}</div>
                                    )}
                                    {passwordChangeSuccess && (
                                        <div style={{color: "green", marginTop: 8}}>{passwordChangeSuccess}</div>
                                    )}
                                    <div>
                                        <button className="button" type="submit">Save Changes</button>
                                    </div>
                                </form>
                            )}
                        </div>
                    </div>
                    <div className={style.twofaSection}>
                        <div className={style.accordionItem}>
                            <div
                                className={openAccordion === "2fa" ? style.accordionHeaderClosed : style.accordionHeader}
                                tabIndex={0}
                                onClick={() => toggleAccordion("2fa")}
                                onKeyPress={e => {
                                    if (e.key === "Enter" || e.key === " ") toggleAccordion("2fa");
                                }}
                                aria-expanded={openAccordion === "2fa"}
                            >
                                <span>Two-Factor Authentication</span>
                                <ChevronIcon open={openAccordion === "2fa"}/>
                            </div>
                            <div
                                className={openAccordion === "2fa" ? style.accordionContent : style.accordionContentClosed}>
                                {openAccordion === "2fa" && (
                                    <div>
                                        <div className={style.settingRow}>
                                            <span>Enable Two-Factor Authentication</span>
                                            <label className={style.switch}>
                                                <input
                                                    type="checkbox"
                                                    checked={twoFactorEnabled}
                                                    disabled={isModalOpen}
                                                    onChange={() => {
                                                        if (!twoFactorEnabled) {
                                                            handleEnable2FA();
                                                        } else {
                                                            handleDisable2FA();
                                                        }
                                                    }}
                                                />
                                                <span className={style.slider}></span>
                                            </label>
                                        </div>
                                        <p style={{margin: "0 0 0 0", color: "#666", fontSize: "14px"}}>
                                            Protect your account with an extra layer of security.
                                        </p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                    <div className={style.buttonGroup}>
                        <button
                            className={style.logoutButton}
                            onClick={() => setIsPopupOpen(true)}
                        >
                            <img src={logoutIcon} alt="Logout" className={style.iconLeft + " " + style.logoutIcon} />
                            Logout
                        </button>
                    </div>

                    {/* Danger Zone */}
                    <div className={style.dangerZone}>
                        <h2 className={style.dangerZoneTitle}>Danger Zone</h2>
                        <p className={style.dangerZoneDesc}>
                            Deleting your account is <b>irreversible</b>. All your data will be permanently removed and cannot be recovered.
                        </p>
                        <button
                            className={style.deleteButton}
                            onClick={() => setShowDeleteConfirm(true)}
                        >
                            <img src={trashIcon} alt="Delete" className={style.iconLeft + " " + style.deleteIcon} />
                            Delete Account
                        </button>
                    </div>

                    {/* Logout Modal */}
                    {isPopupOpen && (
                        <div className={style.modalOverlay}>
                            <div className={style.modalContent}>
                                <button
                                    className={style.closeButton}
                                    onClick={() => setIsPopupOpen(false)}
                                >
                                    <img src={closeIcon} alt="Close"/>
                                </button>
                                <h3>Confirm Logout</h3>
                                <p>You are about to log out from your account.<br/>Are you sure you want to continue?</p>
                                <div className={style.modalButtonRow}>
                                    <button className={style.logoutButton} onClick={handleLogout}>
                                        <img src={logoutIcon} alt="Logout" className={style.iconLeft + " " + style.logoutIcon} />
                                        Logout
                                    </button>
                                    <button className="button" onClick={() => setIsPopupOpen(false)}>
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Delete Account Modal */}
                    {showDeleteConfirm && (
                        <div className={style.modalOverlay}>
                            <div className={style.modalContent}>
                                <button
                                    className={style.closeButton}
                                    onClick={() => setShowDeleteConfirm(false)}
                                >
                                    <img src={closeIcon} alt="Close"/>
                                </button>
                                <h3>Delete Account</h3>
                                <p style={{color: "#e74c3c", fontWeight: 500}}>
                                    This action is <b>irreversible</b>.<br/>
                                    All your data will be permanently deleted.<br/>
                                    Are you sure you want to continue?
                                </p>
                                <div className={style.modalButtonRow}>
                                    <button className={style.deleteButton} onClick={() => {
                                        setShowDeleteConfirm(false);
                                        handleDeleteAccount();
                                    }}>
                                        <img src={trashIcon} alt="Delete" className={style.iconLeft + " " + style.deleteIcon} />
                                        Delete
                                    </button>
                                    <button className="button" onClick={() => setShowDeleteConfirm(false)}>
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                </div>

                {isModalOpen && (
                    <div className={style.modalOverlay}>
                        <div className={style.modalContent}>
                            <button
                                className={style.closeButton}
                                onClick={handleCloseModal}
                            >
                                <img src={closeIcon} alt="Close"/>
                            </button>
                            <h3>Scan the QR Code</h3>
                            <p>Use an authenticator app (e.g. Google Authenticator) to scan the QR code below:</p>
                            <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" className={style.qrCode}/>
                            <p>If you cannot scan the QR code, enter this code manually:</p>
                            <code>{manualCode}</code>
                            <p>Enter the OTP to confirm:</p>
                            <input
                                type="text"
                                value={otp}
                                onChange={(e) => setOtp(e.target.value)}
                                maxLength="6"
                                className={style.input}
                            />
                            {error && <p className={style.error}>{error}</p>}
                            <div className={style.buttonVerify}>
                            <button onClick={handleVerifyAndEnable2FA} className="button">
                                    Verify & Enable
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Settings;

