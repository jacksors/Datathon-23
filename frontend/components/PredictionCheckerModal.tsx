import React, { useState } from 'react';

interface Props {
  prediction: string;
  isOpen: boolean;
  onClose: () => void;
}

function PredictionCheckerModal({ prediction, isOpen, onClose } : Props) {
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [actualDrawing, setActualDrawing] = useState('');

  const handleConfirmation = (answer : boolean | null) => {
    setIsCorrect(answer);
    if (answer) {
      alert('Great! The prediction was correct.');
      onClose();
      setIsCorrect(null);
    }
  };

  const handleActualDrawingInput = (e : any) => {
    setActualDrawing(e.target.value);
  };

  const handleSubmit = () => {
    alert(`Got it! You actually drew a ${actualDrawing}.`);
    onClose();
    setIsCorrect(null);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-neutral-800 p-6 rounded-lg text-center relative">
        <h1 className="text-2xl mb-4">Prediction: {prediction}</h1>
        {isCorrect === null ? (
          <div>
            <button
              className="bg-green-500 text-white py-2 px-4 rounded-lg mr-2"
              onClick={() => handleConfirmation(true)}
            >
              Yes, that's correct
            </button>
            <button
              className="bg-red-500 text-white py-2 px-4 rounded-lg"
              onClick={() => handleConfirmation(false)}
            >
              No, that's incorrect
            </button>
          </div>
        ) : isCorrect === false ? (
          <div>
            <label className="block mb-2">
              What did you actually draw?
              <input
                type="text"
                value={actualDrawing}
                onChange={handleActualDrawingInput}
                className="border p-2 rounded-lg w-full mt-2 text-black"
              />
            </label>
            <button
              className="bg-blue-500 text-white py-2 px-4 rounded-lg"
              onClick={handleSubmit}
            >
              Submit
            </button>
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default PredictionCheckerModal;
