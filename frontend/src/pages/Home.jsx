import { useState, useEffect } from "react";
import api from "../api";
import Idea from "../components/Idea"
import "../styles/Home.css"

function Home() {
    const [ideas, setIdeas] = useState([]);
    const [content, setContent] = useState("");
    const [title, setTitle] = useState("");

    useEffect(() => {
        getIdeas();
    }, []);

    const getIdeas = () => {
        api
            .get("/api/ideas/")
            .then((res) => res.data)
            .then((data) => {
                setIdeas(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const deleteIdea = (id) => {
        api
            .delete(`/api/ideas/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Idea deleted!");
                else alert("Failed to delete idea.");
                getIdeas();
            })
            .catch((error) => alert(error));
    };

    const createIdea = (e) => {
        e.preventDefault();
        api
            .post("/api/ideas/", { content, title })
            .then((res) => {
                if (res.status === 201) alert("Idea created!");
                else alert("Failed to make idea.");
                getIdeas();
            })
            .catch((err) => alert(err));
    };

    return (
        <div>
            <div>
                <h2>Ideas</h2>
                {ideas.map((idea) => (
                    <Idea idea={idea} onDelete={deleteIdea} key={idea.id} />
                ))}
            </div>
            <h2>Create an Idea</h2>
            <form onSubmit={createIdea}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="content">Content:</label>
                <br />
                <textarea
                    id="content"
                    name="content"
                    required
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                ></textarea>
                <br />
                <input type="submit" value="Submit"></input>
            </form>
        </div>
    );
}

export default Home;