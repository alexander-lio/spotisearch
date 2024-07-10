import React from "react"

const ContactList = ({contacts}) => {
    return <div>
        <h2>Top Tracks</h2>
        <table>
            <tbody>
                {contacts.map((contact) => (
                    <tr key={contact.id}>
                        <td>{contact.id + ".      " + contact.track}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default ContactList