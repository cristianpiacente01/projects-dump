import { useState } from "react";
import style from "./PasswordGenerator.module.css";
import generate from "../../assets/icons/generate.png";
import copyIcon from "../../assets/icons/copy.svg";
import { useTheme } from "../../hooks/useTheme.js";

const API_BASE = "/api";

const PasswordGenerator = ({ setShowGenerator, onUse }) => {
    const [tab, setTab] = useState("password");
    const [generatedValue, setGeneratedValue] = useState("");
    const [includeUppercase, setIncludeUppercase] = useState(true);
    const [includeLowercase, setIncludeLowercase] = useState(true);
    const [includeNumbers, setIncludeNumbers] = useState(true);
    const [includeSymbols, setIncludeSymbols] = useState(true);
    const [wordCount, setWordCount] = useState(4);
    const { darkMode } = useTheme();

    const generatePassword = async () => {
        try {
            const params = new URLSearchParams({
                length: "16",
                uppercase: includeUppercase,
                lowercase: includeLowercase,
                numbers: includeNumbers,
                symbols: includeSymbols,
            });

            const res = await fetch(`${API_BASE}/generate-password?${params.toString()}`, {
                credentials: "include",
            });
            if (!res.ok) throw new Error("Errore generazione password");
            const { password } = await res.json();
            setGeneratedValue(password);
        } catch (e) {
            alert(e.message);
        }
    };

    const generatePassphrase = async () => {
        try {
            const res = await fetch(
             `${API_BASE}/generate-passphrase?words=${wordCount}`, {
                    credentials: "include",
            });
            if (!res.ok) throw new Error("Errore generazione passphrase");
            const { passphrase } = await res.json();
            setGeneratedValue(passphrase);
        } catch (e) {
            alert(e.message);
        }
    };


const handleGenerate = () => {
  if (tab === "password") {
    generatePassword();
  } else {
    generatePassphrase();
  }
};


    const handleCopy = () => {
        navigator.clipboard.writeText(generatedValue);
    };

    return (
        <div className={`${style.popupOverlay} ${darkMode ? style.dark : ''}`}>
            <div className={style.generatorPopup}>
                <h2>Generator</h2>
                <div className={style.tabs}>
                    <div className={`${style.tab} ${tab === "password" ? style.active : ""}`}
                         onClick={() => setTab("password")}>Password
                    </div>
                    <div className={`${style.tab} ${tab === "passphrase" ? style.active : ""}`}
                         onClick={() => setTab("passphrase")}>Passphrase
                    </div>
                </div>

                <div className={style.result}>
                    {tab === "password" ? (
                        <input type="text" readOnly value={generatedValue} className={style.resultField}/>
                    ) : (
                        <textarea readOnly value={generatedValue} className={style.resultField}/>
                    )}
                    <div className={style.actions}>
                        <button onClick={handleGenerate} className={style.actionButton}>
                            <img src={generate} alt="Generate"/></button>
                        <button onClick={handleCopy} className={style.copyButton}>
                            <img src={copyIcon} alt="Copy"/>
                        </button>
                    </div>
                    {tab === "password" ? (<span>Length fixed: 16 characters</span>) : ("")}
                </div>

                {tab === "password" ? (
                    <div className={style.optionWrapper}>
                        <h6>Options</h6>
                        <div className={style.options}>
                            <label><input type="checkbox" checked={includeUppercase}
                                        onChange={() => setIncludeUppercase(!includeUppercase)} /> A-Z</label>
                            <label><input type="checkbox" checked={includeLowercase}
                                        onChange={() => setIncludeLowercase(!includeLowercase)} /> a-z</label>
                            <label><input type="checkbox" checked={includeNumbers}
                                        onChange={() => setIncludeNumbers(!includeNumbers)} /> 0-9</label>
                            <label><input type="checkbox" checked={includeSymbols}
                                        onChange={() => setIncludeSymbols(!includeSymbols)} /> Special symbols</label>
                        </div>
                    </div>
                ) : (
                    <div className={style.optionWrapper}>
                        <h6>Number of words</h6>
                        <input
                            type="number"
                            min={4}
                            max={10}
                            value={wordCount}
                            onChange={(e) => setWordCount(Number(e.target.value))}
                        />
                        <span>The value must be between 4 and 10.</span>
                    </div>
                )}

                <div className={style.popupButtons}>
                    <button className="button" onClick={() => onUse(generatedValue)} disabled={!generatedValue}>
                        Use this {tab === "password" ? "password" : "passphrase"}
                    </button>
                    <button className="button" onClick={() => setShowGenerator(false)}>
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};

export default PasswordGenerator;