import React, { useState, useEffect, useCallback, useRef } from 'react';

const GRID_SIZE = 20;
const CELL_SIZE = 20;
const INITIAL_SNAKE = [{ x: 10, y: 10 }];
const INITIAL_DIRECTION = { x: 1, y: 0 };
const GAME_SPEED = 150;

export default function SnakeGame() {
  const [snake, setSnake] = useState(INITIAL_SNAKE);
  const [food, setFood] = useState({ x: 15, y: 15 });
  const [direction, setDirection] = useState(INITIAL_DIRECTION);
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const [wallMode, setWallMode] = useState(true); // true = walls, false = pass-through
  
  const directionRef = useRef(direction);

  useEffect(() => {
    directionRef.current = direction;
  }, [direction]);

  const generateFood = useCallback(() => {
    let newFood;
    do {
      newFood = {
        x: Math.floor(Math.random() * GRID_SIZE),
        y: Math.floor(Math.random() * GRID_SIZE)
      };
    } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
    return newFood;
  }, [snake]);

  const resetGame = () => {
    setSnake(INITIAL_SNAKE);
    setDirection(INITIAL_DIRECTION);
    setFood({ x: 15, y: 15 });
    setGameOver(false);
    setScore(0);
    setIsPaused(false);
    setGameStarted(true);
  };

  const moveSnake = useCallback(() => {
    if (gameOver || isPaused || !gameStarted) return;

    setSnake(prevSnake => {
      const head = prevSnake[0];
      let newHead = {
        x: head.x + directionRef.current.x,
        y: head.y + directionRef.current.y
      };

      // Handle wall collision or pass-through
      if (wallMode) {
        // Walls mode - check collision
        if (
          newHead.x < 0 ||
          newHead.x >= GRID_SIZE ||
          newHead.y < 0 ||
          newHead.y >= GRID_SIZE
        ) {
          setGameOver(true);
          return prevSnake;
        }
      } else {
        // Pass-through mode - wrap around
        if (newHead.x < 0) newHead.x = GRID_SIZE - 1;
        if (newHead.x >= GRID_SIZE) newHead.x = 0;
        if (newHead.y < 0) newHead.y = GRID_SIZE - 1;
        if (newHead.y >= GRID_SIZE) newHead.y = 0;
      }

      // Check self collision
      if (prevSnake.some(segment => segment.x === newHead.x && segment.y === newHead.y)) {
        setGameOver(true);
        return prevSnake;
      }

      const newSnake = [newHead, ...prevSnake];

      // Check food collision
      if (newHead.x === food.x && newHead.y === food.y) {
        setScore(prev => prev + 10);
        setFood(generateFood());
      } else {
        newSnake.pop();
      }

      return newSnake;
    });
  }, [gameOver, isPaused, gameStarted, food, generateFood, wallMode]);

  useEffect(() => {
    const gameLoop = setInterval(moveSnake, GAME_SPEED);
    return () => clearInterval(gameLoop);
  }, [moveSnake]);

  useEffect(() => {
    const handleKeyPress = (e) => {
      if (!gameStarted && e.key.startsWith('Arrow')) {
        setGameStarted(true);
      }

      if (e.key === ' ') {
        e.preventDefault();
        setIsPaused(prev => !prev);
        return;
      }

      const currentDir = directionRef.current;

      switch (e.key) {
        case 'ArrowUp':
          if (currentDir.y === 0) setDirection({ x: 0, y: -1 });
          break;
        case 'ArrowDown':
          if (currentDir.y === 0) setDirection({ x: 0, y: 1 });
          break;
        case 'ArrowLeft':
          if (currentDir.x === 0) setDirection({ x: -1, y: 0 });
          break;
        case 'ArrowRight':
          if (currentDir.x === 0) setDirection({ x: 1, y: 0 });
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [gameStarted]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-900 via-green-800 to-green-900 p-8">
      <div className="mb-6 text-center">
        <h1 className="text-5xl font-bold text-green-300 mb-2 drop-shadow-lg">Snake Game</h1>
        <div className="text-3xl font-bold text-white mb-4">Score: {score}</div>
        <div className="flex items-center justify-center gap-4">
          <span className="text-lg text-green-200">Mode:</span>
          <button
            onClick={() => setWallMode(!wallMode)}
            disabled={gameStarted && !gameOver}
            className={`px-6 py-2 rounded-lg font-semibold text-lg transition-all ${
              gameStarted && !gameOver
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed opacity-50'
                : 'bg-green-600 hover:bg-green-700 text-white shadow-lg'
            }`}
          >
            {wallMode ? '🧱 Walls' : '🌀 Pass-through'}
          </button>
        </div>
        {gameStarted && !gameOver && (
          <p className="text-sm text-yellow-300 mt-2">⚠️ Restart game to change mode</p>
        )}
      </div>

      <div 
        className={`relative bg-green-950 border-4 rounded-lg shadow-2xl transition-colors ${
          wallMode ? 'border-red-600' : 'border-blue-500'
        }`}
        style={{ 
          width: GRID_SIZE * CELL_SIZE, 
          height: GRID_SIZE * CELL_SIZE 
        }}
      >
        {/* Game Grid */}
        <div className="absolute inset-0">
          {snake.map((segment, index) => (
            <div
              key={index}
              className={`absolute ${index === 0 ? 'bg-green-400' : 'bg-green-500'} rounded-sm border border-green-600`}
              style={{
                width: CELL_SIZE - 2,
                height: CELL_SIZE - 2,
                left: segment.x * CELL_SIZE,
                top: segment.y * CELL_SIZE,
              }}
            />
          ))}
          <div
            className="absolute bg-red-500 rounded-full animate-pulse"
            style={{
              width: CELL_SIZE - 4,
              height: CELL_SIZE - 4,
              left: food.x * CELL_SIZE + 2,
              top: food.y * CELL_SIZE + 2,
            }}
          />
        </div>

        {/* Overlays */}
        {!gameStarted && (
          <div className="absolute inset-0 bg-black bg-opacity-75 flex items-center justify-center">
            <div className="text-center">
              <p className="text-white text-2xl mb-4 font-semibold">Press any arrow key to start!</p>
              <p className="text-green-300 text-lg">Use arrow keys to move</p>
              <p className="text-green-300 text-lg">Press SPACE to pause</p>
              <div className="mt-4 pt-4 border-t border-green-600">
                <p className="text-yellow-300 text-xl font-bold">
                  Current Mode: {wallMode ? '🧱 Walls' : '🌀 Pass-through'}
                </p>
              </div>
            </div>
          </div>
        )}

        {isPaused && gameStarted && !gameOver && (
          <div className="absolute inset-0 bg-black bg-opacity-75 flex items-center justify-center">
            <p className="text-white text-3xl font-bold">PAUSED</p>
          </div>
        )}

        {gameOver && (
          <div className="absolute inset-0 bg-black bg-opacity-80 flex items-center justify-center">
            <div className="text-center">
              <p className="text-red-500 text-4xl font-bold mb-4">Game Over!</p>
              <p className="text-white text-2xl mb-6">Final Score: {score}</p>
              <button
                onClick={resetGame}
                className="px-8 py-3 bg-green-500 hover:bg-green-600 text-white font-bold rounded-lg text-xl transition-colors shadow-lg"
              >
                Play Again
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="mt-6 text-center text-green-200 space-y-2">
        <p className="text-lg">🎮 Use <span className="font-bold">Arrow Keys</span> to control the snake</p>
        <p className="text-lg">⏸️ Press <span className="font-bold">Space</span> to pause/resume</p>
        <div className="mt-4 pt-4 border-t border-green-700">
          <p className="text-lg font-semibold mb-2">Game Modes:</p>
          <p className="text-sm"><span className="font-bold">🧱 Walls:</span> Hit the walls and game over</p>
          <p className="text-sm"><span className="font-bold">🌀 Pass-through:</span> Go through walls and appear on the other side</p>
        </div>
      </div>
    </div>
  );
}