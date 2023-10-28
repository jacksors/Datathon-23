import Image from 'next/image'
import { Inter } from 'next/font/google'
import DrawingCanvas from '../components/DrawingCanvas'
import WebSocketManager from '../utility/WebSocketManager'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  const wsManager = new WebSocketManager('ws://your-websocket-server-url');

  const handleStrokeEnd = (stroke: { xs: number[]; ys: number[] }) => {
    wsManager.sendStroke(stroke);
  };

  const handleClear = () => {
    wsManager.sendClear();
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
