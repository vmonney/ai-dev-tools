import { useState, useEffect, useCallback, useRef } from 'react';

const GRID_SIZE = 20;
const CELL_SIZE = 20;
const INITIAL_SNAKE = [{ x: 10, y: 10 }];
const INITIAL_DIRECTION = { x: 1, y: 0 };
const GAME_SPEED = 150;

const SnakeGame = () => {
  const [snake, setSnake] = useState(INITIAL_SNAKE);
  const [direction, setDirection] = useState(INITIAL_DIRECTION);
  const [food, setFood] = useState({ x: 15, y: 15 });
  const [gameOver, setGameOver] = useState(false);
  const [paused, setPaused] = useState(false);
  const [score, setScore] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);

  const directionRef = useRef(direction);

  useEffect(() => {
    directionRef.current = direction;
  }, [direction]);

  const generateFood = useCallback(() => {
    let newFood;
    do {
      newFood = {
        x: Math.floor(Math.random() * GRID_SIZE),
        y: Math.floor(Math.random() * GRID_SIZE),
      };
    } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
    return newFood;
  }, [snake]);

  const resetGame = () => {
    setSnake(INITIAL_SNAKE);
    setDirection(INITIAL_DIRECTION);
    directionRef.current = INITIAL_DIRECTION;
    setFood({ x: 15, y: 15 });
    setGameOver(false);
    setPaused(false);
    setScore(0);
    setGameStarted(true);
  };

  const moveSnake = useCallback(() => {
    if (gameOver || paused || !gameStarted) return;

    setSnake(prevSnake => {
      const head = prevSnake[0];
      const newHead = {
        x: head.x + directionRef.current.x,
        y: head.y + directionRef.current.y,
      };

      if (
        newHead.x < 0 ||
        newHead.x >= GRID_SIZE ||
        newHead.y < 0 ||
        newHead.y >= GRID_SIZE ||
        prevSnake.some(segment => segment.x === newHead.x && segment.y === newHead.y)
      ) {
        setGameOver(true);
        return prevSnake;
      }

      const newSnake = [newHead, ...prevSnake];

      if (newHead.x === food.x && newHead.y === food.y) {
        setScore(prev => prev + 10);
        setFood(generateFood());
        return newSnake;
      }

      newSnake.pop();
      return newSnake;
    });
  }, [gameOver, paused, gameStarted, food, generateFood]);

  useEffect(() => {
    const handleKeyPress = (e) => {
      if (!gameStarted && e.key === ' ') {
        e.preventDefault();
        resetGame();
        return;
      }

      if (e.key === ' ') {
        e.preventDefault();
        setPaused(prev => !prev);
        return;
      }

      const currentDir = directionRef.current;

      switch (e.key) {
        case 'ArrowUp':
          e.preventDefault();
          if (currentDir.y === 0) {
            setDirection({ x: 0, y: -1 });
          }
          break;
        case 'ArrowDown':
          e.preventDefault();
          if (currentDir.y === 0) {
            setDirection({ x: 0, y: 1 });
          }
          break;
        case 'ArrowLeft':
          e.preventDefault();
          if (currentDir.x === 0) {
            setDirection({ x: -1, y: 0 });
          }
          break;
        case 'ArrowRight':
          e.preventDefault();
          if (currentDir.x === 0) {
            setDirection({ x: 1, y: 0 });
          }
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [gameStarted]);

  useEffect(() => {
    const gameLoop = setInterval(moveSnake, GAME_SPEED);
    return () => clearInterval(gameLoop);
  }, [moveSnake]);

  const isCellSnake = (x, y) => {
    return snake.some(segment => segment.x === x && segment.y === y);
  };

  const isCellHead = (x, y) => {
    return snake[0]?.x === x && snake[0]?.y === y;
  };

  const isCellFood = (x, y) => {
    return food.x === x && food.y === y;
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <div className="mb-6 text-center">
        <h1 className="text-5xl font-bold text-white mb-2">Snake Game</h1>
        <div className="text-3xl font-semibold text-green-400">Score: {score}</div>
      </div>

      <div className="relative bg-gray-800 p-2 rounded-lg shadow-2xl">
        <div
          className="grid gap-0 border-4 border-green-500 rounded-lg overflow-hidden"
          style={{
            gridTemplateColumns: `repeat(${GRID_SIZE}, ${CELL_SIZE}px)`,
            gridTemplateRows: `repeat(${GRID_SIZE}, ${CELL_SIZE}px)`,
          }}
        >
          {Array.from({ length: GRID_SIZE }).map((_, y) =>
            Array.from({ length: GRID_SIZE }).map((_, x) => (
              <div
                key={`${x}-${y}`}
                className={`
                  ${isCellSnake(x, y)
                    ? isCellHead(x, y)
                      ? 'bg-green-400'
                      : 'bg-green-500'
                    : isCellFood(x, y)
                      ? 'bg-red-500'
                      : 'bg-gray-900'}
                  ${isCellFood(x, y) ? 'animate-pulse' : ''}
                  transition-colors duration-100
                `}
                style={{ width: CELL_SIZE, height: CELL_SIZE }}
              />
            ))
          )}
        </div>

        {!gameStarted && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-70 rounded-lg">
            <div className="text-center">
              <h2 className="text-4xl font-bold text-white mb-4">Welcome!</h2>
              <p className="text-xl text-gray-300 mb-6">Press SPACE to Start</p>
            </div>
          </div>
        )}

        {gameOver && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-70 rounded-lg">
            <div className="text-center">
              <h2 className="text-4xl font-bold text-red-500 mb-4">Game Over!</h2>
              <p className="text-2xl text-white mb-2">Final Score: {score}</p>
              <button
                onClick={resetGame}
                className="mt-4 px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg transition-colors"
              >
                Play Again
              </button>
            </div>
          </div>
        )}

        {paused && !gameOver && gameStarted && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-70 rounded-lg">
            <div className="text-center">
              <h2 className="text-4xl font-bold text-yellow-400 mb-4">Paused</h2>
              <p className="text-xl text-gray-300">Press SPACE to Resume</p>
            </div>
          </div>
        )}
      </div>

      <div className="mt-6 text-center text-gray-300 space-y-2">
        <p className="text-lg font-semibold">Controls:</p>
        <div className="flex flex-col gap-1">
          <p>Arrow Keys - Move</p>
          <p>SPACE - Pause/Resume</p>
        </div>
      </div>
    </div>
  );
};

export default SnakeGame;
