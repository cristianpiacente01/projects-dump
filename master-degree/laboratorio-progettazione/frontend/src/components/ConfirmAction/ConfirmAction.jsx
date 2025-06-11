import style from "./ConfirmAction.module.css";
import { useTheme } from "../../hooks/useTheme.js";

const ConfirmAction = ({ isOpen, onClose, onConfirm }) => {
    const { darkMode } = useTheme();
    if (!isOpen) return null;

    return (
        <div className={`${style.popupOverlay} ${darkMode ? style.dark : ''}`}>
            <div className={style.popupContent}>
                <h3>Are you sure?</h3>
                <p>This action cannot be undone.</p>
                <div className={style.popupButtons}>
                    <button className="redButton" onClick={onConfirm}>Confirm</button>
                    <button className="button" onClick={onClose}>Cancel</button>
                </div>
            </div>
        </div>
    );
};

export default ConfirmAction;