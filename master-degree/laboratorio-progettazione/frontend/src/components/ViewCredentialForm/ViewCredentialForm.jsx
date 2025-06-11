import {useState, useEffect} from "react";
import style from "./ViewCredentialForm.module.css";
import eyeIcon from "../../assets/icons/eye.svg";
import eyeSlashIcon from "../../assets/icons/eye-slash.svg";
import copyIcon from "../../assets/icons/copy.svg";
import generate from "../../assets/icons/generate.png";
import openURL from "../../assets/icons/link.png";
import PasswordGenerator from "../../components/PasswordGenerator/PasswordGenerator.jsx";
import { useTheme } from "../../hooks/useTheme.js";

const ViewCredentialForm = ({credential, isEditing: initialEditing, onClose}) => {
    const [showPassword, setShowPassword] = useState(false);
    const [isEditing, setIsEditing] = useState(initialEditing);
    const [editedCredential, setEditedCredential] = useState({...credential});
    const [showGenerator, setShowGenerator] = useState(false);
    const { darkMode } = useTheme();

    useEffect(() => {
        setEditedCredential({...credential});
        setIsEditing(initialEditing);
    }, [credential, initialEditing]);

    if (!credential) return null;

    const handleCopyPassword = () => {
        navigator.clipboard.writeText(credential.password);
    };

    const handleChange = (e) => {
        const {name, value} = e.target;
        setEditedCredential((prev) => ({...prev, [name]: value}));
    };

    const handleSave = async (e) => {
        if (e) e.preventDefault();
        try {
            const response = await fetch(`/api/credentials/${credential.id_credential}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(editedCredential),
            });
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Failed to update credential");
            }
        } catch (error) {
            console.error("Error updating credential:", error);
        }
    };

    const handleOpenURL = () => {
        if (credential.url) {
            // Add https:// if missing
            const prefixedUrl = credential.url.startsWith('https://') || credential.url.startsWith('http://')
                ? credential.url
                : `https://${credential.url}`;
            window.open(prefixedUrl, '_blank', 'noopener,noreferrer');
        }
    };
 

    return (
        <div className={`${style.popupOverlay} ${darkMode ? style.dark : ''}`}>
            <div className={style.formWrapper}>
                <h2>{isEditing ? "Edit Credential" : "View Credential"}</h2>
                {isEditing ? (
                    <form onSubmit={handleSave}>
                        <input
                            className={style.fieldEdit}
                            type="text"
                            name="url"
                            placeholder="URL"
                            value={editedCredential.url}
                            onChange={handleChange}
                            required
                        />
                        <input
                            className={style.fieldEdit}
                            type="text"
                            name="username"
                            placeholder="Username"
                            value={editedCredential.username}
                            onChange={handleChange}
                            required
                        />
                        <div className={`${style.fieldEdit} eyeContainer`}>
                            <input
                                type={showPassword ? "text" : "password"}
                                name="password"
                                placeholder="Password"
                                value={editedCredential.password}
                                onChange={handleChange}
                                required
                            />
                            <div className="eyeButtons">
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="eyeButton"
                                >
                                    <img src={showPassword ? eyeSlashIcon : eyeIcon} alt="Toggle Password Visibility"/>
                                </button>
                                <button
                                    type="button"
                                    onClick={(e) => {
                                        e.preventDefault();
                                        setShowGenerator(true);
                                    }}
                                    className={style.generateButton}
                                >
                                    <img src={generate} alt="Generate Password"/>
                                </button>
                            </div>
                        </div>
                        <textarea
                            className={style.fieldEdit}
                            name="notes"
                            placeholder="Notes"
                            value={editedCredential.notes}
                            onChange={handleChange}
                        ></textarea>
                        <div className={`${style.fieldEdit} ${style.popupButtons} ${style.rightButtons}`}>
                            <button type="submit" className="button">
                                Save Changes
                            </button>
                            <button type="button" className="button" onClick={onClose}>
                                Cancel
                            </button>
                        </div>
                        {showGenerator && (
                            <PasswordGenerator
                                setShowGenerator={setShowGenerator}
                                onClose={() => setShowGenerator(false)}
                                onUse={(generated) => {
                                    setEditedCredential((prev) => ({
                                        ...prev,
                                        password: generated,
                                    }));
                                    setShowGenerator(false);
                                }}
                            />
                        )}
                    </form>
                ) : (
                    <div className={`${style.view} ${darkMode ? style.dark : ''}`}>
                        <div className={`${style.field} eyeContainer`}>
                            <input
                                type="text"
                                name="url"
                                placeholder="URL"
                                value={credential.url}
                                readOnly
                            />
                            <div className="eyeButtons">
                                <button type="button" onClick={handleOpenURL} className={style.generateButton}>
                                    <img src={openURL} alt="Open URL"/>
                                </button>
                            </div>
                        </div>
                        <input
                            className={style.field}
                            type="text"
                            name="username"
                            placeholder="Username"
                            value={credential.username}
                            readOnly
                        />
                        <div className={`${style.field} eyeContainer`}>
                            <input
                                type={showPassword ? "text" : "password"}
                                name="password"
                                placeholder="Password"
                                value={credential.password}
                                readOnly
                            />
                            <div className="eyeButtons">
                                <button type="button" onClick={() => setShowPassword(!showPassword)}
                                        className="eyeButton">
                                    <img src={showPassword ? eyeSlashIcon : eyeIcon} alt="Toggle Password Visibility"/>
                                </button>
                                <button type="button" onClick={handleCopyPassword} className="eyeButton">
                                    <img src={copyIcon} alt="Copy Password"/>
                                </button>
                            </div>
                        </div>
                        <textarea
                            className={style.field}
                            name="notes"
                            placeholder="Notes"
                            value={credential.notes}
                            readOnly
                        ></textarea>
                        <div className={`${style.field} ${style.popupButtons} ${style.rightButtons}`}>
                            <button type="button" className="button" onClick={() => setIsEditing(true)}>
                                Edit
                            </button>
                            <button type="button" className="button" onClick={onClose}>
                                Close
                            </button>
                        </div>
                    </div>
                )}
            </div>
            {showGenerator && (
                <PasswordGenerator
                    setShowGenerator={setShowGenerator}
                    onClose={() => setShowGenerator(false)}
                    onUse={(generated) => {
                        setEditedCredential((prev) => ({
                            ...prev,
                            password: generated,
                        }));
                        setShowGenerator(false);
                    }}
                />
            )}
        </div>
    );
};

export default ViewCredentialForm;
