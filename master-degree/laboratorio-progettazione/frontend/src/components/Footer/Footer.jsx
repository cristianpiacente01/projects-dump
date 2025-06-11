import style from "./Footer.module.css";
import unimib from "../../assets/images/unimib.png";
import disco from "../../assets/images/disco.png";

function Footer() {
    return (
        <footer className={style.footer}>
            <p>&copy; 2025 PassGuard. All rights reserved.</p>
            <div className={style.iconContainer}>
                <div id={style.disco} className={style.footerImage}>
                    <a href="https://www.disco.unimib.it/it" target="_blank">
                        <img src={disco} alt="disco"/>
                    </a>
                </div>
                <div id={style.unimib} className={style.footerImage}>
                    <a href="https://www.unimib.it/" target="_blank">
                        <img src={unimib} alt="unimib"/>
                    </a>
                </div>
            </div>
        </footer>
    )
}

export default Footer;