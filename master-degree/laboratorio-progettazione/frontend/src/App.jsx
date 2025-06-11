import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainTemplate from './components/MainTemplate/MainTemplate.jsx';
import Registration from './views/Registration/Registration.jsx';
import Passphrase from './views/Passphrase/Passphrase.jsx';
import Verify from './views/Verify/Verify.jsx';
import Vault from './views/Vault/Vault.jsx';
import Login from './views/Login/Login.jsx';
import Logo from './assets/images/logo.png';
import Settings from './views/Settings/Settings.jsx';
import EnterOTP from './views/EnterOTP/EnterOTP.jsx';
import RecoverPassword from './views/RecoverPassword/RecoverPassword.jsx';
import { useTheme } from "./hooks/useTheme.js";

function App() {
    const { darkMode } = useTheme();
    return (
        <div className={darkMode ? 'dark-mode' : 'light-mode'}>
            <BrowserRouter>
                <MainTemplate logo={Logo}>
                    <Routes>
                        <Route path="/" element={<Login/>}/>
                        <Route path="/registration" element={<Registration/>}/>
                        <Route path="/passphrase" element={<Passphrase/>}/>
                        <Route path="/verify" element={<Verify/>}/>
                        <Route path="/vault" element={<Vault/>}/>
                        <Route path="/settings" element={<Settings/>}/>
                        <Route path="/enter-otp" element={<EnterOTP/>}/>
                        <Route path="/login" element={<Login/>}/>
                        <Route path="/recover-password" element={<RecoverPassword/>}/>
                    </Routes>
                </MainTemplate>
            </BrowserRouter>
        </div>
    );
}

export default App;