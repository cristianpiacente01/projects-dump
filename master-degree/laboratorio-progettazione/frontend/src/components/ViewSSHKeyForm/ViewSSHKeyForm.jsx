import { useState, useEffect } from "react";
import style from "./ViewSSHKeyForm.module.css";
import eyeIcon from "../../assets/icons/eye.svg";
import eyeSlashIcon from "../../assets/icons/eye-slash.svg";
import copyIcon from "../../assets/icons/copy.svg";
import { useTheme } from "../../hooks/useTheme.js";

const ViewSSHKeyForm = ({ keyData, initialEditing, onClose, onSave }) => {
    const [isEditing, setIsEditing] = useState(initialEditing);
    const [showPrivateKey, setShowPrivateKey] = useState(false);
    const [editedKey, setEditedKey] = useState({});
    const { darkMode } = useTheme();

    useEffect(() => {
        setEditedKey({ ...keyData });
        setIsEditing(initialEditing);
    }, [keyData, initialEditing]);

    if (!keyData) return null;

    const handleCopy = (text) => {
        navigator.clipboard.writeText(text);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEditedKey((prev) => ({ ...prev, [name]: value }));
    };

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/api/sshkeys/${keyData.id_sshkey}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(editedKey),
            });

            if (response.ok) {
                onSave();
            } else {
                const error = await response.json();
                alert(error.detail || "Failed to update SSH key");
            }
        } catch (err) {
            console.error("Error updating SSH key:", err);
        }
    };


    return (
        <div className={`${style.popupOverlay} ${darkMode ? style.dark : ''}`}>
            <div className={style.formWrapper}>
                <h2>{isEditing ? "Edit SSH Key" : "View SSH Key"}</h2>
                {isEditing ? (
                    <form onSubmit={handleSave}>
                        <input
                            type="text"
                            name="name"
                            placeholder="Name"
                            value={editedKey.name}
                            onChange={handleChange}
                            required
                        />
                        <div className="eyeContainer">
                            <input
                                type={showPrivateKey ? "text" : "password"}
                                name="private_key"
                                placeholder="Private Key"
                                value={editedKey.private_key}
                                onChange={handleChange}
                                required
                            />
                            <div className="eyeButtons">
                                <button type="button" onClick={() => setShowPrivateKey(!showPrivateKey)}
                                        className="eyeButton">
                                    <img src={showPrivateKey ? eyeSlashIcon : eyeIcon} alt="Toggle Private Key"/>
                                </button>
                            </div>
                        </div>
                        <input
                            type="text"
                            name="public_key"
                            placeholder="Public Key"
                            value={editedKey.public_key}
                            onChange={handleChange}
                        />
                        <input
                            type="text"
                            name="passphrase"
                            placeholder="Passphrase"
                            value={editedKey.passphrase}
                            onChange={handleChange}
                        />
                        <textarea
                            type="text"
                            name="notes"
                            placeholder="Notes"
                            value={editedKey.notes}
                            onChange={handleChange}
                        />
                        <div className={style.popupButtons}>
                            <button type="submit" className="button">
                                Save Changes
                            </button>
                            <button type="button" className="button" onClick={onClose}>
                                Cancel
                            </button>
                        </div>
                    </form>
                ) : (
                    <div className={`${style.view} ${darkMode ? style.dark : ''}`}>
                        <input
                            className={style.field}
                            type="text"
                            name="name"
                            placeholder="Name"
                            value={keyData.name}
                            readOnly
                        />
                        <div className={`${style.field} eyeContainer`}>
                            <input
                                type={showPrivateKey ? "text" : "password"}
                                name="private_key"
                                placeholder="Private Key"
                                value={keyData.private_key}
                                readOnly
                            />
                            <div className="eyeButtons">
                                <button type="button" onClick={() => setShowPrivateKey(!showPrivateKey)}
                                        className="eyeButton">
                                    <img src={showPrivateKey ? eyeSlashIcon : eyeIcon} alt="Toggle Private Key"/>
                                </button>
                                <button type="button" onClick={() => handleCopy(keyData.private_key)}
                                        className="eyeButton">
                                    <img src={copyIcon} alt="Copy Private Key"/>
                                </button>
                            </div>
                        </div>
                        <input
                            className={style.field}
                            type="text"
                            name="public_key"
                            placeholder="Public Key"
                            value={keyData.public_key}
                            readOnly
                        />
                        <input
                            className={style.field}
                            type="text"
                            name="passphrase"
                            placeholder="Passphrase"
                            value={keyData.passphrase}
                            readOnly
                        />
                        <textarea
                            className={style.field}
                            type="text"
                            name="notes"
                            placeholder="Notes"
                            value={keyData.notes}
                            readOnly
                        />
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
        </div>
    );
};

export default ViewSSHKeyForm;
