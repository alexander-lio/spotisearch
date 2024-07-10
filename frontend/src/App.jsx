import { useState, useEffect } from 'react'
import ContactList from './ContactList'
import './App.css'
import ContactForm from './ContactForm'

function App() {
  const [contacts, setContacts] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
   fetchContacts()
  }, [])

  const fetchContacts = async () => {
    const response = await fetch("http://127.0.0.1:8888/contacts")
    const data = await response.json()
    setContacts(data.contacts)
    console.log(data.contacts)
  };

  const closeModal = () => {
    setIsModalOpen(false)
  }

  const openCreateModal = (contact) => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchContacts()
  }

  return (
    <>
      <ContactList contacts={contacts} updateCallback={onUpdate}/>
      <button onClick={openCreateModal}>Input Artist</button>
      {isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <ContactForm updateCallback={onUpdate}/>
        </div>
      </div>

      }
    </>
  );

}

export default App
