import React from "react";
import "../styles/Idea.css"

function Idea({ idea, onDelete }) {
    const formattedDate = new Date(idea.created_at).toLocaleDateString("en-US")

    return (
        <div className="idea-container">
            <p className="idea-title">{idea.title}</p>
            <p className="idea-content">{idea.content}</p>
            <p className="idea-date">{formattedDate}</p>
            <button className="delete-button" onClick={() => onDelete(idea.id)}>
                Delete
            </button>
        </div>
    );
}

export default Idea