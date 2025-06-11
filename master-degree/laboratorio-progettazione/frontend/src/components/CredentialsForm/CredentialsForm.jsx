import { useState, useEffect } from "react";
import style from "./CredentialsForm.module.css";
import eyeSlashIcon from "../../assets/icons/eye-slash.svg";
import eyeIcon from "../../assets/icons/eye.svg";
import generate from "../../assets/icons/generate.png";
import PasswordGenerator from "../../components/PasswordGenerator/PasswordGenerator.jsx";
import { useTheme } from "../../hooks/useTheme.js";

const CredentialsForm = ({ credential, onClose, onSave }) => {
    const [url, setUrl] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [notes, setNotes] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showGenerator, setShowGenerator] = useState(false);
    const { darkMode } = useTheme();

    useEffect(() => {
        if (credential) {
            setUrl(credential.url);
            setUsername(credential.username);
            setPassword(credential.password);
            setNotes(credential.notes);
        }
    }, [credential]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const userRes = await fetch("/api/me", {
                credentials: "include",
            });
            if (!userRes.ok) throw new Error("Failed to get user");
            const user = await userRes.json();

            const res = await fetch(
                credential ? `/api/credentials/${credential.id_credential}` : "/api/credentials/add",
                {
                    method: credential ? "PUT" : "POST",
                    credentials: "include",
                    headers: {
                    "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                    ...(credential ? {} : { id_user: user.id }), // Only send id_user on create
                    url,
                    username,
                    password,
                    notes,
                    }),
                }
                );

            if (res.ok) {
                onSave();
                onClose();
            } else {
                const error = await res.json();
                alert(error.detail || "Failed to save credential");
            }
        } catch (err) {
            console.error("Error submitting credential:", err);
        }
    };

    return (
        <div className={`${style.popupOverlay} ${darkMode ? style.dark : ''}`}>
            <div className={style.formWrapper}>
                <h2>{credential ? "Edit Credential" : "Add New Credential"}</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="URL"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        required
                    />
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <div className="eyeContainer">
                        <input
                            type={showPassword ? "text" : "password"}
                            name="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <div className="eyeButtons">
                            <button type="button" onClick={() => setShowPassword(!showPassword)}
                                    className="eyeButton">
                                <img src={showPassword ? eyeSlashIcon : eyeIcon} alt="Toggle Password Visibility"/>
                            </button>
                            <button onClick={() => setShowGenerator(true)} className={style.generateButton}>
                                <img src={generate} alt="Generate Password"/>
                            </button>
                        </div>
                    </div>
                    <textarea
                        placeholder="Notes"
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                    ></textarea>
                    <div className={style.popupButtons}>
                        <button type="submit" className="button">
                            {credential ? "Save Changes" : "Save"}
                        </button>
                        <button type="button" className="button" onClick={onClose}>
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
            {showGenerator && (
                <PasswordGenerator
                    setShowGenerator={setShowGenerator}
                    onClose={() => setShowGenerator(false)}
                    onUse={(generated) => {
                        setPassword(generated);
                        setShowGenerator(false);
                    }}
                />
            )}
        </div>
    );
};

export default CredentialsForm;