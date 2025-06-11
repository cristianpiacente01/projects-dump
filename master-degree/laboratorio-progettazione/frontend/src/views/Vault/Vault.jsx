import { useEffect, useState } from "react";
import style from "./Vault.module.css";
import plus from "../../assets/icons/plus.png";
import empty from "../../assets/images/empty.png";
import credentials from "../../assets/icons/credentialsColor.png";
import key from "../../assets/icons/keyColor.png";
import VaultItem from "../../components/VaultItem/VaultItem.jsx";
import ConfirmAction from "../../components/ConfirmAction/ConfirmAction.jsx";
import ViewCredentialForm from "../../components/ViewCredentialForm/ViewCredentialForm.jsx";
import CredentialsForm from "../../components/CredentialsForm/CredentialsForm.jsx";
import SSHKeyForm from "../../components/SSHKeyForm/SSHKeyForm.jsx";
import ViewSSHKeyForm from "../../components/ViewSSHKeyForm/ViewSSHKeyForm.jsx";
import { useTheme } from "../../hooks/useTheme.js";

const formComponents = {
    credentials: CredentialsForm,
    sshkey: SSHKeyForm,
};

const getFormProps = (formType, editingIndex, items) => {
    if (formType === "credentials") {
        return {
            credential: editingIndex !== null ? items[editingIndex] : null,
        };
    }
    if (formType === "sshkey") {
        return {
            sshKey: editingIndex !== null ? items[editingIndex] : null,
        };
    }
    return {};
};

const Vault = () => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [items, setItems] = useState([]);
    const [actionIndex, setActionIndex] = useState(null);
    const [editingIndex, setEditingIndex] = useState(null);
    const [showConfirm, setShowConfirm] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [formType, setFormType] = useState(null);
    const [isAddOpen, setIsAddOpen] = useState(false);
    const [viewingItem, setViewingItem] = useState(null);
    const { darkMode } = useTheme();

    const confirmAction = async () => {
        if (actionIndex !== null) {
            const item = items[actionIndex];
            console.log("Elemento selezionato per eliminazione:", item);
            // Determine the correct endpoint depending on the type
            const isSSHKey = item.type === "sshKey";
            const endpoint = isSSHKey
                ? `/api/sshkeys/${item.id_sshkey}`
                : `/api/credentials/${item.id_credential}`;

            try {
                const res = await fetch(endpoint, {
                    method: "DELETE",
                    credentials: "include",
                });

                if (res.ok) {
                    setItems((prev) => prev.filter((_, index) => index !== actionIndex));
                } else {
                    const error = await res.json();
                    alert(error.detail || `Failed to delete ${isSSHKey ? "SSH key" : "credential"}`);
                }
            } catch (err) {
                console.error(`Error deleting ${isSSHKey ? "SSH key" : "credential"}:`, err);
            }

            setActionIndex(null);
            setShowConfirm(false);
        }
    };

    const fetchVaultItems = async () => {
        try {
            const [credsRes, keysRes] = await Promise.all([
                fetch("/api/credentials/decrypted", { credentials: "include" }),
                fetch("/api/sshkeys/decrypted", { credentials: "include" })
            ]);

            if (!credsRes.ok || !keysRes.ok) {
                throw new Error("Failed to fetch credentials or SSH keys");
            }

            const credsData = await credsRes.json();
            const keysData = await keysRes.json();

            const combinedItems = [
                ...credsData.map((item) => ({ ...item, type: "credential" })),
                ...keysData.map((item) => ({ ...item, type: "sshKey" }))
            ];

            setItems(combinedItems);
        } catch (err) {
            console.error("Error fetching vault items:", err);
        }
    };

    const handleAddItem = () => {
        fetchVaultItems();
        setIsPopupOpen(false);
        setEditingIndex(null);
        setFormType(null);
    };

    const handleEdit = (index) => {
        const item = items[index];
        if (item.type === "sshKey") {
            setViewingItem({ type: "sshKey", data: item });
            setFormType("sshkey");
        } else {
            setViewingItem({ type: "credential", data: item });
            setFormType("credentials");
        }
        setIsEditing(true);
    };

    const handleView = (item) => {
        if (item.type === "sshKey") {
            setViewingItem({ type: "sshKey", data: item });
            setFormType("sshkey");
        } else {
            setViewingItem({ type: "credential", data: item });
            setFormType("credentials");
        }
        setIsEditing(false);
    };

    const handleDelete = (index) => {
        setActionIndex(index);
        setShowConfirm(true);
    };

    const toggleAdd = (event) => {
        event.stopPropagation();
        setIsAddOpen(!isAddOpen);
    };

    useEffect(() => {
        fetchVaultItems();
    }, []);

    const renderPopupForm = () => {
        if (!isPopupOpen || !formType) return null;
        const FormComponent = formComponents[formType];
        if (!FormComponent) return null;
        return (
            <FormComponent
                {...getFormProps(formType, editingIndex, items)}
                onClose={() => {
                    setIsPopupOpen(false);
                    setEditingIndex(null);
                    setFormType(null);
                }}
                onSave={handleAddItem}
            />
        );
    };

    return (
        <div className={`${darkMode ? style.dark : ''}`}>
            <div className="container">
                <div className={style.header}>
                    <h1>Your Vault</h1>
                    <div className={style.itemButton}>
                        <button className="button" onClick={toggleAdd}>
                            <img src={plus} alt="Add item" className={style.menuIcon}/>
                        </button>
                        {isAddOpen && (
                            <div className={style.menuPopup}>
                                <button onClick={() => {
                                    setFormType("credentials");
                                    setIsPopupOpen(true);
                                    setIsAddOpen(false);
                                }}>
                                <span className={style.menuButtonContent}>
                                    <img src={credentials} alt="Credentials"/>
                                    <span>Credentials</span>
                                </span>
                                </button>
                                <button onClick={() => {
                                    setFormType("sshkey");
                                    setIsPopupOpen(true);
                                    setIsAddOpen(false);
                                }}>
                                <span className={style.menuButtonContent}>
                                    <img src={key} alt="SSH Key"/>
                                    <span>SSH Key</span>
                                </span>
                                </button>
                            </div>
                        )}
                    </div>
                </div>
                <div className="row justify-content-center">
                    <div className="col">
                        {items.length === 0 ? (
                            <div className={style.emptyState}>
                                <img src={empty} alt="No items"/>
                                <p>No items to show</p>
                            </div>
                        ) : (
                            <div className={style.container}>
                                {items.map((item, index) => (
                                    <VaultItem
                                        key={index}
                                        index={index}
                                        item={item}
                                        onEdit={handleEdit}
                                        onView={handleView}
                                        onDelete={handleDelete}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                {renderPopupForm()}

                {viewingItem && formType === "sshkey" && (
                    <ViewSSHKeyForm
                        keyData={viewingItem.data}
                        isEditing={isEditing}
                        setIsEditing={setIsEditing}
                        onClose={() => {
                            setViewingItem(null);
                            setIsEditing(false);
                            setFormType(null);
                        }}
                        onSave={() => {
                            setViewingItem(null);
                            setIsEditing(false);
                            setFormType(null);
                            fetchVaultItems();
                        }}
                    />
                )}

                {viewingItem && formType === "credentials" && (
                    <ViewCredentialForm
                        credential={viewingItem.data}
                        isEditing={isEditing}
                        onClose={() => {
                            setViewingItem(null);
                            setIsEditing(false);
                        }}
                        onSave={() => {
                            setViewingItem(null);
                            setIsEditing(false);
                        }}
                    />
                )}

                <ConfirmAction
                    isOpen={showConfirm}
                    onClose={() => setShowConfirm(false)}
                    onConfirm={confirmAction}
                />
            </div>
        </div>
    );
};

export default Vault;