import { useEffect, useState, useRef } from 'react';
import DrawingCanvas from '../components/DrawingCanvas'
import WebSocketManager from "../utility/WebSocketManager";
import PredictionCheckerModal from '../components/PredictionCheckerModal';
import { FaGithub } from 'react-icons/fa';
import Head from 'next/head';

export default function Home() {
  const url = "wss://quotesbot.xyz/ws/stroke/";
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
      <Head>
        <title>DoodleDuel!</title>
        <meta name="description" content="Datathon 23" />
        <link rel="apple-touch-icon" sizes="57x57" href="/apple-icon-57x57.png" />
        <link rel="apple-touch-icon" sizes="60x60" href="/apple-icon-60x60.png" />
        <link rel="apple-touch-icon" sizes="72x72" href="/apple-icon-72x72.png" />
        <link rel="apple-touch-icon" sizes="76x76" href="/apple-icon-76x76.png" />
        <link rel="apple-touch-icon" sizes="114x114" href="/apple-icon-114x114.png" />
        <link rel="apple-touch-icon" sizes="120x120" href="/apple-icon-120x120.png" />
        <link rel="apple-touch-icon" sizes="144x144" href="/apple-icon-144x144.png" />
        <link rel="apple-touch-icon" sizes="152x152" href="/apple-icon-152x152.png" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-icon-180x180.png" />
        <link rel="icon" type="image/png" sizes="192x192"  href="/android-icon-192x192.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="msapplication-TileColor" content="#ffffff" />
        <meta name="msapplication-TileImage" content="/ms-icon-144x144.png" />
        <meta name="theme-color" content="#ffffff" />
        <meta property="og:title" content="DoodleDuel!" />
        <meta charSet='UTF-8' />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>
      <p className="text-4xl font-bold text-center pb-2">
        Let's Duel!
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
      <FaGithub
                onClick={() =>
                    window.open(
                        'https://github.com/jacksors/Datathon-23'
                    )
                }
        className="fixed bottom-0 left-0 mb-2 ml-2 cursor-pointer h-7 w-7"
            />
    </main>
  )
}
