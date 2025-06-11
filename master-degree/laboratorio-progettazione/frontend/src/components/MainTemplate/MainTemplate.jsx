import { useLocation } from "react-router-dom";
import Header from '../Header/Header.jsx';
import Footer from '../Footer/Footer.jsx';

function MainTemplate(props) {
    const { children, logo } = props;
    const location = useLocation();

    if (location.pathname === "/registration") {
        return children;
    }

    if (location.pathname === "/passphrase") {
        return children;
    }

    if (location.pathname === "/verify") {
        return children;
    }

    if (location.pathname === "/recover-password") {
        return children;
    }

    if (location.pathname === "/enter-otp") {
        return children;
    }

    return (
        <div className="layout">
            <Header logo={logo}/>
            <main>
                <div className="my-5">
                    {children}
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default MainTemplate;