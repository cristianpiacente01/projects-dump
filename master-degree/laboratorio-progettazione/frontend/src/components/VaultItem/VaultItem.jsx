import React, { useState } from 'react';
import style from './VaultItem.module.css';
import menu from '../../assets/icons/menu.png';
import keyIcon from '../../assets/icons/key.png';
import credentialsIcon from '../../assets/icons/credentials.png';
import { useTheme } from "../../hooks/useTheme.js";

const VaultItem = ({ item, index, onEdit, onView, onDelete }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const { darkMode } = useTheme();

    const toggleMenu = (event) => {
        event.stopPropagation();
        setIsMenuOpen(!isMenuOpen);
    };

    const isSSH = item.type === "sshKey";
    const title = isSSH ? item.name : item.url;
    const subtitle = isSSH ? item.public_key : item.username;
    const icon = isSSH ? keyIcon : credentialsIcon;

    return (
        <div className={`${style.wrapper} ${darkMode ? style.dark : ''}`}>
            <div
                className={style.itemContainer}
                onClick={(e) => {
                    if (e.target.closest(`.${style.itemButton}`)) return;
                    onView(item);
                }}
            >
                <div className={style.itemContent}>
                    <div className={style.icon}>
                        <img src={icon} alt="icon" className={style.imgIcon}/>
                    </div>
                    <div className={style.infoContainer}>
                        <div className={style.title}>{title}</div>
                        <div className={style.subtitle}>{subtitle}</div>
                    </div>
                </div>
            </div>
            <div className={style.itemButton}>
                <img src={menu} alt="Menu" className={style.menuIcon} onClick={toggleMenu}/>
                {isMenuOpen && (
                    <div className={style.menuPopup}>
                        <button className={style.editButton}onClick={(event) => {
                            event.stopPropagation();
                            onEdit(index);
                            setIsMenuOpen(false);
                        }}>Edit
                        </button>
                        <button className={style.deleteButton} onClick={(event) => {
                            event.stopPropagation();
                            onDelete(index);
                            setIsMenuOpen(false);
                        }}>Delete
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default VaultItem;