import {useState} from "react";

const ContactForm = ({updateCallback}) => {
    const [artist, setArtist] = useState("")

    const onSubmit = async (e) => {
        e.preventDefault()
        
        const data = {
            artist
        }
        const url = "http://127.0.0.1:8888/create_contact"
        const options = {
            method: "POST",
            headers: {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify(data)
        }

        const response = await fetch(url, options)
        if (response.status != 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCallback()
        }
    }
    return ( 
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="artist">artist:</label>
                <input 
                    type="text" 
                    id="artist" 
                    value={artist} 
                    onChange={(e) => setArtist(e.target.value)}
                />
            </div>
            <button type="submit">Search Top Tracks</button>
        </form>
    );
};

export default ContactForm