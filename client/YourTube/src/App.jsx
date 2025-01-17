import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {

  return (
    <>
      <h1>YourTube🫵🤓</h1>

      <form>
        <label htmlFor="youtubeUrl"></label>
        <input type="text" id='youtubeUrl' name='youtubeUrl'/>

        <label htmlFor='submit'></label>
        <input type="submit" id='urlSubmit' name='urlSubmit'/>
      </form>
    </>
  )
}

export default App
