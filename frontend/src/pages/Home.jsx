import { useState, useEffect } from "react";
import api from "../api";
import Idea from "../components/Idea"
import PrimarySearchAppBar from "../components/AppBar";
import "../styles/Home.css"

function Home() {
    const [ideas, setIdeas] = useState([]);
    const [youtubeUrl, setYoutubeUrl] = useState("");
    const [userPrompt, setUserPrompt] = useState("")
    const [numIdeas, setNumIdeas] = useState(1);


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

    const createIdea = ( title, content ) => {
        api
            .post("/api/ideas/", { title, content })
            .then((res) => {
                if (res.status === 201) console.log("Idea created!");
                else console.error("Failed to make idea.");
            })
            .catch((err) => alert(err));
    };


    const generateIdeas = async (e) => {
        e.preventDefault();

        const requestData = {
            youtube_url: youtubeUrl,
            num_ideas: numIdeas,
        }

        if (userPrompt) {
            requestData.user_prompt = userPrompt
        }

        try {
            const response = await api.post("/api/generate-ideas/", requestData);

            if (response.status === 200) {
                const generatedIdeas = response.data.ideas;
                generatedIdeas.forEach(async (idea) => {
                    createIdea( idea.idea_title, idea.idea_content )
                });
                setYoutubeUrl("");
                setNumIdeas(1);
                getIdeas();
                alert("Ideas generated!")
            } else {
                alert("Failed to generate ideas.");
            }
        } catch (err) {
            alert(`An error occurred: ${err.message}`);
            if (err.response && err.response.data) {
              console.error("Server error details:", err.response.data);
            }
        }
    };


    return (
        
        <div>
            <PrimarySearchAppBar/>
            <div>
                <h2>Ideas</h2>
                {ideas.map((idea) => (
                    <Idea idea={idea} onDelete={deleteIdea} key={idea.id} />
                ))}
            </div>
            <h2>Generate Ideas from YouTube</h2>
            <form onSubmit={generateIdeas}>
                <label htmlFor="youtubeUrl">YouTube URL:</label>
                <input
                    type="text"
                    id="youtubeUrl"
                    value={youtubeUrl}
                    onChange={(e) => setYoutubeUrl(e.target.value)}
                    required
                />
                <br />
                <label htmlFor="prompt">Prompt:</label>
                <input
                    type="text"
                    id="prompt"
                    value={userPrompt}
                    onChange={(e) => setUserPrompt(e.target.value)}
                    max = "300"
                />
                <br />
                <label htmlFor="numIdeas">Number of Ideas:</label>
                <input
                    type="number"
                    id="numIdeas"
                    value={numIdeas}
                    onChange={(e) => setNumIdeas(parseInt(e.target.value, 10) || 1)}
                    min="1"
                    max="10"
                    required
                />
                <br />
                <button type="submit">Generate</button>
            </form>
        </div>
    );
}


export default Home;