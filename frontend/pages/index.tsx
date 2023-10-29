import { useEffect, useState, useRef } from 'react';
import DrawingCanvas from '../components/DrawingCanvas'
import WebSocketManager from "../utility/WebSocketManager";
import PredictionCheckerModal from '../components/PredictionCheckerModal';

export default function Home() {
  const url = "ws://quotesbot.xyz:8000/ws/stroke/";
  const [message, setMessage] = useState<string>('Start drawing to get a prediction!');
  const [probability, setProbability] = useState<number>(0);
  const [isModalOpen, setModalOpen] = useState(false);
  const wsManagerRef = useRef<WebSocketManager | null>(null);

  useEffect(() => {
    const handleMessage = (message: any) => {
      console.log('Received message in App component:', message);
      setMessage(message.prediction);
      setProbability(message.probability * 100);
    };

    // Initialize the WebSocketManager and store it in the ref
    wsManagerRef.current = new WebSocketManager(url, handleMessage);
  }, [url]);

  const handleStrokeEnd = (stroke: any) => {
    // Use the current value of the ref to access the WebSocketManager instance
    wsManagerRef.current!.sendStroke(stroke);
  };

  const handleClear = () => {
    // Use the current value of the ref to access the WebSocketManager instance
    wsManagerRef.current!.sendClear();
    setMessage('Start drawing to get a prediction!');
    setProbability(0);
  };

  const handleSaveStroke = (name: string) => {
    // Use the current value of the ref to access the WebSocketManager instance
    wsManagerRef.current!.saveStroke(name);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  return (
    <main
      className="h-[calc(100dvh)] w-screen flex flex-col justify-center items-center bg-neutral-900"
    >
      <p className="text-4xl font-bold text-center pb-2">
        Let's Draw!
      </p>
      <p className="text-2xl text-center pb-2">
        {message.toString()}
      </p>
      <p className="text-2xl text-center pb-2">
        {probability != 0 ? "Confidence: " + probability.toFixed(2).toString() + "%" : ""}
      </p>
      <DrawingCanvas onStrokeEnd={handleStrokeEnd} onClear={handleClear} />
      <PredictionCheckerModal
        prediction={message}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSave={handleSaveStroke}
      />
      {
        message && (probability != 0) && (probability < 50) ?
          <button
            className="fixed mb-5 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors duration-200 ease-in-out bottom-0"
            onClick={() => setModalOpen(true)}
          >
            <p>Provide Feedback</p>
          </button>
          : <></>
      }
    </main>
  )
}
