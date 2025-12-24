import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [longUrl, setLongUrl] = useState<string>('');
  const [shortUrl, setShortUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      console.log("longUrl submitted:", longUrl);
      const response = await fetch('http://localhost:3000/dev/create', {
        method: 'POST',
        headers: {
          'Content-Type' : 'application/json'
        },
        body: JSON.stringify({
          url: longUrl
        }),
      });
      const data = await response.json();

      // update state with short url from backend
      setShortUrl(data.shortUrl);
    } catch (error) {
      console.error('Error creating short URL from backend or connecting backend:', error);
      alert('Make sure serverless backend is running on http://localhost:3000');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={ { padding: '50px', textAlign: 'center', fontFamily: 'Asans-serif' } }>
      <h1>URL Shortener</h1>
      <form onSubmit={ handleSubmit }>
        <input
          type="url"
          placeholder="Enter long URL here ..."
          value={ longUrl }
          onChange={ (e) => setLongUrl(e.target.value) } //updates state here
          required
          style={{padding: '10px', width: '30px'}}
        />
        <button type="submit" disabled={ isLoading } style={{padding: '10px', marginLeft: '10px'}}>
          { isLoading ? 'Shortening...' : 'Shorten URL' }
        </button>
      </form>
      {/* Conditionally render the short URL if it exists */}
      { shortUrl && (
        <div style={{ marginTop: '20px' }}>
          <p>Shortened URL:</p>
          <a href={ shortUrl } target="_blank" rel="noopener noreferrer">
            { shortUrl }
          </a>
        </div>
      ) }
    </div>
  );

}

export default App
