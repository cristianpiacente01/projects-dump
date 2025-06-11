import { useState, useEffect } from "react";
import style from "./SSHKeyForm.module.css";
import eyeSlashIcon from "../../assets/icons/eye-slash.svg";
import eyeIcon from "../../assets/icons/eye.svg";
import { useTheme } from "../../hooks/useTheme.js";

const SSHKeyForm = ({ keyData, onClose, onSave }) => {
    const [name, setName] = useState("");
    const [private_key, setPrivateKey] = useState("");
    const [public_key, setPublicKey] = useState("");
    const [passphrase, setPassphrase] = useState("");
    const [notes, setNotes] = useState("");
    const [showPrivateKey, setShowPrivateKey] = useState(false);
    const { darkMode } = useTheme();

    useEffect(() => {
        if (keyData) {
            setName(keyData.name || "");
            setPrivateKey(keyData.private_key || "");
            setPublicKey(keyData.public_key || "");
            setPassphrase(keyData.passphrase || "");
            setNotes(keyData.notes || "");
        } else {
            setName("");
            setPrivateKey("");
            setPublicKey("");
            setPassphrase("");
            setNotes("");
        }
    }, [keyData]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const userRes = await fetch("/api/me", {
                credentials: "include",
            });
            if (!userRes.ok) throw new Error("Failed to get user");
            const user = await userRes.json();

            const res = await fetch(
                keyData && keyData.id_sshkey
                    ? `/api/sshkeys/${keyData.id_sshkey}`
                    : "/api/sshkeys/add",
                {
                    method: keyData && keyData.id_sshkey ? "PUT" : "POST",
                    credentials: "include",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                    id_user: user.id,
                    name,
                    private_key: private_key,
                    public_key: public_key,
                    passphrase,
                    notes,
                    }),
                }
                );

            if (res.ok) {
                onSave();
                onClose();
            } else {
                const error = await res.json();
                alert(error.detail || "Failed to save SSH key");
            }
        } catch (err) {
            console.error("Error submitting SSH key:", err);
        }
    };


    return (
        <div className={`${style.popupOverlay} ${darkMode ? style.dark : ''}`}>
            <div className={style.formWrapper}>
                <h2>Add New SSH Key</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                    <div className="eyeContainer">
                        <input
                            type={showPrivateKey ? "text" : "password"}
                            name="password"
                            placeholder="Private Key"
                            value={private_key}
                            onChange={(e) => setPrivateKey(e.target.value)}
                            required
                        />
                        <div className="eyeButtons">
                            <button type="button" onClick={() => setShowPrivateKey(!showPrivateKey)}
                                    className="eyeButton">
                                <img src={showPrivateKey ? eyeSlashIcon : eyeIcon} alt="Toggle Password Visibility"/>
                            </button>
                        </div>
                    </div>
                    <input
                        type="text"
                        placeholder="Public Key"
                        value={public_key}
                        onChange={(e) => setPublicKey(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Passphrase"
                        value={passphrase}
                        onChange={(e) => setPassphrase(e.target.value)}
                    />
                    <textarea
                        placeholder="Notes"
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                    ></textarea>
                    <div className={style.popupButtons}>
                        <button type="submit" className="button">
                            Save
                        </button>
                        <button type="button" className="button" onClick={onClose}>
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default SSHKeyForm;
