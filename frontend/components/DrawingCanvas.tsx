import React, { useRef, useState, useEffect } from "react";

interface CanvasDrawProps {
  onStrokeEnd: (stroke: { xs: number[]; ys: number[] }) => void;
  onClear: () => void;
}

const CanvasDraw: React.FC<CanvasDrawProps> = ({ onStrokeEnd, onClear }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const contextRef = useRef<CanvasRenderingContext2D | null>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [points, setPoints] = useState<{ x: number; y: number }[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }
    canvas.width = 256 * 2; // Multiply by 2 for high DPI displays
    canvas.height = 256 * 2;
    canvas.style.width = "256px";
    canvas.style.height = "256px";

    const context = canvas.getContext("2d");
    if (!context) {
      return;
    }
    context.scale(2, 2); // Scale by 2 for high DPI displays
    context.lineCap = "round";
    context.strokeStyle = "black";
    context.lineWidth = 3;
    contextRef.current = context;
  }, []);

  const startDrawing = ({ nativeEvent }: React.MouseEvent) => {
    const { offsetX, offsetY } = nativeEvent as MouseEvent;
    contextRef.current?.beginPath();
    contextRef.current?.moveTo(offsetX, offsetY);
    setIsDrawing(true);
    setPoints([{ x: offsetX, y: offsetY }]);
  };

  const draw = ({ nativeEvent }: React.MouseEvent) => {
    if (!isDrawing) {
      return;
    }
    const { offsetX, offsetY } = nativeEvent as MouseEvent;
    contextRef.current?.lineTo(offsetX, offsetY);
    contextRef.current?.stroke();
    setPoints((prevPoints) => [...prevPoints, { x: offsetX, y: offsetY }]);
  };

  const endDrawing = () => {
    contextRef.current?.closePath();
    setIsDrawing(false);
    if (onStrokeEnd) {
      const xs = points.map((point) => Math.min(Math.max(point.x, 0), 255));
      const ys = points.map((point) => Math.min(Math.max(point.y, 0), 255));
      onStrokeEnd({ xs, ys });
    }
    setPoints([]);
  };

  const clearCanvas = () => {
    const context = contextRef.current;
    if (context) {
      context.clearRect(0, 0, context.canvas.width, context.canvas.height);
      if (onClear) {
        onClear();
      }
    }
  };


  return (
    <div className="flex flex-col items-center">
    <div className="border-4 border-black inline-block ">
    <canvas
      ref={canvasRef}
      onMouseDown={startDrawing}
      onMouseMove={draw}
      onMouseUp={endDrawing}
      className="bg-white block"
    />
    </div>
    <button onClick={clearCanvas} className="w-fit px-4 py-2 bg-blue-600 rounded mt-2">
        Clear
      </button>
    </div>
  );
};

export default CanvasDraw;
