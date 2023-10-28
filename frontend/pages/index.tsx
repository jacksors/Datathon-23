import { useEffect, useState, useRef } from 'react';
import DrawingCanvas from '../components/DrawingCanvas'
import WebSocketManager from "../utility/WebSocketManager";

export default function Home() {
  const url = 'ws://localhost:8000/ws/stroke/';
  const [message, setMessage] = useState({});
  const wsManagerRef = useRef<WebSocketManager | null>(null);

  useEffect(() => {
    const handleMessage = (message : any) => {
      console.log('Received message in App component:', message);
      setMessage(message);
    };

    // Initialize the WebSocketManager and store it in the ref
    wsManagerRef.current = new WebSocketManager(url, handleMessage);
  }, [url]);

  const handleStrokeEnd = (stroke : any) => {
    // Use the current value of the ref to access the WebSocketManager instance
    wsManagerRef.current!.sendStroke(stroke);
  };

  const handleClear = () => {
    // Use the current value of the ref to access the WebSocketManager instance
    wsManagerRef.current!.sendClear();
  };

  return (
    <main
      className="h-[calc(100dvh)] w-screen flex flex-col justify-center items-center bg-neutral-900"
    >
      <p className="text-4xl font-bold text-center pb-2">
        Let's Draw!
      </p>
      <DrawingCanvas onStrokeEnd={handleStrokeEnd} onClear={handleClear}/>
    </main>
  )
}
